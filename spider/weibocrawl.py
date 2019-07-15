import os
import random
import re
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


def saveProfile(nick_name, img_src, cat_name, current_url):
    # 把50*50图片地址转换成150*150图片地址
    larger_src = re.sub("50/", "150/", img_src)
    resp = requests.get(larger_src, headers={"User-Agent": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/75.0.3770.100 safari/537.36", "Referer": current_url})
    cat_dir_path = cat_name + "/"
    if not os.path.exists(cat_dir_path):
        os.makedirs(cat_dir_path)
    if resp.status_code == 200:
        img_file_name = cat_dir_path + nick_name + ".jpg"
        with open(img_file_name, 'wb') as file:
            file.write(resp.content)
            print("save file ", img_file_name)
    else:
        print(resp.status_code, "error saving img")


def openCat(browser, category_url, cat_name):
    browser.get(category_url)
    time.sleep(5)
    page_num = browser.find_element_by_xpath("//div[@class='W_pages']/a[last()-1]").text
    for index in range(int(page_num)):
        js = "document.documentElement.scrollTop=10000"
        browser.execute_script(js)
        time.sleep(random.randint(3, 7))
        # 下一页
        try:
            next_page_ele = browser.find_element_by_xpath("//div[@class='W_pages']/a[last()]")
            user_ele_list = browser.find_elements_by_xpath("//ul[@class='follow_list']/li/dl/dt/a/img")
            cur_page_num = browser.find_element_by_xpath("//div[@class='W_pages']/a[contains(@class, 'S_bg1')]").text
        except NoSuchElementException as e:
            print("page exception, now sleep and retry")
            time.sleep(30)
            browser.refresh()
            continue
        print("category:", cat_name, ", total page:", page_num, ", current page:", cur_page_num)
        for ele in user_ele_list:
            nick_name = ele.get_attribute("alt")
            img_src = ele.get_attribute("src")
            print(nick_name, img_src)
            saveProfile(nick_name, img_src, cat_name, browser.current_url)
        next_page_ele.click()
        time.sleep(3)


def startBrowser():
    chrome_options = Options()
    chrome_options.add_argument("user-agent=mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/75.0.3770.100 safari/537.36")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(options=chrome_options)
    browser.get("https://weibo.com/?topnav=1&mod=logo")
    time.sleep(12)
    category_ele_list = browser.find_elements_by_xpath("//ul[@class='clearfix']/li/a[@class='S_txt1']")
    print("category length:" + str(len(category_ele_list)))
    pair_list = []
    for ele in category_ele_list:
        href = ele.get_attribute("href")
        category = ele.find_element_by_class_name("W_autocut")
        category_name = category.text
        pair_list.append((category_name, href))
    for category_name, href in pair_list:
        print(category_name, href, "\n")
        openCat(browser, href, category_name)


if __name__ == '__main__':
    startBrowser()
