# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JikeItem(scrapy.Item):
    #课程ID
    courseId = scrapy.Field()
    #标题
    productName = scrapy.Field()
    #介绍
    description = scrapy.Field()
    #企业
    provider = scrapy.Field()
    #星级
    score = scrapy.Field()
    #学习人数
    learnerCount = scrapy.Field()
    #课程数
    lessonCount = scrapy.Field()
    #讲师名
    lectorName = scrapy.Field()
    #原价
    originalPrice = scrapy.Field()
    #折扣价
    discountPrice = scrapy.Field()
    #VIP价格
    vipPrice = scrapy.Field()
    #网站
    website = scrapy.Field()