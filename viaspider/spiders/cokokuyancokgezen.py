# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from viaspider.items import ItemParser


class CokOkuyanCokGezenSpider(CrawlSpider):
    name = "cokokuyancokgezen"
    allowed_domains = ["cokokuyancokgezen.com"]
    start_urls = ['http://cokokuyancokgezen.com']
    
    rules = [
        Rule(
            LinkExtractor(allow = [
                '/geziler/\w*', 
                '/geziler/\w*/page/\d*',
                '/gezi-tuyolari/\w*',
                '/gezi-tuyolari/\w*/page/\d*',
                '/istanbul-gezileri/\w*',
                '/istanbul-gezileri/\w*/page/\d*'
            ]),
            callback='parse_item',
            follow=True
        )    
    ]

    def parse_item(self, response):
        urls = response.xpath('//div[@class="td_module_11 td_module_wrap td-animation-stack"]/*[@class="item-details"]/h3/a/@href')
        
        for url in urls:
            yield Request(url.extract(), callback=self.parse_post)
      
    def parse_post(self, response):
        item = ItemParser('cokokuyancokgezen.com', response, '|', 'Çok Okuyan Çok Gezen')
        return item.parse()
