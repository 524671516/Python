from pip._vendor import requests
import re
# 创建循环链接
import pymssql
import json
import datetime
import time
import urllib

server = "115.29.197.27"
user = "sa"
password = "mail#wwwx"
database="tmall"
conn = pymssql.connect(server, user, password,database)
cur=conn.cursor()

def getAssessment(start,end):
    i=1
    flag = False
    sql="delete from t_assessment where t_date<'"+end+"' and t_date>='"+start+"'"
    cur.execute(sql)
    conn.commit()
    sum_count=0
    while(flag==False):
    #for i in list(range(1,10)):
        single_count=0
        url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=41482176804&spuId=235557795&sellerId=1613774608&order=1&currentPage=%s'%i
        request = urllib.request.Request(url=url,method='GET')
        response = urllib.request.urlopen(request)
        response_json = response.read()
        str = bytes.decode(response_json,'gbk')
        str = "{"+str.strip()+"}"
        try:
            assessment = json.loads(str)
            print("no error:",i)
            for item in assessment["rateDetail"]["rateList"]:
                if(start<=item["rateDate"]<end):
                     sql="insert into t_assessment(t_date,t_content,t_type) values ('"+item["rateDate"]+"','"+item["rateContent"]+"',0)"
                     cur.execute(sql)
                     conn.commit()
                     single_count=single_count+1
                     sum_count=sum_count+1
                if(item["rateDate"]<start):
                    flag = True
                    break
            i=i+1
            print("single_count:",single_count)
            print("sum_count:",sum_count)
        except:
            print("error:",i)
            time.sleep(3)
        
        

now = datetime.datetime.now()
end = now.strftime('%Y-%m-%d 00:00:00')
start = (now + datetime.timedelta(days=-1)).strftime('%Y-%m-%d 00:00:00')
getAssessment(start,end)
