#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author  :   Arthals
# @File    :   session.py
# @Time    :   2025/01/25 01:44:46
# @Contact :   zhuozhiyongde@126.com
# @Software:   Visual Studio Code


import json
import os
import random
import re
import time
from datetime import datetime
import requests


class Session(requests.Session):
    def __init__(self, config, notifier=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._config = config
        self._notifier = notifier
        self.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0",
                "TE": "Trailers",
                "Pragma": "no-cache",
                "Referer": "https://portal.pku.edu.cn/publicQuery/",
            }
        )

    def __del__(self):
        self.close()

    def get(self, url, *args, **kwargs):
        """重写 get 方法，验证状态码，转化为 json"""
        res = super().get(url, *args, **kwargs)
        res.raise_for_status()
        return res

    def post(self, url, *args, **kwargs):
        """重写 post 方法，验证状态码，转化为 json"""
        res = super().post(url, *args, **kwargs)
        res.raise_for_status()

        return res

    def logger(self, title, info):
        print(
            f"{'[' + title + ']':<15}{'[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']'}: {info}"
        )

    def login(self) -> bool:
        """登录门户，重定向成绩查询"""
        self.cookies.clear()
        self.logger("Login", "正在尝试登录...")
        # IAAA 登录
        json = self.post(
            "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do",
            data={
                "userName": self._config["username"],
                "appid": "portal2017",
                "password": self._config["password"],
                "redirUrl": "https://portal.pku.edu.cn/portal2017/ssoLogin.do",
                "randCode": "",
                "smsCode": "",
                "optCode": "",
            },
        ).json()
        assert json["success"], json

        # 门户 token 验证
        self.get(
            "https://portal.pku.edu.cn/portal2017/ssoLogin.do",
            params={"_rand": random.random(), "token": json["token"]},
        )

        # 成绩查询重定向
        res = self.get(
            "https://portal.pku.edu.cn/portal2017/util/portletRedir.do?portletId=myscores"
        )

        # 获取鉴权 JSESSION ID
        jsessionid = re.search(r"jsessionid=([^#;]+)", res.url).group(1)
        self.cookies.set("JSESSIONID", jsessionid)
        self.logger("Succeed", "登录成功，JSESSIONID: " + jsessionid)

    def get_grade(self):
        """获取成绩"""

        res = self.get(
            "https://portal.pku.edu.cn/publicQuery/ctrl/topic/myScore/retrScores.do",
        ).json()
        with open("current.json", "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=4)

    def check_init(self):
        """检查是否初始化"""
        if not os.path.exists("data.json"):
            # cp current.json to data.json
            with open("current.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self._notifier.send(
                title="[成绩更新] 初始化",
                info="成功初始化成绩数据",
            )

    def check_update(self):
        """检查成绩更新并返回新增课程信息"""
        try:
            # 检查是否初始化
            self.check_init()

            # 读取新数据
            with open("current.json", "r", encoding="utf-8") as f:
                new_data = json.load(f)

            # 读取旧数据，若不存在则初始化空数据
            with open("data.json", "r", encoding="utf-8") as f:
                old_data = json.load(f)

            # 提取所有旧课程ID
            old_ids = set()
            for term in old_data.get("cjxx", []):
                for course in term.get("list", []):
                    if "bkcjbh" in course:
                        old_ids.add(course["bkcjbh"])

            # 提取所有新课程ID
            cur_ids = set()
            new_courses = []
            for term in new_data.get("cjxx", []):
                for course in term.get("list", []):
                    if "bkcjbh" in course:
                        cur_ids.add(course["bkcjbh"])
                        cid = course["bkcjbh"]
                        if cid not in old_ids:
                            new_courses.append(
                                {
                                    "name": course.get("kcmc", "无"),
                                    "grade": course.get("xqcj", "无"),
                                    "gpa": course.get("jd", "无"),
                                }
                            )

            assert len(cur_ids) >= len(old_ids), "异常返回课程数据：" + str(cur_ids)

            # 更新本地数据文件
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)

            if new_courses and self._notifier:
                for course in new_courses:
                    self._notifier.send(
                        title=f"[成绩更新] {course['name']}",
                        info=f"成绩：{course['grade']}，绩点：{course['gpa']}",
                    )

            return new_courses

        except Exception as e:
            self.logger("Error", f"检查更新时出错: {e}")
            raise e

    def check_cycle(self):
        """执行完整的检查周期"""
        # self.logger("Start", "开始成绩检查")
        self.get_grade()
        new_courses = self.check_update()
        if new_courses:
            self.logger("Succeed", f"成功发现 {len(new_courses)} 门新课程")
        else:
            self.logger("Nothing", "未发现新成绩")

    def run(self):
        """永续运行主循环"""
        self.logger("Start", "开始运行")
        while True:
            try:
                self.login()

                # 登录后立即检查一次成绩
                self.check_cycle()

                # 保持会话有效期间定期检查
                while True:
                    time.sleep(60)  # 等待1分钟
                    try:
                        self.check_cycle()
                    except requests.exceptions.HTTPError as e:
                        self.logger("Error", f"检测到会话过期: {e}")
                        raise  # 跳出内层循环重新登录
                    except Exception as e:
                        self.logger("Error", f"检查出错: {e}")

            except Exception as e:
                self.logger("Error", f"运行出错: {e}")
                self.logger("Retry", "60秒后重试...")
                time.sleep(60)
                self.cookies.clear()  # 清除旧cookie


class BarkNotifier:
    def __init__(self, token):
        self._token = token

    def send(self, title, info):
        requests.post(
            f"https://api.day.app/{self._token}",
            data={
                "title": title,
                "body": info,
                "icon": "https://cdn.arthals.ink/pku.jpg",
                "level": "timeSensitive",
            },
        )
