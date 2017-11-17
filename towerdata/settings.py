# -*- coding: utf-8 -*-

# Scrapy settings for towerdata project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'towerdata'

SPIDER_MODULES = ['towerdata.spiders']
ITEM_PIPELINES = {
        'towerdata.pipelines.TowerdataPipeline': 500
}
NEWSPIDER_MODULE = 'towerdata.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'towerdata (+https://github.com/seken/BellBoardSpider)'

DOWNLOAD_DELAY = 0.1

DATABASE = {
    'drivername': 'sqlite',
    'database': 'content.db'
}
