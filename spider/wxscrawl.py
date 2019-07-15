import time

import requests

headers = {
    "Origin": "https://account.wxb.com",
    "Referer": "https://account.wxb.com/page/login?from=https://data.wxb.com/rankArticle",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}
base_url = "https://data.wxb.com/rank/article"
claw_url = "http://174.137.54.154:8080/parse/add"


def crawlCategory(session, cat):
    print("开始类别：" + cat)
    first_page_resp = session.get(url=base_url, params={"baidu_cat": cat, "page": 1, "pageSize": 20, "type": 2}, headers=headers, timeout=20)
    first_page_resp.encoding = "utf-8"
    print(first_page_resp.text)
    category_json = first_page_resp.json()
    max_page = category_json['pager']['numPages']
    print(cat, max_page)
    for i in range(1, int(max_page)):
        crawlPage(session, cat, i)


def crawlPage(session, cat, page):
    page_resp = session.get(url=base_url, params={"baidu_cat": cat, "page": page, "pageSize": 20, "type": 2}, headers=headers, timeout=10)
    print(page_resp.url)
    page_resp.encoding = "utf-8"
    page_json = page_resp.json()
    data_list = page_json['data']
    for article_link in data_list:
        sendUrl(article_link['url'])
    time.sleep(2)


def sendUrl(url):
    send_resp = requests.post(claw_url, data={"url": url, "type": "3"}, timeout=8)
    print(url)
    print(send_resp.status_code, send_resp.text)


if __name__ == '__main__':
    session = requests.session()
    session.post("https://account.wxb.com/index2/login", data={"email": "13123456785", "from": "https://data.wxb.com/rankArticle", "password": "your_pwd", "remember": "on"}, headers=headers)
    main_page_resp = session.get("https://data.wxb.com/rankArticle", headers=headers)
    main_page_resp.encoding = "utf-8"
    for cookie in session.cookies:
        print(cookie.name, cookie.value)
    headers['Referer'] = "https://data.wxb.com/rankArticle"
    cat_resp = session.get("https://data.wxb.com/rank/articleCatalog", headers=headers)
    cat_list = cat_resp.json()['data']
    print(cat_list)
    for cat in cat_list[1:]:
        crawlCategory(session, cat)
    session.close()
