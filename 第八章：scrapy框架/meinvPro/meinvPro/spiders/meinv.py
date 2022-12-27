import scrapy

from scrapy.spiders import Rule
from scrapy.spiders.crawl import LinkExtractor, CrawlSpider


class MeinvSpider(CrawlSpider):
    name = 'meinv'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.meinv.hk/?cat=2']

    # 增加提取 a 标签的href连接的规则
    # 将提取到的href连接，生成新的Request 请求， 同时指定新的请求后解析函数
    rules = (
        # allow 默认使用正则的表达式，查找所有a标签的href
        # follow 为True时，表示在提取规则连接下载完成后，是否再次提取规则中连接;False表示只提取当前页的数据
        Rule(LinkExtractor(allow=r'p=\d+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = {}
        info = response.xpath('//div[@class="wshop wshop-layzeload"]/text()').extract_first()
        try:
            item['hometown'] = info.split("/")[2].strip().split()[1]
            item['birthday'] = info.split("/")[1].strip().split()[1]
        except:
            item['birthday'] = "未知"
            item['hometown'] = "未知"
        item['name'] = response.xpath('//h1[@class="title"]/text()').extract_first()
        images = response.xpath('//div[@class="post-content"]//img/@src')
        try:
            item['image_urls'] = images.extract()
        except:
            item['image_urls'] = ''
        item['images'] = ''
        item['detail_url'] = response.url
        yield item
