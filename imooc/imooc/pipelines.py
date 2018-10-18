# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


mongo_host = '127.0.0.1'
mongo_port = 27017
mongo_db_name = 'imooc'

class ImoocPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host=mongo_host,port=mongo_port)
        self.post = client[mongo_db_name]
        
    def process_item(self, item, spider):
        data = purge(item)
        if spider.name == 'imooc_spider':
            collecttion = 'data_www'
        elif spider.name == 'imooc_coding':
            collecttion = 'data_coding'
        elif spider.name == 'imooc_class':
            collecttion = 'data_class'
        elif spider.name == 'imooc_spider_2':
            collecttion = 'data_www'
        elif spider.name == 'imooc_spider_coding':
            collecttion = 'data_coding'
        elif spider.name == 'imooc_spider__class':
            collecttion = 'data_class'
        else:
            return False
        if spider.name =='imooc_spider_2' or spider.name =='imooc_spider_coding' or spider.name == 'imooc_spider__class':
            self.post[collecttion].update({"courseId":data['courseId']},{"$set":data},False,False)
            return data
        else:
            print(data)
            self.post[collecttion].insert(data)
            return data

def purge(item):
    data = dict(item)
    temp={}
    for DA,DD in data.items():
        temp[DA] = str_int(DD)
    return temp
    
def str_int(num):
    try:
        if num.find('.') != -1:
            temp = int(num[:num.find('.')])
            if int(num[num.find('.')+1:]) != 0:
                temp += int(num[num.find('.')+1:]) / (10 ** len(str(int(num[num.find('.')+1:]))))
        else:
            temp = int(num)
        return temp
    except:
        return num


#  courseId      课程ID
#  productName   标题
#  description   介绍
#  provider      企业
#  score         星级
#  learnerCount  学习人数
#  lessonCount   课程数
#  lectorName    讲师名
#  originalPrice 原价
#  discountPrice 折扣价
#  vipPrice      VIP价格