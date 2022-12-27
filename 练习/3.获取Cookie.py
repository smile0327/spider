# -*- coding: UTF-8 -*-
from urllib import request, parse
from http import cookiejar

import requests


def get_cookie(url):
    """
    利用CookieJar对象实现获取cookie的功能，并存储导变量中
    :return:
    """
    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    response = opener.open(url)
    # 打印cookie信息
    for item in cookie:
        print('Name = %s' % item.name)
        print('Value = %s' % item.value)


def getAndSave_cookie(url):
    """
    获取cookie并保存到文件
    :param url:
    :return:
    """
    # 设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'cookie.txt'
    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookiejar.MozillaCookieJar(filename)
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    response = opener.open(url)
    # 保存cookie到文件
    '''
    ignore_discard: 即使cookies将被丢弃也将它保存下来
    ignore_expires: 如果在该文件中cookies已经存在，则覆盖原文件写入
    '''
    cookie.save(ignore_discard=True, ignore_expires=True)


def load_cookie(url):
    """
    加载文件中的cookie并使用
    :param url:
    :return:
    """
    # 设置保存cookie的文件的文件名,相对路径,也就是同级目录下
    filename = 'cookie.txt'
    # 创建MozillaCookieJar实例对象
    cookie = cookiejar.MozillaCookieJar()
    # 从文件中读取cookie内容到变量
    cookie.load(filename, ignore_discard=True, ignore_expires=True)
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此用opener的open方法打开网页
    response = opener.open(url)
    # 打印信息
    text = response.read().decode('utf-8')
    with open('baidu_index.html', 'w', encoding='utf-8') as f:
        f.write(text)


def get_cookie_by_session(url):
    """
    从session中获取cookie
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4515.159 Safari/537.36'
    }
    # 创建一个session对象
    session = requests.Session()
    # 通过session访问url，访问成功之后cookie就会存储在session对象中
    session.get(url, headers=headers)

    # 1、直接从session中获取到cookie
    cookies = session.cookies
    # dict = cookies.get_dict()
    # print(dict)
    for name, value in cookies.items():
        print(name, value)

    print("------------------------")

    # 2、session中无法直接获取cookie时，从headers中获取
    response = requests.get(url, headers=headers)
    headers = response.headers
    cookie_tuple = headers.get("Set-Cookie").split(";")
    print(type(cookie_tuple), cookie_tuple)
    cookie_dict = {}
    for item in cookie_tuple:
        if item.count(",") >= 1:
            for item1 in item.split(","):
                key1, value1 = item1.split("=")
                cookie_dict[key1] = value1
        else:
            key, value = item.split("=")
            cookie_dict[key] = value
    for item in cookie_dict.items():
        print(item)

if __name__ == '__main__':
    url = 'http://www.baidu.com'
    # get_cookie(url)
    # getAndSave_cookie(url)
    # load_cookie(url)
    get_cookie_by_session(url)