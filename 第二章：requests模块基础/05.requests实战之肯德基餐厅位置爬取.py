#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import json

import requests

if __name__ == "__main__":
    # 1. url  http://www.kfc.com.cn/kfccda/index.aspx
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    # 2.进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    # 3. post请求  组装参数
    keyword = '武汉'
    data = {
        'cname':'',
        'pid':'',
        'keyword': keyword,
        'pageIndex': 1,
        'pageSize': 5
    }
    # 4.发送该请求
    rs = requests.post(url, data=data, headers=headers)
    # 拿到返回结果处理
    res_obj = rs.json()
    print(res_obj)
    fp = open('./kfc.json', 'w', encoding='utf-8')
    json.dump(res_obj, fp=fp, ensure_ascii=False)
