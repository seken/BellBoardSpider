# -*- coding: utf-8 -*-
import scrapy

from ..items import TowerdataItem
from ..models import Peal, db_connect, create_tables
from sqlalchemy.orm import sessionmaker

def is_date(p):
    if 'Monday' in p or 'Tuesday' in p or 'Wednesday' in p or 'Thursday' in p or 'Friday' in p or 'Saturday' in p or 'Sunday' in p:
        return True
    return False


class PealsSpider(scrapy.Spider):
    source_id = "PealsSpider1"
    name = "peals"
    allowed_domains = ["www.bb.ringingworld.co.uk", "bb.ringingworld.co.uk"]
    #newest_id = 1175971
    #start_urls = ['http://www.bb.ringingworld.co.uk/view.php?id=%d' % (i+1) for i in range(364181)]

    def start_requests(self):
        engine = db_connect()
        create_tables(engine)
        self.session_factory = sessionmaker(bind=engine)
        self.download_delay = 0.1

        for i in range(1, 110):#2657+1):
            yield scrapy.Request('http://bb.ringingworld.co.uk/list.php?&newest&page={}'.format(i), self.parse_list)

    def parse_list(self, response):
        performances = response.xpath('id("performances")/tr/td/a/@href').extract()
        self.logger.info("Found {} performances".format(len(performances)))
        session = self.session_factory()
        i = 0
        for p in performances:
            previous_peal_entry = session.query(Peal).filter(Peal.original_id == int(p[p.find("=")+1:])).one_or_none()
            # TODO deal with older versions
            if previous_peal_entry == None:
                i+=1
                yield response.follow(p, self.parse)
        self.logger.info("Page yielded {} new performances".format(i))


    def is_conductor(self, ringer):
        for text in ringer.xpath('text()').extract():
            if "(C)" in text:
                return True
        
        return False

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
        item['conductor_known'] = False
        for ringer in ringers:
            conductor = self.is_conductor(ringer)
            if conductor:
                item['conductor_known'] = True
            item['ringers'].append((
                ringer.xpath('span[@class="bell"]/text()').extract()[0],
                ringer.xpath('span[@class="ringer persona"]/text()').extract()[0],
                conductor
            ))

        #item['ringers'] = performance.xpath('//span[@class="ringer persona"]/text()').extract()
        try:
            item['changes'] = int(performance.xpath('//span[@class="changes"]/text()').extract()[0])
        except:
            item['changes'] = 0
        item['name'] = performance.xpath('//span[@class="title"]/text()').extract()[0]
        self.logger.debug("Performance {}".format(item['name']))
        item['footnote'] = '\n'.join(performance.xpath('//div[@class="footnote"]/text()').extract())
        try:
            item['donation'] = performance.xpath('//div[@class="donation"]/text()').extract()[0]
        except:
            pass

        try:
            item['association'] = performance.xpath('//div[@class="association"]/text()').extract()[0]
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
