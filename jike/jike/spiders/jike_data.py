# -*- coding: utf-8 -*-
import scrapy
import pymongo
from jike.items import JikeItem


class JikeDataSpider(scrapy.Spider):
    name = 'jike_data'
    allowed_domains = ['www.jikexueyuan.com']
    start_urls = []
    urls = pymongo.MongoClient(host='127.0.0.1',port=27017)['jike']['data']
    for url in urls.find():
        start_urls.append('https://www.jikexueyuan.com/course/'+str(url['courseId'])+'.html')

    def parse(self, response):
        item = JikeItem()
        item['courseId'] = response.url[35:-5]
        item['productName'] = response.xpath(".//div[@class='bc-box']/h2/a/text()").extract_first()
        description = response.xpath(".//div[@class='infor-content']/text()").extract()
        item['description'] = ''
        for i_content in description:
            item['description'] += ("".join(i_content.split()))
        item['provider'] = response.xpath(".//div[@class='infor-text']/p/text()").extract_first()
        item['lectorName'] = response.xpath(".//div[@class='infor-text']/strong/a/text()").extract_first()
        item['score'] = None
        item['lessonCount'] = response.xpath("count(.//div[@class='lesson-box']/ul/li)").extract_first()
        item['website'] = "jike"
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
