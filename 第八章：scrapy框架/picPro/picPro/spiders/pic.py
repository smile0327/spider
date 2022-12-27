import scrapy

from picPro.items import PicproItem

class PicSpider(scrapy.Spider):
    """
    爬取 https://pic.netbian.com/4kmeinv/ 的图片
    """
    name = 'pic'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://pic.netbian.com/4kmeinv/']

    # 分页的url
    url = 'https://pic.netbian.com/4kmeinv/index_%d.html'
    page_num = 2

    def parse(self, response):
        li_list = response.xpath('//*[@id="main"]/div[3]/ul/li')
        for li in li_list:
            src = 'https://pic.netbian.com/' + li.xpath('./a/img/@src').extract_first()
            item = PicproItem()
            item['src'] = src
            # 提交给管道
            yield item

        # 爬取分页数据
        if self.page_num <= 3:
            page_url = format(self.url%self.page_num)
            self.page_num += 1
            yield scrapy.Request(page_url, callback=self.parse)