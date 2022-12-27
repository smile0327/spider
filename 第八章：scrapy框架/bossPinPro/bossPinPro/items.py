# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BosspinproItem(scrapy.Item):
    # define the fields for your item here like:
    job_company = scrapy.Field()
    job_salary = scrapy.Field()
    job_education = scrapy.Field()
    job_desc = scrapy.Field()
    # pass
