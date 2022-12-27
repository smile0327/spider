# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MovieproPipeline:
    def process_item(self, item, spider):
        if item.__class__.__name__ == 'MovieproItem':
            print(item['movie_name'], item['movie_type'],item['movie_area'],item['movie_duration'],item['movie_score'])
        else:
            print(item['movie_name'], item['moive_desc'])
        return item

