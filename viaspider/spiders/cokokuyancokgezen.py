# -*- coding: utf-8 -*-
import scrapy
from viaspider.items import ViaspiderItem


class CokOkuyanCokGezenSpider(scrapy.Spider):
    name = "cokokuyancokgezen"
    allowed_domains = ["cokokuyancokgezen.com"]
    start_urls = [
        'http://cokokuyancokgezen.com/geziler/afrika/',
        'http://cokokuyancokgezen.com/geziler/asya/'
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!' % response.url)
