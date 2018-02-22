# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopinwebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company = scrapy.Field()
    company_address = scrapy.Field()
    company_position = scrapy.Field()
    company_wage = scrapy.Field()
    company_desc = scrapy.Field()
    
