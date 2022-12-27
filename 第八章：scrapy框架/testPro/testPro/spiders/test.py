import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        div_list = response.xpath('//*[@id="content"]/div/div[2]/div')
        all_data = []
        for div in div_list:
            # xpath返回的是列表，但是列表元素一定是Selector类型的对象 <Selector xpath='./div[1]/a[2]/h2/text()' data='\n12岁龟\n'>
            # extract可以将Selector对象中data参数存储的字符串提取出来
            author = div.xpath('./div[1]/a[2]/h2/text()')[0].extract()
            # 对列表调用extract()
            # 列表调用了extract之后，则表示将列表中每一个Selector对象中data对应的字符串提取了出来,返回还是一个列表
            content = div.xpath('./a[1]/div[1]/span//text()').extract()
            # 讲列表拼接为字符串
            content = ''.join(content)
            dic = {
                'author':author,
                'content':content
            }
            all_data.append(dic)
        return all_data