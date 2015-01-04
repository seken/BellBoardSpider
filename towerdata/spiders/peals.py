# -*- coding: utf-8 -*-
import scrapy


class PealsSpider(scrapy.Spider):
    name = "peals"
    allowed_domains = ["http://www.bb.ringingworld.co.uk/"]
    start_urls = (
        'http://www.http://www.bb.ringingworld.co.uk//',
    )

    def parse(self, response):
        pass
