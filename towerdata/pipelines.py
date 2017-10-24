# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .models import Peal, Ringer, db_connect, create_tables
from sqlalchemy.orm import sessionmaker

class TowerdataPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_tables()
        self.session_factory = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.session_factory()

        peal = Peals()
        peal.association = item.association
        peal.place = item.place
        peal.address = item.address
        peal.changes = item.changes
        peal.name = item.name
        peal.date = item.date
        peal.footnote = item.footnote
        peal.donation = item.donation
        for r in item.ringers:
            ringer = session.query(Ringer).filter(Ringer.name==r).first()
            if ringer == None:
                ringer = Ringer(name=r)
            peal.ringers.append(ringer)
        peal.page_data = item.page_data
        peal.spider_source = item.spider_source
        peal.original_url = item.original_url

        try:
            session.add(peal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
