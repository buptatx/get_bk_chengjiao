# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaChengjiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    house_location = scrapy.Field()
    house_layout = scrapy.Field()
    house_size = scrapy.Field()
    house_detail_link = scrapy.Field()
    house_hangout_price = scrapy.Field()
    house_final_price = scrapy.Field()
    house_final_price_per_square = scrapy.Field()
    price_changed_count = scrapy.Field()
    house_deal_time = scrapy.Field()
    house_direction = scrapy.Field()
    house_has_elevator = scrapy.Field()
    house_position = scrapy.Field()
