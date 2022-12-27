#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
from lxml import etree
#需求：爬取58二手房中的房源信息
if __name__ == "__main__":
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    #爬取到页面源码数据
    url = 'https://bj.58.com/ershoufang/'
    page_text = requests.get(url=url,headers=headers).text

    #数据解析
    tree = etree.HTML(page_text)
    #存储的就是div
    div_list = tree.xpath('//div[@class="property-content-title"]')
    fp = open('58.txt', 'w', encoding='utf-8')
    for div in div_list:
        #局部解析  ./标识当前定位到的标签
        title = div.xpath('./h3/text()')[0]
        print(title)
        fp.write(title+'\n')
    fp.close()
