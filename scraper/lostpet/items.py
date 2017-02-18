# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LostpetItem(scrapy.Item):
    # define the fields for your item here like:
    client_id = scrapy.Field()
    url = scrapy.Field()
    client_name = scrapy.Field()
    client_email = scrapy.Field()
    pet_name = scrapy.Field()
