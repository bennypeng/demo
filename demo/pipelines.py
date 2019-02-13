# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import os
import logging


class ImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_category_name = item['category']
        image_name = item['title']
        url = request.url
        file_name = url.split('/')[-1]
        path = '/' + image_category_name + '/' + image_name + '/' + file_name
        return path

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Image Downloaded Failed.')
        logging.info('Download complete：' + image_path[0])
        return item

    def get_media_requests(self, item, info):
        yield Request(item['url'], meta={'item': item})


class CategoryPipeline(object):

    @staticmethod
    def create_dir(path):
        path = path.strip()
        path = path.rstrip('\\')
        is_exists = os.path.exists(path)

        if not is_exists:
            os.makedirs(path)
            logging.info('Create directory：' + path)
            return True
        else:
            return False

    def process_item(self, item, spider):
        image_category_name = item['category']
        image_name = item['title']
        path = './images/' + image_category_name + '/' + image_name
        self.create_dir(path)
        return item
