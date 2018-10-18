import requests
import json
import pymongo

url = 'https://www.imooc.com/course/AjaxCourseMembers?ids='
client = pymongo.MongoClient(host='127.0.0.1',port=27017)
post = client['imooc']['data_www']

num = 0

for temp  in post.find():
    try:
        post_text = requests.get(url+str(temp['courseId']),timeout=2)
    except:
    	post.update({"courseId":temp['courseId']},{"$set":{'learnerCount':None}},True,False)
    else:
    	post.update({"courseId":temp['courseId']},{"$set":{'learnerCount':json.loads(post_text.text)['data'][0]['numbers']}},True,False)
    print(str(temp['courseId'])+'#'+json.loads(post_text.text)['data'][0]['numbers'])
    print(num)
    num+=1
