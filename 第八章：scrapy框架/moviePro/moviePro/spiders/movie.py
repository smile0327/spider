import time

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from moviePro.items import MovieproItem, MovieDescItem


class MovieSpider(CrawlSpider):
    """
    爬取所有电影 名称、评分、地区、类型、剧情简介
    """
    name = 'movie'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://ssr1.scrape.center/']
    # 分页提取
    link_page = LinkExtractor(allow=r'/page/\d+')
    # 详情提取
    link_detail = LinkExtractor(allow=r'/detail/\d+')

    rules = (
        Rule(link_page, callback='parse_item', follow=True),
        Rule(link_detail, callback='parse_detail'),
    )

    def parse_item(self, response):
        print(response.url)
        # 解析电影 名称、评分、地区、类型
        div_list = response.xpath('//*[@id="index"]/div[1]/div[1]/div')
        for div in div_list:
            movie_name = div.xpath('./div/div/div[2]/a/h2/text()').extract_first()
            movie_type = div.xpath('./div/div/div[2]/div[1]//text()').extract()
            movie_area = div.xpath('./div/div/div[2]/div[2]/span[1]/text()').extract_first()
            movie_duration = div.xpath('./div/div/div[2]/div[2]/span[3]/text()').extract_first()
            movie_score = div.xpath('./div/div/div[3]/p[1]/text()').extract_first()

            movie_type = [type.strip() for type in movie_type if len(type.strip()) > 0]
            movie_type = "/".join(movie_type)

            item = MovieproItem()
            item['movie_name'] = movie_name.strip()
            item['movie_type'] = movie_type.strip()
            item['movie_area'] = movie_area.strip()
            item['movie_duration'] = movie_duration.strip()
            item['movie_score'] = movie_score.strip()
            print(item['movie_name'], item['movie_type'],item['movie_area'],item['movie_duration'],item['movie_score'])
            yield item


    def parse_detail(self, response):
        movie_name = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/a/h2/text()').extract_first()
        movie_desc = response.xpath('//*[@id="detail"]/div[1]/div/div/div[1]/div/div[2]/div[4]/p/text()').extract_first()
        item = MovieDescItem()
        item['movie_name'] = movie_name
        item['movie_desc'] = movie_desc
        yield item