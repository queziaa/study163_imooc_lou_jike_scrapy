# -*- coding: utf-8 -*-
import scrapy
import pymongo
from imooc.items import ImoocItem

class ImoocSpiderClassSpider(scrapy.Spider):
    name = 'imooc_spider__class'
    allowed_domains = ['class.imooc.com']
    start_urls = []
    imooc_url = pymongo.MongoClient(host='127.0.0.1',port=27017)['imooc']['data_class']
    for url in imooc_url.find():
        start_urls.append('https://class.imooc.com/sc/'+str(url['courseId'])+'/series')

    def parse(self, response):
        item = ImoocItem()
        item['courseId'] = response.url[27:][:-7]
        item['productName'] = response.xpath(".//div[@class='banner']/div[@class='container']/h2/text()").extract_first()
        item['productName'] += response.xpath(".//div[@class='banner']/div[@class='container']/p/text()").extract_first()
        item['description'] = self.imooc_url.find_one({"courseId":int(item['courseId'])})["description"]
        item['provider'] = "imooc"
        item['lectorName'] = item['provider']
        item['score'] = response.xpath(".//dl[@class='info-wrap'][4]/dd/text()").extract_first()
        item['lessonCount'] = response.xpath("count(.//div[@class='sc-course-cart'])").extract_first()
        item['learnerCount'] = response.xpath(".//dl[@class='info-wrap'][3]/dd/text()").extract_first()
        item['originalPrice'] = response.xpath(".//div[@class='price']/div[@class='pricebox']/span/text()").extract_first()[1:][:-3]
        item['discountPrice'] = item['originalPrice']
        item['vipPrice'] = item['originalPrice']
        item['website'] = "class.imooc"

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
