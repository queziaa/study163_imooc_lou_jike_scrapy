# -*- coding: utf-8 -*-
import scrapy
import pymongo
from lou.items import LouItem

class LouDataSpider(scrapy.Spider):
    name = 'lou_data'
    allowed_domains = ['www.shiyanlou.com']
    start_urls = []
    urls = pymongo.MongoClient(host='127.0.0.1',port=27017)['lou']['lou_url']
    for url in urls.find():
        start_urls.append('https://www.shiyanlou.com/courses/'+str(url['courseId']))

    def parse(self, response):
        item = LouItem()
        item['courseId'] = response.url[34:]
        item['productName'] = response.xpath(".//div[@class='clearfix course-infobox-header']/h4/span[1]/text()").extract_first()
        item['description'] = response.xpath(".//div[@class='course-infobox-content']/p/text()").extract_first()
        item['provider'] = response.xpath(".//div[@class='mooc-info']/div[@class='name']/strong/text()").extract_first()
        item['lectorName'] = item['provider']
        item['score'] = None
        item['lessonCount'] = response.xpath("count(.//div[@class='tab-pane active']/div)").extract_first()[:-2]
        item['learnerCount'] = response.xpath(".//div[@class='course-info-details']/span[1]/text()").extract_first()[:-4]
        vip_type = response.xpath(".//h4[@class='course-infobox-title']/span[2]/@data-course-type").extract_first()
        if vip_type == "5":
            item['originalPrice'] = 399/10
            item['discountPrice'] = item['originalPrice']
            item['vipPrice'] = item['originalPrice']
        elif vip_type == "1":
            item['originalPrice'] = response.xpath(".//span[@class='bootcamp-real-price']/text()").extract_first()[1:]
            item['vipPrice'] = response.xpath(".//div[@class='bootcamp-discount']/div/span[2]/span[2]/span/text()").extract_first()
            if response.xpath(".//span[@class='bootcamp-original-price']/text()").extract_first() != None:
                item['discountPrice'] = response.xpath(".//span[@class='bootcamp-original-price']/text()").extract_first()[1:]
            else:
                item['discountPrice'] = None
        else:
            item['originalPrice'] = None
            item['discountPrice'] = item['originalPrice']
            item['vipPrice'] = item['originalPrice']
        item['website'] = "lou"
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
