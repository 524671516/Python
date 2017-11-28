from pip._vendor import requests
import re
# 创建循环链接
import pymssql
import json
import datetime
import time
import urllib


def getAssessment(start,end):
    sql = "delete from t_assessment where t_date<'" + end + "' and t_date>='" + start + "' and t_productId=%s" % row_Id[i][0]
    cur.execute(sql)
    conn.commit()
    j = 1
    flag = False
    sum_count = 0
    while(flag == False):
        single_count = 0
        url = source % j
        request = urllib.request.Request(url=url,method='GET')
        response = urllib.request.urlopen(request)
        response_json = response.read()
        str = bytes.decode(response_json,'gbk')
        str = "{" + str.strip() + "}"
        try:
            assessment = json.loads(str)
            print("no error:",j)
            if(len(assessment["rateDetail"]["rateList"]) == 0):
                flag = True
                break
            for item in assessment["rateDetail"]["rateList"]:
                if(start <= item["rateDate"] < end):
                    sql = "insert into t_assessment(t_productId,t_date,t_content,t_type) values ('" + newId_str + "','" + item["rateDate"] + "','" + item["rateContent"] + "',0)"
                    cur.execute(sql)
                    conn.commit()
                    single_count = single_count + 1
                    sum_count = sum_count + 1
                if(item["rateDate"] < start):
                    flag = True
                    break
            j = j + 1
            print("single_count:",single_count)
            print("sum_count:",sum_count)
        except:
            print("error:",j)
            time.sleep(3)
    return sum_count
    

server = "115.29.197.27"
user = "sa"
password = "mail#wwwx"
database = "tmall"
conn = pymssql.connect(server, user, password,database)

file = open('d:/tmall.txt','a')
file.write("    ----" + datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S') + "----" + '\n')
cur = conn.cursor()
productIdList = "select Id, t_itemCode from t_product"
cur.execute(productIdList)
row_Id = cur.fetchall()
total_count = 0
for i in list(range(0,len(row_Id))):
    file.write("开始下载商品:【" + str(row_Id[i][1]) + "】的评价..." + '\n')
    source = 'https://rate.tmall.com/list_detail_rate.htm?itemId=' + row_Id[i][1] + '&sellerId=1613774608&order=1&currentPage=%s'
    print(source)
    newId_str = str(row_Id[i][0])
    
    now = datetime.datetime.now()
    end = now.strftime('%Y-%m-%d 00:00:00')
    #end = '2015-01-01 00:00:00'
    start = (now + datetime.timedelta(days=-1)).strftime('%Y-%m-%d 00:00:00')
    #start = '2014-12-31 00:00:00'
    single_count = getAssessment(start,end)
    file.write("下载完成，共%s" %single_count + "条！" + '\n')
    total_count = total_count + single_count
file.write("    --所有评价下载完成，共%s" %total_count+ "条！--" + '\n')
file.close()
