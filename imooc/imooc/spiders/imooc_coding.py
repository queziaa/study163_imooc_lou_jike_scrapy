# -*- coding: utf-8 -*-
import scrapy
from imooc.items import ImoocItem

class ImoocCodingSpider(scrapy.Spider):
    name = 'imooc_coding'
    allowed_domains = ['coding.imooc.com']
    start_urls = ['https://coding.imooc.com/?sort=0&unlearn=0&page=1']

    def parse(self, response):
        imooc_url_item = ImoocItem()
        num=0
        for i in response.xpath(".//div[@class='shizhan-course-list clearfix']/div/a/@href"):
            num+=1
            imooc_url_item['courseId'] = i.extract()[7:][:-5]
            yield imooc_url_item
        print('#'+response.url[48:]+'#'+str(num))
        if num!=0:
        	yield scrapy.Request(response.url[:48] + str((int(response.url[48:]))+1),callback=self.parse)
