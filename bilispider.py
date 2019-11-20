import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}


def startBrowser():
    chrome_options = Options()
    chrome_options.add_argument("user-agent=mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/75.0.3770.100 safari/537.36")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(options=chrome_options)
    browser.get("https://space.bilibili.com/32479133/")
    time.sleep(12)
    # print(browser.page_source)
    page = etree.HTML(browser.page_source)
    give_coin_items = page.xpath("//div[@class='small-item fakeDanmu-item']/a[@class='title']/text()")
    give_coin_items_filtered = []
    for item in give_coin_items:
        give_coin_items_filtered.append(item.replace('\n', '').strip())
    print(give_coin_items_filtered)
    collect_name = page.xpath("//div[@class='fav-item']/div[@class='m']/a[@class='name']/text()")
    collect_item_count = page.xpath("//div[@class='fav-item']/span[@class='fav-count']/text()")
    collect_tuple_list = []
    if len(collect_name) == len(collect_item_count):
        for index, name in enumerate(collect_name):
            name = name.replace('\n', '').strip()
            count = collect_item_count[index]
            collect_tuple_list.append((name, count))
    print(collect_tuple_list)
    with open('janeBilibili.txt', 'w') as file:
        file.write(str(give_coin_items_filtered))
        file.write('\n')
        file.write(str(collect_tuple_list))


if __name__ == '__main__':
    startBrowser()
