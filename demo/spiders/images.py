# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from ..items import ImageItem


class ImagesSpider(Spider):
    name = 'images'
    allowed_domains = ['hh8987.pw', 'mgscloud.com']
    base_url = 'http://hh8987.pw'

    def start_requests(self):
        url = self.base_url + '/wtydfAA.htm'
        yield Request(url, callback=self.parse_pre)

    def parse_pre(self, response):
        url = self.base_url + '/cg/index.htm'
        yield Request(url, callback=self.parse_type_pre)

    def parse_type_pre(self, response):
        type_list = response.xpath('//li[@class="biaotou"]/a/@href').extract()
        type_name_list = response.xpath('//li[@class="biaotou"]/a/text()').extract()
        for k, type_url in enumerate(type_list):
            yield Request(type_url, callback=self.parse_type,
                          meta={'type_name': str(type_name_list[k]).replace('\t', ' ')})

    def parse_type(self, response):
        type_name = response.meta['type_name']
        page_list = response.xpath('//div[@class="PageBar"]/a/@href').extract()
        page_list = list(set(page_list))
        for page_url in page_list:
            yield Request(page_url, callback=self.parse_child_pre, meta={'type_name': type_name})

    def parse_child_pre(self, response):
        type_name = response.meta['type_name']
        child_list = response.xpath('//span[@id="main"]/a[@class="aRF"]/@href').extract()
        for child_url in child_list:
            yield Request(child_url, callback=self.parse_child, meta={'type_name': type_name})

    def parse_child(self, response):
        type_name = response.meta['type_name']
        image_title = response.css('title::text').extract_first()[5:]
        image_url_list = response.xpath('//html/script[1]').re('http.*?jpg')
        for image_url in image_url_list:
            item = ImageItem()
            item['url'] = image_url
            item['category'] = type_name
            item['title'] = image_title
            yield item
