# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    stock_symbol = scrapy.Field()

