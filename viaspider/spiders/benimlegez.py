# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from viaspider.items import ViaspiderItem
from viaspider.settings import SUMMARY_LIMIT
from w3lib.html import remove_tags


class BenimlegezSpider(CrawlSpider):
    name = "benimlegez"
    allowed_domains = ["www.benimlegez.com"]
    start_urls = ['http://www.benimlegez.com/']

    rules = [
        Rule(
            LinkExtractor(allow = [
                '/category/\w*',
                '/category/\w*/page/\d*'
            ], deny = [
                '/category/duyuru/',
                '/category/video/'
            ]),
            callback='parse_item',
            follow=True
        )    
    ]

    def parse_item(self, response):
        urls = response.xpath('//h2[@itemprop="name"]/a/@href')
        
        for url in urls:
            yield Request(url.extract(), callback=self.parse_post)

    def parse_post(self, response):
        item = ViaspiderItem()
        item['url'] = response.url
        item['source'] = 'benimlegez.com'
        item['title'] = self.get_title(response)
        item['summary'] = self.get_summary(response)
        item['categories'] = self.get_categories(response)
        item['tags'] = self.get_tags(response)
        item['image'] = self.get_image(response)
        item['created'] = self.get_created(response)
        return item
        
    def get_title(self, response):
        title = response.xpath('//head/title/text()').extract()[0].encode('utf-8')
        return title[:-13] if title.endswith(' - BenimleGez') else title
        
    def get_summary(self, response):
        summary = response.xpath('//head/meta[@property="og:description"]/@content').extract()[0]
        return summary[:-SUMMARY_LIMIT] if len(summary) > SUMMARY_LIMIT else summary
        
    def get_categories(self, response):
        categories = response.xpath('//head/meta[@property="article:section"]/@content').extract()[0]
        return categories
        
    def get_tags(self, response):
        tags = response.xpath('//head/meta[@property="article:tag"]/@content').extract()
        return tags
        
    def get_image(self, response):
        image = response.xpath('//head/meta[@property="og:image"]/@content').extract()[0]
        return image
        
    def get_created(self, response):
        created = response.xpath('//head/meta[@property="article:published_time"]/@content').extract()[0]
        return created