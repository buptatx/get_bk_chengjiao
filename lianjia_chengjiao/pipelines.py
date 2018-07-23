# -*- coding: utf-8 -*-

import codecs
import json
import pymysql
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

class LianjiaDBPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8')

        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.excute("select * from tbl_house_info where house_detail_link='%s'" 
                % item["house_detail_link"])
            rep = self.curcor.fetchone()
        except Exception as error:
            print("select error " + error)
            self.cursor.close()
            self.connect.close()
            
        if not rep:
            try:
                mexec = "insert into tbl_house_info () value`"
                self.cursor.execute(mexec)
                self.connect.commit()
            except Exception as error:
                print("insert error" + error)
                self.cursor.close()
                self.connect.close()

        self.cursor.close()
        self.connect.close()
        return item
