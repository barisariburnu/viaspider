# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from viaspider.items import ItemParser


class DrummerlizardSpider(CrawlSpider):
    name = "drummerlizard"
    allowed_domains = ["drummerlizard.com"]
    start_urls = ['http://drummerlizard.com/']
    
    rules = [
        Rule(
            LinkExtractor(allow = [
                '/gezi-rehberi/$',
                '/gezi-rehberi/page/\d*',
                '/dogada-seyahat/$',
                '/dogada-seyahat/page/\d*',
                '/seyahat-ipuclari/$',
                '/seyahat-ipuclari/page/\d*',
                '/seyir-defteri/$',
                '/seyir-defteri/page/\d*'
            ], deny = [
                '/guncel/$',
                '/guncel/page/\d*'
            ]),
            callback='parse_item',
            follow=True
        )    
    ]

    def parse_item(self, response):
        urls = response.xpath('//article/h2[@class="post-box-title"]/a/@href')
        
        for url in urls:
            yield Request(url.extract(), callback=self.parse_post)

    def parse_post(self, response):
        item = ItemParser('drummerlizard.com', response, '|', 'Adım Adım Seyahat')
        return item.parse()
