# encoding:utf-8
import requests
from lxml import etree
import sys
import json

print(sys.getdefaultencoding())

baseUrl = 'http://www.qhrd.gov.cn/'
referer = baseUrl
header = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referrer': 'http://www.qhrd.gov.cn/'
}

if __name__ == '__main__':
    response = requests.get(baseUrl, headers=header, verify=False)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        html = response.text
        # print(html)
        tree = etree.HTML(html)
        resultUrl = tree.xpath("/html/body/div[1]/div[2]/ul/li[3]/ul/li/a/@href")
        resultNames = tree.xpath("/html/body/div[1]/div[2]/ul/li[3]/ul/li/a/text()")
        print(len(resultUrl), len(resultNames))
        data = []
        for i in range(0, len(resultNames)):
            item = {'name': resultNames[i], 'url': resultUrl[i]}
            data.append(item)
        print(json.dumps(data, ensure_ascii=False))
        print(len(data))
