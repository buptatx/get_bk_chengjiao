#! -*- coding:utf-8 -*-

import codecs
import json
import scrapy

from lianjia_chengjiao.items import LianjiaChengjiaoItem


class LianjiaChengjiao(scrapy.Spider):
    name = "LjChengjiao"
    allowed_domains = ['bj.ke.com']

    def start_requests(self):
        urls = ["https://bj.ke.com/chengjiao/xibahe/"]
        for item in urls:
            yield scrapy.Request(url=item, callback=self.parse_cj_list)

    def parse_cj_list(self, response):
        # #解析当前页
        for item in response.css("ul.listContent li div.info"):
            house_item = LianjiaChengjiaoItem()
            house_item["house_detail_link"] = item.css("div.title a::attr(href)").extract_first()
            info_tmp = item.css("div.title a::text").extract_first().split(" ")
            house_item["house_location"] = info_tmp[0]
            house_item["house_layout"] = info_tmp[1]
            house_item["house_size"] = info_tmp[2]
            house_item["house_deal_time"] = item.css("div.address div.dealDate::text").extract_first()
            house_item["house_position"] = item.css("div.flood div.positionInfo::text").extract_first()
            house_info = item.css("div.address div.houseInfo::text").extract_first()
            temp = house_info.split("|")
            house_item["house_direction"] = temp[0].strip()
            if len(temp) != 3:
                house_item["house_has_elevator"] = u"暂无数据"
            else:
                house_item["house_has_elevator"] = temp[2].strip()

            deal_company = item.css("div.flood div.source::text").extract_first()
            print("deal company:" + deal_company)

            #判断是否需要进入详情页面获取成交信息
            if deal_company == u"其他公司成交":
                house_item["house_hangout_price"] = 0
                house_item["house_final_price"] = 0
                house_item["house_final_price_per_square"] = 0
                house_item["price_changed_count"] = 0
                #print(json.dumps(dict(house_item), encoding="utf-8", ensure_ascii=False))
                yield house_item
            else:
                yield scrapy.Request(url=house_item["house_detail_link"], meta={'item' : house_item}, callback=self.parse_cj_detail)

        #爬取下一页
        page_info = json.loads(response.css("div.house-lst-page-box::attr(page-data)").extract_first())
        total_page = int(page_info["totalPage"])
        cur_page = int(page_info["curPage"])
        base_url = response.css("div.house-lst-page-box::attr(page-url)").extract_first()
        if cur_page < total_page:
        #if cur_page < 2:
            next_page = "".join(["https://bj.ke.com", base_url[:-7], str(cur_page + 1)])
            yield scrapy.Request(url=next_page, callback=self.parse_cj_list)

    def parse_cj_detail(self, response):
        house_item = response.meta['item']

        price = response.css("div.overview div.info div.price::text").extract_first()
        if price != "" and price == u"暂无价格":
            print(u"其他公司成交")
            house_item["house_hangout_price"] = 0
            house_item["house_final_price"] = 0
            house_item["house_final_price_per_square"] = 0
            house_item["price_changed_count"] = 0
        else:   
            house_item["house_hangout_price"] = response.css("div.overview div.info div.msg span label::text").extract_first()
            house_item["house_final_price"] = response.css("div.overview div.info div.price span.dealTotalPrice i::text").extract_first()
            house_item["house_final_price_per_square"] = response.css("div.overview div.info div.price b::text").extract_first()
            house_item["price_changed_count"] = response.css("div.overview div.info div.msg span label::text").extract()[2]
        yield house_item

    def parse_cj_detail_test(self, response):
        price = response.css("div.overview div.info div.price::text").extract_first()
        print(price)
        if price != "" and price == u"暂无价格":
            print(u"其他公司成交")

    def parse_cj_list_test(self, response):
        # #解析当前页
        for item in response.css("ul.listContent li div.info"):
            house_item = LianjiaChengjiaoItem()
            house_item["house_detail_link"] = item.css("div.title a::attr(href)").extract_first()
            info_tmp = item.css("div.title a::text").extract_first().split(" ")
            house_item["house_location"] = info_tmp[0]
            house_item["house_layout"] = info_tmp[1]
            house_item["house_size"] = info_tmp[2]
            house_item["house_deal_time"] = item.css("div.address div.dealDate::text").extract_first()
            house_item["house_deal_time"] = item.css("div.address div.dealDate::text").extract_first()
            house_item["house_position"] = item.css("div.flood div.positionInfo::text").extract_first()
            house_info = item.css("div.address div.houseInfo::text").extract_first()
            temp = house_info.split("|")
            house_item["house_direction"] = temp[0]
            if len(temp) != 3:
                house_item["house_has_elevator"] = u"暂无数据"
            else:
                house_item["house_has_elevator"] = temp[2]

            deal_company = item.css("div.flood div.source::text").extract_first()
            print("deal company:" + deal_company)

            print(json.dumps(dict(house_item), encoding="utf-8", ensure_ascii=False))
            #判断是否需要进入详情页面获取成交信息
            if deal_company == u"其他公司成交":
                house_item["house_hangout_price"] = 0
                house_item["house_final_price"] = 0
                house_item["house_final_price_per_square"] = 0
                house_item["price_changed_count"] = 0
                #print(json.dumps(dict(house_item), encoding="utf-8", ensure_ascii=False))
                #yield house_item
            else:
                print("go to " + house_item["house_detail_link"])
                #yield scrapy.Request(url=house_item["house_detail_link"], meta={'item' : house_item}, callback=self.parse_cj_detail)

        
