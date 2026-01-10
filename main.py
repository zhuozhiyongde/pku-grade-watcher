#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author  :   Arthals
# @File    :   main.py
# @Time    :   2024/08/10 03:06:58
# @Contact :   zhuozhiyongde@126.com
# @Software:   Visual Studio Code

import os
import time
from datetime import datetime

from session import ServerChanNotifier, Session


def start():
    print(f"{'[Start]':<15}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    username = os.getenv("username", "")
    password = os.getenv("password", "")
    sendkey = os.getenv("sendkey", "")

    print(f"[Debug]      : sendkey from env = '{sendkey[:10]}...' (len={len(sendkey)})" if sendkey else "[Debug]      : sendkey from env = ''")

    if not username or not password:
        raise ValueError("username, password are required")

    if not sendkey:
        print("[Debug]      : sendkey is empty, notifier = None")
        notifier = None
    else:
        print("[Debug]      : creating ServerChanNotifier")
        notifier = ServerChanNotifier(sendkey)

    data = {
        "username": username,
        "password": password,
    }

    s = Session(config=data, notifier=notifier)

    # 测量 login 耗时
    t0 = time.time()
    print("[Debug]      : 正在登录...")
    s.login()
    t1 = time.time()
    print(f"[Debug]      : login 耗时 {t1 - t0:.2f} 秒")

    # 测量 get_grade 耗时
    t0 = time.time()
    print("[Debug]      : 正在获取成绩...")
    s.get_grade()
    t1 = time.time()
    print(f"[Debug]      : get_grade 耗时 {t1 - t0:.2f} 秒")

    # 测量 check_update 耗时
    t0 = time.time()
    print("[Debug]      : 正在检查更新...")
    s.check_update()
    t1 = time.time()
    print(f"[Debug]      : check_update 耗时 {t1 - t0:.2f} 秒")

    print(f"{'[End]':<15}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    start()
