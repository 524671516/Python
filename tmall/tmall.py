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

for i in list(range(1,2)):
    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=557193106901&spuId=869151019&sellerId=1613774608&order=1&currentPage=%s'%i
    
    request = urllib.request.Request(url=url,method='GET')
    response = urllib.request.urlopen(request)

    response_json = response.read()
    str = bytes.decode(response_json,'gbk')
    str = "{"+str.strip()+"}"
    #file =open('C:/Users/CAIWU02/Desktop/tmall.txt','a')
    #file.write(str)
    #file.close()
    assessment = json.loads(str)
    for item in assessment["rateDetail"]["rateList"]:
        sql="insert into t_assessment(t_date,t_content,t_type) values ('"+item["rateDate"]+"','"+item["rateContent"]+"',0)"
        #print(sql)
        cur.execute(sql)
        conn.commit()
    #print(i)
    # 循环抓取数据
    #nickname = []
    #ratecontent = []
    #ratedate=[]
    #content = requests.get(url).text
    #nickname.extend(re.findall('"displayUserNick":"(.*?)"',content))
    #ratedate.extend(re.findall('"rateDate":"(.*?)"',content))
    #ratecontent.extend(re.findall('"rateContent":"(.*?)"',content))
    #print(nickname,ratedate,ratecontent)
    # 写入数据
    # file =open('C:/Users/CAIWU02/Desktop/tmall.txt','a')
    #for j in list(range(0,len(nickname))):
    #    print(j)
    #    #print()
    #    sql="insert into t_assessment(t_date,t_content,t_type) values ('"+ratedate[j]+"','"+ratecontent[j]+"',0)"
    #    # print(sql)
    #    cur.execute(sql)
    #    conn.commit()
    #    #file.write(','.join((nickname[i],ratedate[i],ratecontent[i],'好评'))+'\n')
    ##file.close()
