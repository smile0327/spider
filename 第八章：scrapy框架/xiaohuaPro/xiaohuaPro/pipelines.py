# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class XiaohuaproPipeline(object):

    def open_spider(self,spider):
        print('开始爬虫......')

    def process_item(self, item, spider):
        print('爬取到图片：%s'%item['name'])
        return item

    def close_spider(self,spider):
        print('爬虫结束.......')