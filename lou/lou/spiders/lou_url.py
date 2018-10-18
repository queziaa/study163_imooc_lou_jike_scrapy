# -*- coding: utf-8 -*-
import scrapy
from lou.items import LouItem

class LouUrlSpider(scrapy.Spider):
    name = 'lou_url'
    allowed_domains = ['www.shiyanlou.com']
    start_urls = ['https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page=1']

    def parse(self, response):
        url_item = LouItem()
        num = 0
        for i in response.xpath(".//div[@class='col-md-3 col-sm-6  course']"):
            num +=1
            url_item['courseId'] = i.xpath("./a[@class='course-box']/@href").extract_first()[9:]
            # print('*'+url_item['url']+'*')
            yield url_item
        print('#'+response.url[85:]+'*'+str(num))
        if num != 0:
            yield scrapy.Request(response.url[:85] + str((int(response.url[85:]))+1),callback=self.parse)
