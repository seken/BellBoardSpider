# -*- coding: utf-8 -*-
import scrapy

from towerdata.items import TowerdataItem

def is_date(p):
    if 'Monday' in p or 'Tuesday' in p or 'Wednesday' in p or 'Thursday' in p or 'Friday' in p or 'Saturday' in p or 'Sunday' in p:
        return True
    return False

class PealsSpider(scrapy.Spider):
    name = "peals"
    allowed_domains = ["www.bb.ringingworld.co.uk"]
    start_urls = ['http://www.bb.ringingworld.co.uk/view.php?id=%d' % (i+1) for i in range(364181)]

    def parse(self, response):
        item = TowerdataItem()
        performance = response.xpath('//div[@id="perf-wrapper"]')[0]
        try:
            item['address'] = performance.xpath('*/div[@class="address"]/text()').extract()[0]
        except:
            pass
        item['ringers'] = performance.xpath('//span[@class="ringer persona"]/text()').extract()
        item['changes'] = int(performance.xpath('//span[@class="changes"]/text()').extract()[0])
        item['name'] = performance.xpath('//span[@class="title"]/text()').extract()[0]
        item['footnote'] = '\n'.join(performance.xpath('//div[@class="footnote"]/text()').extract())
        try:
            item['donation'] = performance.xpath('//div[@class="donation"]/text()').extract()[0]
        except:
            pass

        try:
            item['assocation'] = performance.xpath('//div[@class="association"]/text()').extract()[0]
        except:
            pass

        try:
            item['place'] = performance.xpath('//span[@class="place"]/text()').extract()[0]
        except:
            pass

        for potential_date in response.xpath('//div[@class="performance"]/div/text()').extract():
            if is_date(potential_date):
                item['date'] = potential_date
                break

        yield item
