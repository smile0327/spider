# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from lxml import etree
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse


class BosspinproDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        下载器中间件
        引擎将请求通过下载器中间件 Downloader Middlewares 发送给下载器
        :param request:
        :param spider:
        :return:
        """
        # Called for each request that goes through the downloader
        # middleware.
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        """
        拦截所有响应请求，进行篡改
        下载器下载完毕后生成一个页面的Response，通过该方法发送给引擎
        :param request:
        :param response:
        :param spider:
        :return:
        """
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        # 获取在爬虫类中定义的浏览器对象
        bro = spider.bro
        bro.get(request.url)
        time.sleep(2)
        # 通过selenium 获取的网页数据  bro.page_source
        html = bro.page_source

        # 返回数据
        return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')

    def process_exception(self, request, exception, spider):
        """
        拦截发生异常的请求
        :param request:
        :param exception:
        :param spider:
        :return:
        """
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
