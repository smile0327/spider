import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver

from qczjPro.items import QczjproItem


class QczjimageSpider(scrapy.Spider):
    name = 'qczjImage'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        'https://club.autohome.com.cn/frontapi/data/page/club_get_topics_list_by_contenttype?page_num=1&page_size=20&club_content_type=138&search_after=&club_bbs_id=0&apitype=more']

    # 实例化一个浏览器对象
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.bro = webdriver.Chrome(executable_path='./chromedriver')

    def parse(self, response):
        """
        解析出每个论坛的url
        :param response:
        :return:
        """
        text = response.xpath('/html/body/pre/text()').extract_first()
        data = json.loads(text)
        items = data['result']['items']

        # for item in items:
        #     pc_url = item['pc_url']
        #     print(pc_url)
        # 只测试第一个地址
        pc_url = items[0]['pc_url']

        yield scrapy.Request(url=pc_url, callback=self.parse_detail)

    def parse_detail(self, response):
        # text = response.text
        # with open('./qczj.html', 'w',encoding='utf-8') as f:
        #     f.write(text)
        """
        获取论坛里面的图片信息
        :param response:
        :return:
        """
        # contains(@class,'tx')  获取所有class属性为tx的所有标签
        div_list = response.xpath('/html/body/section[4]/div/div[2]/div/div[5]//div[contains(@class,"tz-picture")]')
        print("图片数量：" + str(len(div_list)))
        for div in div_list:
            url = div.xpath("./img/@data-src").extract_first()
            if url is None:
                url = div.xpath("./img/@src").extract_first()
                item = QczjproItem()
                item['src'] = url
                yield item

    def closed(self, spider):
        self.bro.quit()
