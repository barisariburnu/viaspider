# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from viaspider.items import ViaspiderItem
from viaspider.settings import SUMMARY_LIMIT


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
        item = ViaspiderItem()
        item['url'] = response.url
        item['source'] = 'drummerlizard.com'
        item['title'] = self.get_title(response)
        item['summary'] = self.get_summary(response)
        item['categories'] = self.get_categories(response)
        item['tags'] = self.get_tags(response, item['categories'])
        item['image'] = self.get_image(response)
        item['created'] = self.get_created(response)
        return item
        
    def get_title(self, response):
        title = response.xpath('//head/title/text()').extract()[0].encode('utf-8')
        return ("|".join(title.split("|")[:-1])).strip() if title.endswith(' | Adım Adım Seyahat') else title
        
    def get_summary(self, response):
        summary = response.xpath('//head/meta[@property="og:description"]/@content').extract()[0]
        return summary[:-SUMMARY_LIMIT] if len(summary) > SUMMARY_LIMIT else summary
        
    def get_categories(self, response):
        categories = response.xpath('//head/meta[@property="article:section"]/@content').extract()
        return categories
        
    def get_tags(self, response, categories):
        tags = response.xpath('//head/meta[@property="article:tag"]/@content').extract()
        return tags if len(tags) > 0 else categories
        
    def get_image(self, response):
        image = response.xpath('//head/meta[@property="og:image"]/@content').extract()[0]
        return image
        
    def get_created(self, response):
        created = response.xpath('//head/meta[@property="article:published_time"]/@content').extract()[0]
        return created