#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author  :   Arthals
# @File    :   main.py
# @Time    :   2024/08/10 03:06:58
# @Contact :   zhuozhiyongde@126.com
# @Software:   Visual Studio Code

import os
from datetime import datetime

from session import BarkNotifier, Session


def start():
    print(f"{'[Start]':<15}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    username = os.getenv("username", "")
    password = os.getenv("password", "")
    bark = os.getenv("bark", "")

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
    s.login()
    s.get_grade()
    s.check_update()

    print(f"{'[End]':<15}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    start()
