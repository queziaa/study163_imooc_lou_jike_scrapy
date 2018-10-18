# -*- coding: utf-8 -*-
import scrapy
import pymongo
from imooc.items import ImoocItem


class ImoocSpiderCodingSpider(scrapy.Spider):
    name = 'imooc_spider_coding'
    allowed_domains = ['coding.imooc.com']
    start_urls = []
    imooc_url = pymongo.MongoClient(host='127.0.0.1',port=27017)['imooc']['data_coding']
    for url in imooc_url.find():
        start_urls.append('https://coding.imooc.com/class/chapter/'+str(url['courseId'])+'.html')

    def parse(self, response):
        item = ImoocItem()
        item['courseId'] = response.url[39:][:-5]
        item['productName'] = "".join(response.xpath(".//div[@class='info-warp tc']/div[1]/h1/text()").extract())
        item['description'] = response.xpath(".//div[@class='info-warp tc']/div[1]/h2/text()").extract_first()
        item['provider'] = response.xpath(".//div[@class='medias']/a/span[@class='name']/text()").extract_first()
        item['lectorName'] = item['provider']
        item['score'] = response.xpath(".//div[@class='static-item'][2]/span[@class='meta-value']/strong/text()").extract_first()[:-1]
        item['lessonCount'] = response.xpath("count(.//li[@class='chapter clearfix']/div[@class='chapter-bd l']/ul/li)").extract_first()
        item['learnerCount'] = response.xpath(".//div[@class='static-item'][1]/span[@class='meta-value']/strong/text()").extract_first()
        item['originalPrice'] = response.xpath(".//span[@class='baseline baseline-y']/span/b[1]/text()").extract_first()
        item['discountPrice'] = item['originalPrice']
        item['vipPrice'] = item['originalPrice']
        item['website'] = "coding.imooc"
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