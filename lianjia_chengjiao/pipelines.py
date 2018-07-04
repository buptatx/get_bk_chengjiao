# -*- coding: utf-8 -*-

import codecs
import json
import time

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LianjiaChengjiaoPipeline(object):
    def __init__(self):
        res_file = time.strftime("./result/res_%Y%m%d_%H%M%S.log")
        self.file = codecs.open(res_file, 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()