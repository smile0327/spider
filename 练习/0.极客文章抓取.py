import re
import os
import time

import requests
from bs4 import BeautifulSoup
from lxml import etree
import pdfkit

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}


class JKBodySpider(object):
    """
    爬取正文内容
    """

    def __init__(self, url):
        self.url = url
        self.fileName = url.split("/")[-1]

    def dir_path(self):
        split = self.url.split("/")
        file_dir = split[-2]
        return file_dir

    def request_url(self):
        """
        请求url
        """
        # text会乱码，以字节流方式返回使用utf-8编码
        page_html = requests.get(url=self.url, headers=headers).content.decode("utf-8")
        return page_html

    def parse_html(self, page_html):
        """
        解析html
        使用xpath解析
        :param page_html:
        :return:
        """
        tree = etree.HTML(page_html)
        text_list = tree.xpath('/html/body/div/div[3]/div/div/div[2]/div[1]/div//text()')
        return text_list

    def parse_html_bs4(self, page_html):
        """
        使用bs4进行解析，获取整个正文部分并保存为html
        :param page_html:
        :return:
        """

        soup = BeautifulSoup(page_html, "html.parser")
        # 通过class标签定位
        # 文章正文 : class_='book-post'  获取文章正文时html页面与原始页面排版有差异
        book_content = soup.find('div', class_='book-post')

        content_html = str(book_content)
        self.exists_and_create(self.dir_path())
        # 默认写入的是gbk编码
        with open(self.dir_path() + "/" + self.fileName + ".html", "w", encoding='utf-8') as fp:
            fp.write(content_html)
        return content_html

    def save_image(self, page_html):
        """
        下载页面中的图片保存的本地，否则生成本地html或者pdf时图片无法显示
        通过正则匹配img标签，并提取文件名
        :param page_html: 原始页面
        :return:
        """
        ex = '.*?<img alt.*? src="(.*?)"'
        # re.S 单行匹配  re.M 多行匹配
        img_src_list = re.findall(ex, page_html, re.S)
        # url截取 从开始到最后一个/  find返回第一个位置，rfind返回最后一个位置  [0:5]截取字符串，从头开始截取可省略开始下标
        last_index = self.url.rfind("/")
        short_url = self.url[:last_index]
        for src in img_src_list:
            dir = src.split("/")[0]
            self.exists_and_create(self.dir_path() + "/" + dir)
            img_url = short_url + "/" + src
            img_data = requests.get(url=img_url, headers=headers).content
            with open(self.dir_path() + "/" + src, 'wb') as fp:
                fp.write(img_data)
                print(src, '下载成功！！！')

    def exists_and_create(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)
            print(dir, "目录不存在,直接创建")

    def save_pdf(self, html, fileName):
        """
        将所有html转换为pdf
        windows需要安装 wkhtmltopdf，并配置环境将执行路径加入到系统环境 $PATH 变量中
        该方法执行比较慢，应该改为异步生成pdf文件
        from_file : 将本地html文件生成pdf
        form_string : 将下载的网页数据生成pdf
        :param html: html列表
        :param fileName:  pdf生成文件名
        :return:
        """
        options = {
            'page-size': 'Letter',
            'encoding': "UTF-8",
            'enable-local-file-access': None,
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ]
        }
        pdfkit.from_file(html, fileName, options=options)

    def save(self, text_list):
        """
        保存结果
        :param text_list:
        :return:
        """
        with open('./' + self.fileName, 'w', encoding='utf-8') as fp:
            for text in text_list:
                fp.write(text)

    def run(self):
        html = self.request_url()

        # xpath 解析正文内容并保存
        # parse_text = self.parse_html(page_html=html)
        # self.save(text_list=parse_text)

        # bs4解析正文内容，并保存为pdf 可以通过parse_text生成pdf，也可以通过本地html文件生成pdf
        parse_text = self.parse_html_bs4(html)
        self.save_image(parse_text)

        split = self.url.split("/")
        file_dir = split[-2]
        pdf_file_name = file_dir + '/' + split[-1].replace('md', 'pdf')
        html_file_name = file_dir + '/' + split[-1] + '.html'
        print('开始生成pdf文件:', pdf_file_name)
        self.save_pdf(html_file_name, pdf_file_name)
        print('生成pdf文件完成:', pdf_file_name)


class JKCatalogSpider(object):
    """
    爬取专栏标题
    """

    def __init__(self, url):
        self.url = url

    def __request_url(self):
        """
        请求url,获取页面数据
        :return:
        """
        page_html = requests.get(url=self.url, headers=headers).content.decode("utf-8")
        with open("./zhuanlan.html", "w", encoding='utf-8') as fp:
            fp.write(page_html)
        return page_html

    def __parse_catalog(self, page_html):
        """
        从返回的页面中解析出目录，分为以及目录和二级目录
        :param page_html:
        :return:
        """
        # 解析爬取的网页
        tree = etree.HTML(page_html)

        # 解析本地文件
        # parser = etree.HTMLParser(encoding='utf-8')
        # tree = etree.parse("zhuanlan.html", parser=parser)

        title_xpath = '/html/body/div/div[3]/div/div/div[2]/div[1]/div/ul/li/a/text()'
        title_li_list = tree.xpath(title_xpath)
        res = {}
        # xpath中下标从1开始计数
        for i in range(len(title_li_list)):
            title = title_li_list[i]
            catalog_xpath = '/html/body/div/div[3]/div/div/div[2]/div[1]/div/ul/ul[' + str(i + 1) + ']/li/a/@href'
            catalog_li_list = tree.xpath(catalog_xpath)
            res[title] = catalog_li_list
        return res

    def run(self):
        page_html = self.__request_url()
        res = self.__parse_catalog(page_html)
        return res


if __name__ == '__main__':
    # url = 'http://learn.lianglianglee.com/专栏/12步通关求职面试-完/00 开篇词：了解面试“潜规则”，从海选中脱颖而出.md'
    # jk_spider = JKBodySpider(url)
    # jk_spider.run()

    # 爬取专栏下所有数据
    base_url = 'http://learn.lianglianglee.com'

    zl_url = base_url + '/专栏'
    cs = JKCatalogSpider(zl_url)
    title_catalog_dict = cs.run()
    for title, cl_list in title_catalog_dict.items():
        # TODO 爬取完成后保存 标题和完整目录，下次重启任务时根据 标题和目录过滤，只爬取未下载的（增量爬虫）
        print(title)
        for catalog in cl_list:
            try:
                body_url = base_url + catalog
                print('\t' + body_url)
                # 开始下载正文，合理的方案应该是多线程异步下载（主要是生成pdf比较慢）,或者只下载网页数据，最后通过离线批量生成pdf
                jk_spider = JKBodySpider(body_url)
                jk_spider.run()
            except Exception as e:
                pass
