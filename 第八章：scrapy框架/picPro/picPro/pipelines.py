# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter


# class PicproPipeline:
#     def process_item(self, item, spider):
#         return item
from scrapy.pipelines.images import ImagesPipeline


class picPipeline(ImagesPipeline):
    """
    ImagesPipeline:
    只需要将img的src的属性值进行解析，提交到管道，
    管道就会对图片的src进行请求发送获取图片的二进制类型的数据，
    且还会进行持久化存储
    """

    def get_media_requests(self, item, info):
        """
        获取图片地址并发送请求
        :param item:
        :param info:
        :return:
        """
        yield scrapy.Request(item['src'])

    def item_completed(self, results, item, info):
        """
        返回给下一个item，类似 process_item
        :param results:
        :param item:
        :param info:
        :return:
        """
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        """
        指定图片存储路径（图片名），图片存储目录在settings文件中配置 IMAGES_STORE 参数
        :param request:
        :param response:
        :param info:
        :param item:
        :return:
        """
        picName = request.url.split('/')[-1]
        return picName