# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from viaspider.settings import SUMMARY_LIMIT


class ViaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    categories = scrapy.Field()
    tags = scrapy.Field()
    image = scrapy.Field()
    source = scrapy.Field()
    created = scrapy.Field()


class ItemParser(object):
    def __init__(self, source, response, seperator, bloginfo):
        self.source = source
        self.response = response
        self.seperator = seperator
        self.bloginfo = " " + self.seperator + " " + bloginfo
        
    @property
    def url(self):
        return self.response.url
        
    @property
    def title(self):
        result = self.response.xpath('//head/title/text()').extract()[0].encode('utf-8')
        if result.endswith(self.bloginfo):
            return (self.seperator.join(result.split(self.seperator)[:-1])).strip() 
        else:
            return result
    
    @property
    def summary(self):
        result = self.response.xpath('//head/meta[@property="og:description"]/@content').extract()[0]
        return result[:-(SUMMARY_LIMIT + 3)] + '...' if len(result) > SUMMARY_LIMIT else result
    
    @property
    def categories(self):
        results = self.response.xpath('//head/meta[@property="article:section"]/@content').extract()
        return results
    
    @property
    def tags(self):
        results = self.response.xpath('//head/meta[@property="article:tag"]/@content').extract()
        return results if len(results) > 0 else self.categories
     
    @property  
    def image(self):
        result = self.response.xpath('//head/meta[@property="og:image"]/@content').extract()[0]
        return result
     
    @property   
    def created(self):
        result = self.response.xpath('//head/meta[@property="article:published_time"]/@content').extract()[0]
        return result
        
    def parse(self):
        item = ViaspiderItem()
        item['url'] = self.url
        item['source'] = self.source
        item['title'] = self.title
        item['summary'] = self.summary
        item['categories'] = self.categories
        item['tags'] = self.tags
        item['image'] = self.image
        item['created'] = self.created
        return item