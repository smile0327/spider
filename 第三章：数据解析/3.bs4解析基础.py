#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
if __name__ == "__main__":
    #将本地的html文档中的数据加载到该对象中
    fp = open('./test.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(fp, 'html.parser')
    # print(soup)
    # print(soup.a) #soup.tagName 返回的是html中第一次出现的tagName标签
    # print(soup.div)
    #find('tagName'):等同于soup.div
    # print(soup.find('div'))  #print(soup.div)
    # class=song的div
    # print(soup.find('div', class_='song'))
    # 所有a标签
    # print(soup.find_all('a'))
    # 选择器 .class class选择器  #id  id选择器
    # print(soup.select('.tang'))
    # > 一个层级  空格  多个层级
    print(soup.select('.tang > ul a')[0]['href'])