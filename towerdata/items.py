# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TowerdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    association = scrapy.Field()
    place = scrapy.Field()
    address = scrapy.Field()
    changes = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    footnote = scrapy.Field()
    donation = scrapy.Field()
    ringers = scrapy.Field()
