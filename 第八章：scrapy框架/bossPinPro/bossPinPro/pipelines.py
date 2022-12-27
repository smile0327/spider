# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class BosspinproPipeline(object):
    def process_item(self, item, spider):
        print(item)
        # 传递给下一个pipeline执行
        return item


class mysqlPipeline(object):
    """
    mysql pipeline
    将爬取到的数据写入数据库
    """

    conn = None
    cursor = None
    # 初始化  只调用一次,初始化数据库连接
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='10.172.246.234',port=3306,user='root',password='bobandata123',db='test',charset='utf8')


    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('insert into boss values ("%s","%s","%s","%s")'%(item['job_company'],item['job_salary'],item['job_education'],item['job_desc']))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        # self.cursor.close()
        self.conn.close()