# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from scrapy import log

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ViaspiderPipeline(object):
    def __init__(self):
         self.post_seen = set()
         
    def process_item(self, item, spider):
        if item['url'] in self.post_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.post_seen.add(item['url'])
            return item  
