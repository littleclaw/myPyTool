import hashlib
import json
import random
import re
import time

import requests

post_url = "http://api.xklm.net/order/submit"
comment_codes = ['XHS103', 'KS103', 'DY103', 'WX103', 'DY106']
# 后台执行
background = True
apiKey = "your_key"
apiSecret = "your_secret"
comment_amount = 100


# sign加密方式：MD5(MD5(productCode=WX101&url=http://www.baidu.com&amount=100)+密钥（api Secret）)
def sign(par, tstamp):
    if par['productCode'] in comment_codes:
        pre_sign = "amount={}&comments={}&productCode={}&timestamp={}&url={}&apiKey={}".format(par['amount'],
                                                                                               len(par['comments']),
                                                                                               par['productCode'],
                                                                                               tstamp, par['url'],
                                                                                               apiKey)
    else:
        pre_sign = 'amount={}&productCode={}&timestamp={}&url={}&apiKey={}'.format(par['amount'], par['productCode'],
                                                                                   tstamp, par['url'], apiKey)
    print("pre_sign_info:" + pre_sign)
    signstr = md5(md5(pre_sign) + apiSecret)
    print("sign result: " + signstr)
    return signstr


def md5(txt):
    m = hashlib.md5()
    m.update(txt.encode("utf-8"))
    return m.hexdigest()


def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


def inferProductCode(task_url):
    if re.match(r"^https?://mp.weixin.qq.com/s.*", task_url):
        if background:
            code_list = ["WX101", "WX102", "WX103", "WX104"]
            probability_list = [0.2, 0.3, 0.2, 0.3]
            return random_pick(code_list, probability_list)
        else:
            return "WX001"
    elif re.match(r"^http://m.chenzhongtech.com/s/.*", task_url) or re.match(r"^http://m.gifshow.com/s/.*", task_url):
        if background:
            code_list = ["KS101", "KS102", "KS103", "KS104"]
            probability_list = [0.4, 0.2, 0.2, 0.2]
            return random_pick(code_list, probability_list)
        else:
            return "KS001"
    elif re.match(r"^http://v.douyin.com/.*", task_url):
        if background:
            code_list = ["DY101", "DY102", "DY103", "DY104", "DY106"]
            probability_list = [0.4, 0.2, 0.2, 0.2, 0.0]
            return random_pick(code_list, probability_list)
        else:
            return "DY001"
    elif re.match(r"^https://www.xiaohongshu.com/discovery/item/.*", task_url) or re.match(r"http://t.cn/.+", task_url):
        if background:
            code_list = ["XHS101", "XHS102", "XHS103", "XHS104", "XHS105"]
            probability_list = [0.3, 0.1, 0.2, 0.2, 0.2]
            return random_pick(code_list, probability_list)
        else:
            return "XHS001"
    else:
        print("任务url不符合任何可解析的url，程序中止")
        exit(0)


def request_order(param_url):
    try:
        timestamp = str(int(time.time() * 1000))
        product_code = inferProductCode(param_url)
        if product_code in comment_codes:
            max_comment_amount = 100
            params = {
                "productCode": product_code,
                "url": param_url,
                "amount": str(max_comment_amount),
                "comments": generateComments(max_comment_amount)
            }
        else:
            params = {
                "productCode": product_code,
                "url": param_url,
                "amount": str(comment_amount),
            }
        headers = {"apiKey": apiKey, "sign": sign(params, timestamp), "timestamp": timestamp,
                   "Content-Type": "application/json", "charset": "utf-8"}
        paramjson = json.dumps(params, ensure_ascii=False)
        print("开始请求……", "参数为：", paramjson)
        resp = requests.post(post_url, data=json.dumps(params), headers=headers, timeout=90)
        print("请求结束，状态码：" + str(resp.status_code))
        if resp.status_code == 200:
            print(resp.json())
            result = json.loads(resp.text)
            msg = result['msg']
            if msg == "成功" or msg == "此链接已下单" or msg == "不允许录入相同资源" or msg == "URL解析失败,请检查是否输入正确" or msg == "解析url地址失败":
                del_api = "http://127.0.0.1:8080/parse/delete"
                del_resp = requests.post(del_api, data={"url": param_url})
                print("删除链接，返回值：" + del_resp.text)
        else:
            print("请求结果异常，跳过链接", resp.status_code, resp.text)
            return "", ""
    except Exception as e:
        print("请求异常，跳过链接", e)
        return "", ""
    return result['data'], result['msg']


def generateComments(amount):
    comment_pool_list = ["吃瓜群众", "我就看看不说话", "强势围观", "偶滴神呐", "前排混分", "城市套路深", "给力", "我服了", "我是一只路过打酱油的",
                         "浮生若梦", "前尘旧梦", "什么鬼", "wtf", "是狼火", "秀色可餐", "盛世美颜", "这也太好看了吧", "好腻害", "引起舒适",
                         "火钳留名", "悄悄的我来了", "橘里橘气", "抢前排", "一脸懵逼", "贫穷限制了我的想象力", "这也可以啊", "火前留名",
                         "水经验", "赛高", "awsl", "霸气", "是个狼人", "请允悲", "一颗赛艇", "因垂丝汀", "秀飞", "飘过", "不错", "太棒了",
                         "么么哒", "顶一下", "打卡", "冒泡", "扎Zn了，老Fe", "还有这种操作", "皮皮虾我们走", "skr,skr", "阅", "留爪",
                         "不明觉厉", "累觉不爱", "施主真是慈悲", "我伙呆", "画美不看", "陈独秀", "确认过眼神", "真实", "你忙吧我吃柠檬",
                         "城会玩", "乡话多", "破事水", "万火留", "醒工砖", "同九何秀", "社会我老哥", "雨女无瓜", "同学你好，同学再见",
                         "我的天", "真是个小天才", "interesting", "pretty", "nice show", "wonderful", "可把我震住了", "<（￣︶￣）>",
                         "┬─┬ ノ( ' - 'ノ)", "糟糕，是心动的感觉", "一花依世界",
                         "[]~（￣▽￣）~*", "Σ（ ° △ °|||）︴", "（=￣ω￣=）", "（￣0 ￣）y", "（→_→）", "◑ω◐", "(╯°Д°)╯ ┻━┻"]*2
    comment_slice = random.sample(comment_pool_list, amount)
    random.shuffle(comment_slice)
    return comment_slice


def orderList(type_code, targetAmount=0, spList=None):
    if spList is None:
        spList = []
    global fail_url_lists, fail_resp_list, urls, url, background
    result = ""
    fail_url_lists = []
    fail_resp_list = []
    if len(spList) == 0:
        auto_url = "http://127.0.0.1:8080/parse/get?type=" + type_code
        print("获取分享链接列表……")
        resp = requests.get(auto_url)
        urls = list(json.loads(resp.text))
        print("此次待解析url总数：" + str(len(urls)))
        if resp.status_code == 200:
            fg_num = len(urls) / 30
            if len(urls) == 0:
                print("没有可执行的url，程序结束")
                exit(0)
            i, success_num = 0, 0
            for url in urls:
                if i > fg_num:
                    background = True
                i = i + 1
                print(i)
                print(url)
                success, msg = request_order(url)
                if success:
                    success_num += 1
                    if targetAmount > 0 and targetAmount == success_num:
                        print("完成此次任务")
                        exit(0)
                else:
                    fail_url_lists.append(url)
                    fail_resp_list.append(msg)
            result = "执行结束，总执行次数{0},成功次数{1}，失败次数{2},成功率{3}".format(i, success_num, i - success_num,
                                                                   str(100 * success_num / i) + '%')
            print(result)
            if len(fail_url_lists) > 0:
                for url in fail_url_lists:
                    print(url)
    else:
        for url in spList:
            success, msg = request_order(url)
            print(success, msg)


if __name__ == '__main__':
    # 1抖音2快手3微信4小红书
    order_type = '2'
    orderList(order_type, 300)
    # orderList(order_type, spList=["https://mp.weixin.qq.com/s/tcPf7xuGK6x0AFLZzXaYhA",
    #                               "https://mp.weixin.qq.com/s/y1bJ1Z6Xtp79o9Lx5Yddyw"])
