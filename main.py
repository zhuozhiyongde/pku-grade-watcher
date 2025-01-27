#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author  :   Arthals
# @File    :   main.py
# @Time    :   2024/08/10 03:06:58
# @Contact :   zhuozhiyongde@126.com
# @Software:   Visual Studio Code

import yaml

from session import BarkNotifier, Session


def start():
    config = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
    username = config["username"]
    password = config["password"]
    bark = config["bark"]

    if not username or not password:
        raise ValueError("username, password are required")

    if not bark:
        notifier = None
    else:
        notifier = BarkNotifier(bark)

    data = {
        "username": username,
        "password": password,
    }

    s = Session(config=data, notifier=notifier)
    s.run()


if __name__ == "__main__":
    start()
