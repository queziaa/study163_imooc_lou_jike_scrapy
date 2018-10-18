# -*- coding: utf-8 -*-
import scrapy
from imooc.items import ImoocItem

class ImoocClassSpider(scrapy.Spider):
    name = 'imooc_class'
    allowed_domains = ['class.imooc.com']
    start_urls = ['https://class.imooc.com/?page=1']

    def parse(self, response):
        imooc_url_item = ImoocItem()
        num=0
        for i in response.xpath(".//a[@class='plan-item l']"):
            num+=1
            imooc_url_item['courseId'] = i.xpath('./@href').extract_first()[4:]
            imooc_url_item['description'] = i.xpath("./div[@class='plan-item-desc-box']/p[@class='plan-item-desc-content']/text()").extract_first()
            yield imooc_url_item
        print('#'+response.url[30:]+'#'+str(num))
        if num!=0:
        	yield scrapy.Request(response.url[:30] + str((int(response.url[30:]))+1),callback=self.parse)


