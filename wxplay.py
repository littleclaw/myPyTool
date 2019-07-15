from wxpy import *
import requests
import re
import tuling

bot = Bot()
friends = bot.friends()
jane = ensure_one(bot.search("简简"))
ltt_bing = ensure_one(bot.search("小冰"))
logger = get_wechat_logger(bot)
fhelper = bot.file_helper
session_flag = False


@bot.register(ltt_bing)
def reply_ltt_bing(msg):
    msg.forward(jane)
    print(msg.type)


@bot.register(jane)
def reply_jane(msg):
    print("incoming msg -->"+msg.text + "---" + msg.type)
    msg.sender.mark_as_read()

    startSession(msg)
    msg.forward(ltt_bing)


def startSession(msg):
    global session_flag
    if not session_flag:
        msg.reply("嗨！我是小爪领养的小冰，今天他带我出来透个气，顺便帮他回下简简小姐的微信，只好勉为其难了")
        session_flag = True


def to_j(msg):
    jane.send(msg)


def good_bye():
    jane.send("小冰下线啦，( ^_^ )/~~拜拜")
    global session_flag
    session_flag = False
    exit(0)


# 堵塞线程
embed()



