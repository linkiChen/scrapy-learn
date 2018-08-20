# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    author_link = scrapy.Field()
    tags = scrapy.Field()
