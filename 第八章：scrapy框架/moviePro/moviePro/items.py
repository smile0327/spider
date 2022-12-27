# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieproItem(scrapy.Item):
    # define the fields for your item here like:
    movie_name = scrapy.Field()
    movie_score = scrapy.Field()
    movie_area = scrapy.Field()
    movie_type = scrapy.Field()
    movie_duration = scrapy.Field()

class MovieDescItem(scrapy.Item):
    movie_name = scrapy.Field()
    movie_desc = scrapy.Field()