# -*- coding: utf-8 -*-
import scrapy
import pymongo
from jike.items import JikeItem

class JikeUrlSpider(scrapy.Spider):
    name = 'jike_url'
    allowed_domains = ['www.jikexueyuan.com']
    start_urls = ['https://www.jikexueyuan.com/course/?pageNum=1']

    def parse(self, response):
        url_item = JikeItem()
        for i in response.xpath(".//ul[@class='cf']/li"):
            url_item['courseId'] = i.xpath("./@id").extract_first()
            url_item['learnerCount'] = i.xpath("./div[@class='lesson-infor']/div[@class='timeandicon']/div[@class='cf']/em/text()").extract_first()[:-3]
            if i.xpath("./div[@class='lessonimg-box']/i[@class='vip-icon']") != []:
                url_item['originalPrice'] = 260/10
            else:
                url_item['originalPrice'] = None
            url_item['discountPrice'] = url_item['originalPrice']
            url_item['vipPrice'] = url_item['originalPrice']
            yield url_item
        print('#'+response.url[44:])
        if int(response.url[44:]) < int(response.xpath(".//script").re('init\(\d+,(\d+)')[0]):
            yield scrapy.Request(response.url[:44] + str((int(response.url[44:]))+1),callback=self.parse)