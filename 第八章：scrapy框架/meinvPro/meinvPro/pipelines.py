# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os
from hashlib import sha1

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from meinvPro import settings


class MeinvImagePipeline(ImagesPipeline):

    # 根据图片地址进行图片数据的请求
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            yield Request(url, meta={'name': item['name']})

    # 下载完成后调用的方法
    def item_completed(self, results, item, info):
        #将下载完成后的图片路径设置到item中
        item['images'] = [x for ok, x in results if ok]
        return item

    # 指定图片的存储路径
    def file_path(self, request, response=None, info=None):
        # 为每位人员创建一个目录，存放她自己所有的图片
        author_name = request.meta['name']
        author_dir = os.path.join(settings.IMAGES_STORE, author_name)
        if not os.path.exists(author_dir):
            os.makedirs(author_dir)
        #从连接中提取文件名和扩展名
        try:
            filename = request.url.split("/")[-1].split(".")[0]
        except:
            filename = sha1(request.url.encode(encoding='utf-8')).hexdigest()
        try:
            ext_name = request.url.split(".")[-1]
        except:
            ext_name = 'jpg'

        # 返回的相对路径
        return '%s/%s.%s' % (author_name, filename, ext_name)


class MeinvPipeline(object):
    def __init__(self):
        self.csv_filename = 'meinv.csv'
        self.existed_header = False
    def process_item(self, item, spider):
        # item dict对象，是spider.detail_parse() yield{}输出模块
        with open(self.csv_filename, 'a', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=(
                'name', 'hometown', 'birthday', 'detail_url'))
            if not self.existed_header:
                # 如果文件不存在，则表示第一次写入
                writer.writeheader()
                self.existed_header = True
            image_urls = ''
            for image_url in item['image_urls']:
                image_urls += image_url + ','
            image_urls.strip("\"").strip("\'")
            data = {
                'name': item['name'].strip(),
                'hometown': item['hometown'],
                'birthday': item['birthday'].replace('年', '-').replace('月', '-').replace('日', ''),
                'detail_url': item['detail_url'],
            }
            writer.writerow(data)
            f.close()
        return item