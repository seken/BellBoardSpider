# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .models import Peal, Ringer, Performance, db_connect, create_tables

class TowerdataPipeline(object):

    def process_item(self, item, spider):
        session = spider.session_factory()

        previous_peal_entry = session.query(Peal).filter(Peal.original_url == item['original_url']).one_or_none()
        if previous_peal_entry != None:
            pass
            # TODO deal with older versions Check and overwrite
        else:
            self.new_peal(session, item)

        return item

    def new_peal(self, session, item):
        peal = Peal()
        if 'association' in item:
            peal.association = item['association']
        if 'place' in item:
            peal.place = item['place']
        if 'address' in item:
            peal.address = item['address']
        peal.changes = item['changes']
        peal.name = item['name']
        peal.date = item['date']
        peal.footnote = item['footnote']
        if 'donation' in item:
            peal.donation = item['donation']
        for bell, ringer_name, conductor in item['ringers']:
            ringer = session.query(Ringer).filter(Ringer.name==ringer_name).one_or_none()
            performance = Performance()
            performance.peal = peal
            performance.bell = bell
            if item['conductor_known']:
                performance.conductor = conductor
            if ringer != None:
                performance.ringer = ringer
            else:
                performance.ringer = Ringer(name=ringer_name)
                session.add(performance.ringer)
            session.add(performance)
        peal.page_data = ''.join(item['page_data'])
        peal.spider_source = item['spider_source']
        peal.original_url = item['original_url']
        peal.conductor_known = item['conductor_known']
        peal.original_id = int(item['original_url'][item['original_url'].find("=")+1:])

        session.add(peal)

        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
