#! -*- coding:utf-8 -*-

import json
import pymysql

def load_from_file(filename):
    content = []
    with open(filename, "rb") as mf:
        for line in mf:
            content.append(json.loads(line))

    return content


def do_mysql_insert(filename):
    res = load_from_file(filename)
    
    db = pymysql.connect('localhost', "test", "test", "myscrapy")
    mcursor = db.cursor()

    for item in res:
        if "--" in item["house_size"]:
            house_size = 0
        else:
            house_size = float(item["house_size"].split(u"平米")[0])
        pps = int(item["house_final_price_per_square"])
        pcc = int(item["price_changed_count"])
        hp = float(item["house_hangout_price"])
        fp = float(item["house_final_price"])
        #print(json.dumps(item, encoding="utf-8", ensure_ascii=False))
        mquery = "insert into tbl_house_info (location,layout,position,haselevator,pricepers,dealtime,"\
            "size,direction,changecount,hangout,final,link) values ('%s', '%s', '%s', '%s', %d, '%s', '%s', '%s', %d, %.2f, %.2f, '%s')" % (
                item["house_location"], item["house_layout"], item["house_position"], item["house_has_elevator"], 
                pps, item["house_deal_time"], house_size, item["house_direction"],
                pcc, hp, fp, item["house_detail_link"])
        print(mquery)
        sta = mcursor.execute(mquery)
        print(str(sta))

    db.commit()
    mcursor.close()
    db.close()
        

if __name__ == "__main__":
    do_mysql_insert("./result/res_20180705_171731.log")
