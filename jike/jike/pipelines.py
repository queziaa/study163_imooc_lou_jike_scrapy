# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

mongo_host = '127.0.0.1'
mongo_port = 27017
mongo_db_name = 'jike'

class JikePipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host=mongo_host,port=mongo_port)
        self.post = client[mongo_db_name]['data']

    def process_item(self, item, spider):
        data = purge(item)
        if spider.name == 'jike_url':
            self.post.insert(data)
            return data
        elif spider.name == 'jike_data':
            self.post.update({"courseId":data['courseId']},{"$set":data},True,False)
            return data
        else:
        	return False

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