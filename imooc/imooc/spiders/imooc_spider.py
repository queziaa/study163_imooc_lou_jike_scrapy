# -*- coding: utf-8 -*-
import scrapy
from imooc.items import ImoocItem

class ImoocSpiderSpider(scrapy.Spider):
    name = 'imooc_spider'
    allowed_domains = ['www.imooc.com']
    start_urls = ['https://www.imooc.com/course/list?page=1']

    def parse(self, response):
        imooc_url_item = ImoocItem()
        for i in response.xpath(".//div[@class='course-card-container']"):
            imooc_url_item['courseId'] = i.xpath('./a/@href').extract_first()[7:]
            #print('*'+imooc_url_item['courseId']+'*')
            yield imooc_url_item
        print('#'+response.url[39:])
        yield scrapy.Request(response.url[:39] + str((int(response.url[39:]))+1),callback=self.parse)
        