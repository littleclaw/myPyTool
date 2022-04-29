# -*- coding: utf-8 -*-
import subprocess
import re

if __name__ == '__main__':
    # 获取本机下存在的 profile
    profiles = subprocess.run(["netsh", "wlan", "show", "profiles"], shell=False, capture_output=True).stdout.decode('gbk')
    # 将 profile 中的 wifi 名取出
    wifi_names = (re.findall("所有用户配置文件 : (.*)\r", profiles))
    for wifi_name in wifi_names:
        # 获取 profile 中的密码
        profile_info = subprocess.run(["netsh", "wlan", "show", "profiles", wifi_name, "key=clear"],
                                      shell=False, capture_output=True).stdout.decode('gbk')
        # 将 profile 中的 wifi 密码取出
        key = (re.findall("关键内容            : (.*)\r", profile_info))
        if len(key) > 0:
            print('name = ' + wifi_name + ', password =', key[0])
        else:
            print(wifi_name + "No passwd found")
