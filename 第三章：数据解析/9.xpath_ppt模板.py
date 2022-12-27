# 爬取ppt模板  https://sc.chinaz.com/ppt/free.html
import os

import requests
from lxml import etree

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

    #创建一个文件夹
    if not os.path.exists('./ppt'):
        os.mkdir('./ppt')

    # 第一页 free.html  第n页 free_n.html(n>1)
    url = 'https://sc.chinaz.com/ppt/free.html'
    page_text = requests.get(url=url, headers=headers).text
    # 免费ppt首页
    home_page = etree.HTML(page_text)

    # 获取总页数
    page_size_path = home_page.xpath('//div[@class="new-page-box container"]/a')[-2]
    page_size = page_size_path.xpath('./b/text()')[0]
    print('总页数：' + page_size)
    # 测试 只爬取前3页
    prefix = 'https://sc.chinaz.com/ppt/free'
    for index in range(1, 2):
        if index == 1:
            path = prefix + '.html'
        else:
            path = prefix + '_' + str(index) + '.html'
        page_one = requests.get(url=path, headers=headers).text
        index_page = etree.HTML(page_one)
        # 所有免费模板集合
        ppt_list = index_page.xpath('//div[@class="container clearfix"]/div[5]/div')
        for item in ppt_list:
            href = item.xpath('./div[2]/a/@href')[0]
            # 单个模板地址
            template_index_url = 'https://sc.chinaz.com' + href
            template_index_page = requests.get(url=template_index_url, headers=headers).text
            # 获取标题
            template_page = etree.HTML(template_index_page)
            title = template_page.xpath('//div[@class="title-box clearfix"]/h1/text()')[0] + '.rar'
            # 处理中文编码
            title = title.encode('iso-8859-1').decode('utf8')
            print('开始下载:' + title + '...')
            # 默认用第一个下载地址（可以获取所有地址，随机取一个）
            download_url = template_page.xpath('//div[@class="download-url"]/a[1]/@href')[0]
            # 开始下载
            ppt_data = requests.get(url=download_url, headers=headers).content
            ppt_path = 'ppt/' + title
            with open(ppt_path, 'wb') as fp:
                fp.write(ppt_data)
                print(title + ' 爬取成功!')
