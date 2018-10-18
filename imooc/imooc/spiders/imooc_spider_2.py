# -*- coding: utf-8 -*-
import scrapy
import pymongo
from imooc.items import ImoocItem


class ImoocSpider2Spider(scrapy.Spider):
    name = 'imooc_spider_2'
    allowed_domains = ['www.imooc.com']
    start_urls = []
    imooc_url = pymongo.MongoClient(host='127.0.0.1',port=27017)['imooc']['data_www']
    for url in imooc_url.find():
        start_urls.append('https://www.imooc.com/learn/'+str(url['courseId']))

    def parse(self, response):
        item = ImoocItem()
        item['courseId'] = response.url[28:]
        item['productName'] = response.xpath(".//div[@class='course-infos']/div[@class='w pr']/div[@class='path']/a/span/text()").extract_first()
        item['description'] = response.xpath(".//div[@class='course-info-main clearfix w']/div[@class='content-wrap clearfix']/div[@class='content']/div[@class='course-description course-wrap']/text()").extract_first()
        item['provider'] = response.xpath(".//div[@class='course-infos']/div[@class='w pr']/div[@class='statics clearfix']/div[@class='teacher-info l']/span/a/text()").extract_first() 
        item['lectorName'] = item['provider']
        item['score'] = response.xpath(".//div[@class='course-infos']/div[@class='w pr']/div[@class='statics clearfix']/div[@class='static-item l score-btn']/span[@class='meta-value']/text()").extract_first()
        item['lessonCount'] = response.xpath("count(.//li[@data-media-id])").extract_first()
        item['learnerCount'] = None #人数通过Ajax获取
        item['originalPrice'] = None  #没有价格
        item['discountPrice'] = None  #没有价格
        item['vipPrice'] = None       #没有价格
        item['website'] = "www.imooc"
        yield item


#  courseId      课程ID
#  productName   标题
#  description   介绍
#  provider      企业
#  lectorName    讲师名
#  score         星级
#  learnerCount  学习人数
#  lessonCount   课程数
#  originalPrice 原价
#  discountPrice 折扣价
#  vipPrice      VIP价格