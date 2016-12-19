# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from viaspider.items import ItemParser


class BizEvdeYokuzSpider(CrawlSpider):
    name = "bizevdeyokuz"
    allowed_domains = ["bizevdeyokuz.com"]
    start_urls = ['http://bizevdeyokuz.com/']

    rules = [
        Rule(
            LinkExtractor(allow = [
                '/turkiye/$',
                '/turkiye/page/\d*',
                '/yurt-disi/$',
                '/yurt-disi/page/\d*',
                '/seyahat/$',
                '/seyahat/page/\d*',
                '/evde-yoklar/$',
                '/evde-yoklar/page/\d*'
            ]),
            callback='parse_item',
            follow=True
        )    
    ]

    def parse_item(self, response):
        urls = response.xpath('//h2[@class="cb-post-title"]/a/@href')
        
        for url in urls:
            yield Request(url.extract(), callback=self.parse_post)

    def parse_post(self, response):
        item = ItemParser('bizevdeyokuz.com', response, '|', "Biz Evde Yokuz")
        return item.parse()
