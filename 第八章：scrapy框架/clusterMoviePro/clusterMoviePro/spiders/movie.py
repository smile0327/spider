import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from scrapy_redis.spiders import RedisCrawlSpider

from clusterMoviePro.items import ClustermovieproItem


class MovieSpider(RedisCrawlSpider):
    """
    分布式爬虫
    1、爬虫类继承 RedisCrawlSpider 类
    2、分布式爬虫这里不用指定start_urls,新增一个redis_key属性,代表可以
       被共享的调度器队列的名称，启动后将起始url push到该队列中即可
    3、编写数据解析相关操作
    4、在settings配置中需要指定 被共享的pipeline和调度器（来源于scrapy_redis中）
    """
    name = 'movie'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['https://ssr1.scrape.center/']

    redis_key = 'movie'

    rules = (
        Rule(LinkExtractor(allow=r'/page/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
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

            item = ClustermovieproItem()
            item['movie_name'] = movie_name.strip()
            item['movie_type'] = movie_type.strip()
            item['movie_area'] = movie_area.strip()
            item['movie_duration'] = movie_duration.strip()
            item['movie_score'] = movie_score.strip()
            yield item
