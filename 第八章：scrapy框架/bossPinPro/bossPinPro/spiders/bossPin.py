import time

import scrapy

from bossPinPro.items import BosspinproItem

from selenium.webdriver import ChromeOptions
from selenium import webdriver
#实现无可视化界面
from selenium.webdriver.chrome.options import Options



class BosspinSpider(scrapy.Spider):
    """
    武汉python招聘信息  爬取boss直聘 公司名称  / 薪资范围 / 职位描述
    页面是动态数据加载，所以结合selenium爬取数据；在DownloaderMiddleware中使用selenium爬取数据
    """
    name = 'bossPin'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=python&city=101200100&industry=&position=']

    # 分页爬取的通用url
    url = 'https://www.zhipin.com/c101200100/?query=python&page=%d'
    page_num = 2

    # 实现规避检测 （浏览器认为是selenium登录，在验证阶段无法通过）
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 实现无可视化界面的操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # 设置UA代理，否则无头浏览器无法获取到数据
    chrome_options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"')

    def __init__(self):
        """
        实例化一个浏览器对象
        """
        self.bro = webdriver.Chrome(executable_path='./chromedriver', options=self.option, chrome_options=self.chrome_options)

    def parse_detail(self, response):
        # 回调函数中获取传入的item对象
        item = response.meta['item']
        # 返回列表
        job_desc = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div//text()').extract()
        job_desc = ''.join(job_desc).strip()
        item['job_desc'] = job_desc
        # 将item传递给pipeline
        yield item

    def parse(self, response):
        # 通过scrapy爬取不到数据 结合selenium
        li_list = response.xpath('//*[@id="main"]/div/div[3]/ul/li')
        cnt = 0
        for li in li_list:
            # 只爬取前5条数据退出（测试  多次请求会被boss封ip,需要设置代理）
            cnt += 1
            if cnt == 6:
                break
            job_company = li.xpath('.//div/div[1]/div[2]/div/h3/a/text()').extract_first()
            job_salary = li.xpath('.//div/div[1]/div[1]/div/div[2]/span/text()').extract_first()
            job_education = li.xpath('.//div/div[1]/div[1]/div/div[2]/p//text()').extract()
            job_education = ''.join(job_education).strip()

            job_detail_url = 'https://www.zhipin.com' + li.xpath('.//div/div[1]/div[1]/div/div[1]/span[1]/a/@href').extract_first()
            item = BosspinproItem()
            item['job_company'] = job_company
            item['job_salary'] = job_salary
            item['job_education'] = job_education

            # 手动发送请求获取详情页数据 通过回调函数parse_detail来解析详情页数据
            # 请求传参：meta={}，可以将meta字典传递给请求对应的回调函数
            yield scrapy.Request(job_detail_url,callback=self.parse_detail,meta={'item':item})

        # 爬取其他分页数据 只爬取前3页数据
        # if self.page_num <= 3:
        #     new_url = format(self.url%self.page_num)
        #     self.page_num +=1
        #     yield scrapy.Request(new_url, callback=self.parse)


    def close(self, spider):
        """
        关闭浏览器
        :param spider:
        :return:
        """
        self.bro.quit()

