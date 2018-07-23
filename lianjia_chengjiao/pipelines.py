# -*- coding: utf-8 -*-

import codecs
import json
import pymysql
import time
import settings

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
        rep = ""
        try:
            self.cursor.execute("select * from tbl_house_info where link='%s'" 
                % item["house_detail_link"])
            rep = self.cursor.fetchone()
        except Exception as error:
            print("select error " + str(error))
            
        if rep == "":
            try:
                if "--" in item["house_size"]:
                    house_size = 0
                else:
                    house_size = float(item["house_size"].split(u"平米")[0])
                    pps = int(item["house_final_price_per_square"])
                    pcc = int(item["price_changed_count"])
                    hp = float(item["house_hangout_price"])
                    fp = float(item["house_final_price"])
                    mquery = "insert into tbl_house_info (location,layout,position,haselevator,pricepers,dealtime,"\
                        "size,direction,changecount,hangout,final,link) "\
                        "values ('%s', '%s', '%s', '%s', %d, '%s', '%s', '%s', %d, %.2f, %.2f, '%s')" % (
                        item["house_location"], item["house_layout"], item["house_position"], 
                        item["house_has_elevator"], pps, item["house_deal_time"], house_size, item["house_direction"],
                        pcc, hp, fp, item["house_detail_link"])
                    self.cursor.execute(mquery)
                    self.connect.commit()
            except Exception as error:
                print("insert error" + str(error))

        return item

    def spider_closed(self, spider):
        self.cursor.close()
        self.connect.close()
