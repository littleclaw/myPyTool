import requests
import time
import adbinput
import re

kusishou_itemId = "2281"
douyin_itemId = "7732"
xhs_itemId = "190"


class Yima():
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd
        self.token = ""
        self.url = "http://api.fxhyd.cn/UserInterface.aspx"

    def login(self):
        loginResp = requests.get(self.url, params={"action": "login", "username": self.username, "password": self.passwd}, timeout=10)
        if loginResp.status_code == 200:
            print(loginResp.text)
            if "success" in loginResp.text:
                self.token = loginResp.text.split('|')[-1]
            else:
                print("登录失败")
        else:
            print(loginResp.status_code)

    def loginWithToken(self, token):
        self.token = token
        print("token set" + self.token)

    def getAccountStatus(self):
        if self.isLogin():
            statusResp = requests.get(self.url, params={"action": "getaccountinfo", "token": self.token})
            print(statusResp.status_code, statusResp.text)

    def getPhone(self, itemId):
        if self.isLogin():
            phoneResp = requests.get(self.url, params={"action": "getmobile", "token": self.token, "itemid": itemId, "timestamp": time.time()})
            print(phoneResp.status_code, phoneResp.text)
            if phoneResp.status_code == 200 and "success" in phoneResp.text:
                return phoneResp.text.split('|')[-1]

    def getSmsCode(self, phone, itemId):
        if self.isLogin():
            max_try = 20
            tried_time = 0
            while tried_time < max_try:
                smsResp = requests.get(self.url, params={"action": "getsms", "token": self.token, "itemid": itemId, "mobile": phone, "release": 1, "timestamp": time.time()}, timeout=10)
                smsResp.encoding = "utf-8"
                print(smsResp.text)
                if smsResp.status_code == 200 and "success" in smsResp.text:
                    smsText = smsResp.text.split('|')[-1]
                    return smsText
                tried_time += 1
                time.sleep(5)
            return ""

    def enBlackListPhone(self, phone):
        pass

    def isLogin(self):
        return self.token is not None and self.token != ""


def getCodeFromSms(sms):
    code = re.search(r"\d{6}", sms).group(0)
    print(code)
    return code


if __name__ == '__main__':
    yima = Yima("sopaby", "x147258")
    yima.loginWithToken("01544573454150d176c5b419507378453e5449989801")
    yima.getAccountStatus()
    itemid = kusishou_itemId
    temp_phone = yima.getPhone(itemid)
    print("获取到的手机号为：" + temp_phone)
    input("type sth")
    sms = yima.getSmsCode(temp_phone, itemid)
    # code = getCodeFromSms(sms)
    # getCodeFromSms("success|【小红书】您的验证码是: 116069，3分钟内有效。请勿向他人泄漏。如非本人操作，可忽略本消息。")
