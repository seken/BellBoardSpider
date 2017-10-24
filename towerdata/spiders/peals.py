# -*- coding: utf-8 -*-
import scrapy

from ..items import TowerdataItem

def is_date(p):
    if 'Monday' in p or 'Tuesday' in p or 'Wednesday' in p or 'Thursday' in p or 'Friday' in p or 'Saturday' in p or 'Sunday' in p:
        return True
    return False

def is_conductor(ringer):
    for text in ringer.extract('/text()').extract():
        if "(C)" in text:
            return True
    
    return False

class PealsSpider(scrapy.Spider):
    source_id = "PealsSpider1"
    name = "peals"
    allowed_domains = ["www.bb.ringingworld.co.uk"]
    #newest_id = 1175971
    #start_urls = ['http://www.bb.ringingworld.co.uk/view.php?id=%d' % (i+1) for i in range(364181)]

    def start_requests(self):
        for i in range(1, 2657+1):
            yield scrapy.Request('http://bb.ringingworld.co.uk/list.php?&newest&page={}'.format(i), self.parse_list)

    def parse_list(self, response):
        performances = response.xpath('id("performances")/tr/td/a/@href').extract()
        self.logger.info("Found {} performances".format(len(performances)))
        for p in performances:
            # TODO these get filtered
            yield response.follow(p, self.parse)

    def parse(self, response):
        item = TowerdataItem()
        performance = None
        try:
            performance = response.xpath('//div[@id="perf-wrapper"]')[0]
            item['address'] = performance.xpath('*/div[@class="address"]/text()').extract()[0]
        except:
            pass
        item['ringers'] = []
        ringers = response.xpath('//div[@class="performance"]/div[@class="ringers"]/div')
        for ringer in ringers:
            ringer.append((
                ringer.xpath('//span[@class="bell"]/text()').extract()[0],
                ringer.xpath('//span[@class="ringer persona"]/text()').extract()[0],
                is_conductor(ringer)#
            ))

        item['ringers'] = performance.xpath('//span[@class="ringer persona"]/text()').extract()
        item['changes'] = int(performance.xpath('//span[@class="changes"]/text()').extract()[0])
        item['name'] = performance.xpath('//span[@class="title"]/text()').extract()[0]
        self.logger.debug("Performance {}".format(item['name']))
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

        item['page_data'] = response.xpath('//td[@id="page-content"]/node()').extract()
        item['spider_source'] = self.source_id
        item['original_url'] = response.url

        yield item
