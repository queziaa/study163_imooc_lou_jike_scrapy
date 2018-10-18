import requests
import json
import copy
import pymongo

start_urls = [
    # {"name":"办公效率","url":[
    #     {"urlMini":"400000000146050","name":"办公软件"},
    #     {"urlMini":"400000000144053","name":"工作效率"},
    #     {"urlMini":"400000000154043","name":"电脑基础"},
    #     {"urlMini":"400000001263002","name":"考试认证"}
    # ],"db":"office"},
    # {"name":"职场发展","url":[
    #     {"urlMini":"400000001315003","name":"个人提升"},
    #     {"urlMini":"400000001319002","name":"职场能力"},
    #     {"urlMini":"400000001312009","name":"求职应聘"},
    #     {"urlMini":"400000001309006","name":"商学院"}
    # ],"db":"work"},
    # {"name":"职业岗位","url":[
    #     {"urlMini":"400000001325004","name":"设计软件"},
    #     {"urlMini":"400000001332011","name":"平面设计"},
    #     {"urlMini":"400000001327012","name":"其他设计"},
    #     {"urlMini":"400000001323009","name":"市场营销"},
    #     {"urlMini":"400000001334010","name":"人力资源管理"},
    #     {"urlMini":"400000001323011","name":"专业岗位"},
    #     {"urlMini":"400000001335004","name":"其他职业岗位"}
    # ],"db":"occupation"},
    # {"name":"金融财会","url":[
    #     {"urlMini":"400000001368004","name":"个人理财"},
    #     {"urlMini":"400000001375002","name":"金融财会理论"},
    #     {"urlMini":"400000001366005","name":"金融行业"},
    #     {"urlMini":"400000001372002","name":"金融财会考试"}
    # ],"db":"finance"},
    # {"name":"语言留学","url":[
    #     {"urlMini":"400000001308002","name":"英语口语"},
    #     {"urlMini":"400000001317002","name":"新概念英语"},
    #     {"urlMini":"400000001318002","name":"英语零基础"},
    #     {"urlMini":"400000001315002","name":"少儿英语"},
    #     {"urlMini":"400000001312001","name":"英语考试"},
    #     {"urlMini":"400000000658001","name":"出国留学"},
    #     {"urlMini":"400000000692002","name":"日语"},
    #     {"urlMini":"400000000698002","name":"韩语"},
    #     {"urlMini":"400000000694003","name":"小语种方言等"}
    # ],"db":"language"},
    # {"name":"职业考试","url":[
    #     {"urlMini":"400000001326002","name":"项目管理"},
    #     {"urlMini":"400000001331001","name":"计算机类认证"},
    #     {"urlMini":"400000001322001","name":"建筑工程"},
    #     {"urlMini":"400000001322002","name":"医药卫生"},
    #     {"urlMini":"400000001329002","name":"电子商务师"},
    #     {"urlMini":"400000001321003","name":"新媒体运营师"},
    #     {"urlMini":"400000001326003","name":"人力资源师"},
    #     {"urlMini":"400000001374005","name":"金融财会考试"},
    #     {"urlMini":"400000001374004","name":"公职培训"},
    #     {"urlMini":"400000001324003","name":"更多考试"}
    # ],"db":"examin"},
    # {"name":"职场之外","url":[
    #     {"urlMini":"400000001367002","name":"摄影影视"},
    #     {"urlMini":"400000001286026","name":"音乐乐器"},
    #     {"urlMini":"400000001292019","name":"运动健康"},
    #     {"urlMini":"400000001295014","name":"兴趣修养"},
    #     {"urlMini":"400000001287024","name":"居家生活"},
    #     {"urlMini":"400000001296020","name":"心理学科"},
    #     {"urlMini":"400000001287025","name":"亲子育儿"},
    #     {"urlMini":"400000001289030","name":"升学辅导"}
    # ],"db":"outside"},
    {"name":" IT&互联网","url":[
        {"urlMini":"400000001334002","name":"编程语言"},
        {"urlMini":"400000001322005","name":"前端开发"},
        {"urlMini":"400000001322004","name":"后端开发"},
        {"urlMini":"400000001329003","name":"移动开发"},
        {"urlMini":"400000001334001","name":"网络与运维"},
        {"urlMini":"400000001332002","name":"互联网产品"},
        {"urlMini":"400000001316005","name":"互联网运营"},
        {"urlMini":"400000001309004","name":"互联网设计"}
    ],"db":"it"},
    {"name":"人工智能","url":[
        {"urlMini":"400000001332006","name":"数据科学"},
        {"urlMini":"400000001333008","name":"人工智能"},
        {"urlMini":"400000001327004","name":"区块链"},
        {"urlMini":"400000001334005","name":"智能设备和物联网"}
    ],"db":"it"}
]

class spider163(object):
    url = 'https://study.163.com/p/search/studycourse.json'
    headers = {"Content-Type":"application/json","edu-script-token": "76cdf6a089d540b581cdd33929a29885","Host": "study.163.com","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    data_initial = {'pageIndex': 1,'pageSize': 50,'relativeOffset': 0,'frontCategoryId': "",'searchTimeType': -1,'orderType': 50,'priceType': -1,'activityId': 0,'keyword': ""}
    mongoHost = '127.0.0.1'
    mongoPort = 27017
    mongoName = 'study'  #数据库名字

    def __init__(self,name="test",db="test",url="test"):
        client = pymongo.MongoClient(host=self.mongoHost,port=self.mongoPort)
        mydb = client[self.mongoName]
        self.post = mydb[db]
        self.name = name
        self.data = copy.deepcopy(self.data_initial)
        self.data["frontCategoryId"] = url
        self.temp = {}
        
    def postIndex(self,index=False):
        if index:
            self.data["pageIndex"] = index
            self.data["relativeOffset"] = (index-1)*50
        try:
            post_text = requests.post(self.url, data=json.dumps(self.data), headers=self.headers)
        except:
            return {"type":0,"name":self.name,"index":self.data["pageIndex"]}
        else:
            self.data["pageIndex"] += 1
            self.data["relativeOffset"] += 50
            temp = json.loads(post_text.text)["result"]["list"]
            if temp == None:
                return {"type":1,"name":self.name,"index":self.data["pageIndex"]-1}
            for i in temp:
                s={}
                s['courseId'] = i['courseId']
                s['productName'] = i['productName']
                s['description'] = i['description']
                s['provider'] = i['provider']
                s['score'] = i['score']
                s['learnerCount'] = i['learnerCount']
                s['lessonCount'] = i['lessonCount']
                s['lectorName'] = i['lectorName']
                s['originalPrice'] = i['originalPrice'] if i['originalPrice'] != 0 else None
                s['discountPrice'] = i['discountPrice'] if i['discountPrice'] != 0 else None
                s['vipPrice'] = None
                s['website'] = '163study'
                self.post.insert(s)
            return {"type":2,"name":self.name,"index":self.data["pageIndex"]-1}

    def verification(self,urlMini,urlName):          #验证url可用
        temp_data = copy.deepcopy(self.data_initial)
        temp_data["frontCategoryId"] = urlMini
        try:
            post_text = requests.post(self.url, data=json.dumps(temp_data), headers=self.headers)
        except:
            print('    None@' + urlName)
        else:
            try:
                json.loads(post_text.text)
            except:
                print('    False@' + urlName)
            else:
                print('    True@' + urlName)


#验证start_urls 不需要就注释################################
# ver = spider163()
# for i_urls in start_urls:
#     print('验证:'+i_urls["name"])
#     for url in i_urls["url"]:
#         ver.verification(url['urlMini'],url['name'])
###########################################################

for i_urls in start_urls:
    print('开始:'+i_urls["name"])
    for url in i_urls["url"]:
        print('    开始:'+url["name"])
        temp_spider = spider163(name=url["name"],db=i_urls["db"],url=url["urlMini"])
        while True:
            temp_spider_log = temp_spider.postIndex()
            if temp_spider_log['type'] == 0:
                print('    下载错误:'+str(temp_spider_log))
            elif temp_spider_log['type'] == 1:
                print('    结束:'+str(temp_spider_log))
                break
            elif temp_spider_log['type'] == 2:
                print('    下载:'+str(temp_spider_log))
            else:
                pass

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
