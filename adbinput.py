import time
import subprocess


def call(cmd, wait=2):
    result = subprocess.call(cmd, shell=True)
    if result != 0:
        print("执行命令" + cmd + "出错，程序退出")
        exit(-1)
    else:
        time.sleep(wait)


def adbCall(cmd):
    call("adb shell input " + cmd)


def runDy(num):
    for i in range(num):
        print("当前执行第" + str(i) + "次")
        call("adb shell input tap 1025 1640")
        call("adb shell input swipe 950 1900 100 1900")
        call("adb shell input tap 542 1870")
        # time.sleep(2)
        call("adb shell input swipe 200 1630 250 400")


def runXhs(num):
    for i in range(num):
        print("当前执行第" + str(i) + "次")
        call("adb shell input tap 290 725")
        call("adb shell input tap 1013 200")
        call("adb shell input tap 321 1870")
        call("adb shell input keyevent 4")
        call("adb shell input tap 800 725")
        call("adb shell input tap 1013 190")
        call("adb shell input tap 321 1870")
        call("adb shell input keyevent 4")
        call("adb shell input swipe 500 1790 500 880")


def runXhsOtherWay(num):
    for i in range(num):
        print("当前执行第" + str(i) + "次")
        call("adb shell input tap 1013 200")
        call("adb shell input tap 321 1870")
        call("adb shell input swipe 500 1790 500 880")


def runKs(num):
    for i in range(num):
        print("当前执行第" + str(i) + "次")
        call("adb shell input tap 290 725", 4)
        call("adb shell input tap 470 150", 5)
        call("adb shell input keyevent 4")
        call("adb shell input keyevent 4")
        call("adb shell input tap 800 725", 4)
        call("adb shell input tap 480 180", 5)
        call("adb shell input keyevent 4")
        call("adb shell input keyevent 4")
        call("adb shell input swipe 500 1790 500 880", 3)


def runWx(num):
    for i in range(num):
        call("adb shell input tap 940 380")
        call("adb shell input tap 1012 174")
        call("adb shell input tap 686 1560")
        call("adb shell input keyevent 4")
        call("adb shell input swipe 230 1770 230 1530")


if __name__ == '__main__':
    exe_time = 550
    runKs(exe_time)
'''
adb input 指令集
在打开抖音的界面下，点开分享，滑动，点击分享链接,再滑动到下一个视频
input tap 1025 1680
input swipe 600 1900 100 1900 
input tap 730 1870
input swipe 200 1630 250 400
'''
