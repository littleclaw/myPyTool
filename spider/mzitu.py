import requests
from lxml import etree
import os
import time
import random
import re
import urllib3

baseUrl = 'https://www.mzitu.com/'
referer = baseUrl
header = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Referer': referer,
}
proxies_list = ['23.105.216.193:3128', '174.137.54.228:3128']


def rand_proxy():
    proxy = None
    randentry = random.randint(1, 3)
    print(randentry)
    if randentry == 1 or randentry == 2:
        proxy = {"http": "http://" + proxies_list[randentry - 1]}
    return proxy


def parse_category_page_count(tree):
    result = tree.xpath("//a[@class='page-numbers'][last()]")
    return int(result[0].text)


def download_album_pics(category, album):
    src = album['src']
    description = album['alt']
    date = album['time']
    proxies = rand_proxy()
    print("using proxy:" + proxies.__str__())
    response = requests.get(src, headers=header, verify=False, timeout=5, proxies=proxies)
    html = response.text
    global referer
    referer = src
    pic_count = etree.HTML(html).xpath("//div[@class='pagenavi']/a[last()-1]/span")[0].text
    pic_count = int(pic_count)
    album_dir_name = "[{0:2d}P]{1}-{2}".format(pic_count, description, date)
    album_dir_name = re.sub(r'[\\/:*?"<>|\r\n]+', '-', album_dir_name)
    album_path = category + '/' + album_dir_name
    if not os.path.exists(album_path):
        os.mkdir(album_path)
    for i in range(1, pic_count):
        page_url = src
        if i > 1:
            page_url = src + '/' + str(i)
        print('page url :' + page_url)
        try:
            resp_page = requests.get(page_url, headers=header, verify=False, timeout=7, proxies=proxies)
        except requests.exceptions.ConnectionError as e:
            print(page_url + "connection error, " + str(e))
            continue
        except requests.exceptions.ReadTimeout:
            print('readTimeout')
            continue
        referer = page_url
        html_page = resp_page.text
        print('picture page loaded, start parsing image src and name')
        img_node = etree.HTML(html_page).xpath("//div[@class='main-image']/p/a/img")[0]
        img_url = img_node.get('src')
        img_name = img_node.get('src').split('/')[-1]
        print('downloading image:{0}, storing path: {1}\n'.format(img_url, album_path + '/' + img_name))
        try:
            pic_bytes = requests.get(img_url, headers=header, verify=False, timeout=7, proxies=proxies).content
        except requests.exceptions.ConnectionError as e:
            print(page_url + "connection error, " + str(e))
            continue
        except requests.exceptions.ReadTimeout:
            print('readTimeout')
            continue
        with open(album_path + '/' + img_name, 'wb') as img:
            img.write(pic_bytes)
        time.sleep(random.randrange(1, 4))


def download_page_pics(category, category_url, page_index):
    req_url = category_url
    if page_index == 1:
        req_url = category_url
    elif page_index > 1:
        req_url = category_url + 'page/' + str(page_index) + '/'
    print('\n category {0}, url is {1}, current page index{2:d}\n'.format(category, req_url, page_index))
    print('starting fetch page html...\n')
    response = requests.get(req_url, headers=header, verify=False)
    if response.status_code == 200:
        global referer
        referer = req_url
        page_html = response.text
        tree = etree.HTML(page_html)
        nodes = tree.xpath("//ul[@id='pins']/li")
        for node in nodes:
            src = node.find('a').get('href')
            alt = node.find('a').find('img').get('alt')
            time = node.findall('span')[-2].text
            album = {
                'src': src,
                'alt': alt,
                'time': time
            }
            album_dir_name = "{0}{1}".format(time, alt)
            print(album_dir_name)
            download_album_pics(category, album)


def download_category_pic(base_url, category):
    print('\n >>>>>>>>>>>Entering category %s' % category)
    if not os.path.isdir(category):
        print('creating category folder:%s' % category)
        os.mkdir(category)
    category_url = base_url + category + '/'
    print(category_url)
    response = requests.get(category_url, headers=header, verify=False)
    if response.status_code == 200:
        global referer
        referer = category_url
        category_html = response.text
        tree = etree.HTML(category_html)
        category_page_count = parse_category_page_count(tree)
        print('>>>>>category:{0} page count: {1:d}'.format(category, category_page_count))
        for i in range(1, category_page_count):
            download_page_pics(category, category_url, i)
    else:
        print("error fetching category " + category)


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    category_suffix = ['xinggan', 'japan', 'taiwan', 'mm']
    for category in category_suffix[3:]:
        download_category_pic(baseUrl, category)


if __name__ == '__main__':
    main()
