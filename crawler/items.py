# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    lx = scrapy.Field()
    bt = scrapy.Field()
    hds = scrapy.Field()
    time = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    dq = scrapy.Field()
