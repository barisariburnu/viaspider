# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from viaspider.items import ItemParser


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
        item = ItemParser('benimlegez.com', response, '-', 'BenimleGez')
        return item.parse()
