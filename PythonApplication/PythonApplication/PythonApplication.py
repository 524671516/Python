from pip._vendor import requests
from os.path import exists 
import pymssql
import json
import datetime
import time
from urllib import parse,request
import hashlib
import sys
import urllib
import http.client
import string

def DBConnection():
    server = "115.29.197.27"
    user = "sa"
    password = "mail#wwwx"
    database = "MonthlyDelivery_BAK"
    conn = pymssql.connect(server, user, password,database)
    return conn

def sign(json_data,secret):
    enValue = secret + str(json_data) + secret
    res = hashlib.md5()
    res.update(enValue.encode(encoding='utf-8'))
    res = res.hexdigest().upper()
    return res

#获取订单
def getOrders(Time):
    conn = DBConnection()
    cur = conn.cursor()
    orderList = "select details.orderid,details.note from ORDERERP.dbo.details where orderid in (select id from ORDERERP.dbo.orders where createtime>'"+Time+"') and details.note like '%sqz[34][34][34]%' group by details.orderid,details.note"
    cur.execute(orderList)
    orders = cur.fetchall()
    sucorders = []
    product_id = 0
    cycle_index = 0
    strsqz = 'sqz333'
    result = ''
    if(orders!=[]):
        for i in list(range(0,len(orders))):
            if strsqz in orders[i][1]:
                product_id = 1
                cycle_index = 6
                result = insertSingleOrder(orders[i][0],product_id,cycle_index)
            else:
                product_id = 2
                cycle_index = 3
                result = insertSingleOrder(orders[i][0],product_id,cycle_index)
            if(result!=None):
                sucorders.append("订单:"+result)
        if(sucorders!=[]):
            max_record=50
            if(len(sucorders)>max_record):
                for i in range(0,len(sucorders)//max_record):
                    CreateRecord("成功获取数:50",""+ str(sucorders[i*max_record:i*max_record+49]).replace('\'','')+ "",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
                CreateRecord("成功获取数:"+ str(len(sucorders)-len(sucorders)//max_record*max_record),""+ str(sucorders[len(sucorders)//max_record*max_record:len(sucorders)]).replace('\'','')+ "",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
            else:
                CreateRecord("成功获取数:"+ str(len(sucorders)),""+ str(sucorders).replace('\'','')+ "",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
    else:
        CreateRecord("成功获取数:"+ str(len(orders)),"暂无订单",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))

def getHistoryOrders(code):
    conn = DBConnection()
    cur = conn.cursor()
    HistoryOrdersList = "select COUNT(orders.platform_code) from ORDERERP.dbo.orders where orders.platform_code = '"+code+"'"
    cur.execute(HistoryOrdersList)
    HistoryOrders = cur.fetchall()
    orderLen = HistoryOrders[0][0]
    if(orderLen>1):
        for i in range(1,orderLen):
             OrdersList = "select * from ORDERERP.dbo.orders where orders.platform_code ='"+code+"'"
             cur.execute(OrdersList)
             Orders = cur.fetchall()
             platform_code = Orders[0][7]
             amount = Orders[0][3]
             pament = Orders[0][4]
             qty = Orders[0][2]/3
             create_time =  Orders[0][8]
             vip_code = Orders[0][18]
             receiver_tel = Orders[0][21]
             receiver_address = Orders[0][23]
             IndexAddress = findStr(receiver_address," ",3)
             Straddress = receiver_address[IndexAddress+1:]
             receiver_ares = Orders[0][24]
             remark = Orders[0][25]
             discount_fee = Orders[0][30]
             patment_amount = Orders[0][33]
             if(receiver_ares == None):
                 receiver_ares = receiver_address[:IndexAddress]
                 receiver_ares = receiver_ares.replace(' ','-')
                 receiver_ares = receiver_ares.replace('null',' ')
             select_str = "select * from MD_Order where MD_Order.order_code = '"+platform_code+"' and createtime = '"+create_time+"'"
             cur.execute(select_str)
             strorder = cur.fetchall()
             if (strorder == []):
                 cur.execute("insert into MD_Order " + "(product_id,order_code,qty,amount,payment,discount_fee,payment_amount,receiver_date,receiver_area,"+
                "receiver_address,receiver_tel,delivery_state,upload_status,vip_code,receiver_times,remark) values(%d,%s,%d,%d,%d,%d,%d,%s,%s,%s,%s,%d,%d,%s,%d,%s)",(product_id,platform_code,qty,amount,pament,discount_fee,patment_amount,create_time,receiver_ares,Straddress,receiver_tel,0,1,vip_code,1,remark))                    
    conn.commit()
    conn.close()

#新建order进数据库
def insertSingleOrder(order,product_id,cycle_index):
    conn = DBConnection()
    cur = conn.cursor()
    OrdersList = "select * from ORDERERP.dbo.orders where orders.id = %d"%order
    cur.execute(OrdersList)
    Orders = cur.fetchall()
    amount = Orders[0][3]
    pament = Orders[0][4]
    qty = Orders[0][2]/3
    platform_code = Orders[0][7]
    #getHistoryOrders("127241773940265853")
    create_time =  Orders[0][8]
    vip_code = Orders[0][18]
    receiver_tel = Orders[0][21]
    receiver_address = Orders[0][23]
    IndexAddress = findStr(receiver_address," ",3)
    Straddress = receiver_address[IndexAddress+1:]
    receiver_ares = Orders[0][24]
    remark = Orders[0][25]
    if(receiver_ares == None):
        receiver_ares = receiver_address[:IndexAddress]
        receiver_ares = receiver_ares.replace(' ','-')
        receiver_ares = receiver_ares.replace('null',' ')
    discount_fee = Orders[0][30]
    patment_amount = Orders[0][33]
    select_str = "select * from MD_Order where  MD_Order.order_code = '"+platform_code+"'"
    cur.execute(select_str)
    strorder = cur.fetchall()
    if (strorder == []):
        cur.execute("insert into MD_Order " + "(product_id,order_code,qty,amount,payment,discount_fee,payment_amount,receiver_date,receiver_area,"+
                "receiver_address,receiver_tel,delivery_state,upload_status,vip_code,receiver_times,remark) values(%d,%s,%d,%d,%d,%d,%d,%s,%s,%s,%s,%d,%d,%s,%d,%s)",(product_id,platform_code,qty,amount,pament,discount_fee,patment_amount,create_time,receiver_ares,Straddress,receiver_tel,0,1,vip_code,1,remark))
        if(qty<5):
            cur.execute("select @@IDENTITY")
            row = cur.fetchall()
            insert_id = row[0]
            Order = "select * from MD_Order where MD_Order.id = %d"%insert_id
            cur.execute(Order)
            orders = cur.fetchall()
            plantformId = orders[0][1]
            order_status= orders[0][3]
            Remark = orders[0][5]
            parentOrderId = orders[0][0]
            vipCode = orders[0][11]
            Qty = orders[0][14]
            receiverArea = orders[0][12]
            receiverAddress = orders[0][6]
            receiverTell = orders[0][9]
            up_date = "update MD_Order set parentOrder_id = %d "%parentOrderId+"where MD_Order.id = %d"%insert_id
            cur.execute(up_date)
            #增加order
            for i in range(1,cycle_index):
                cur.execute("select @@IDENTITY")
                row_d = cur.fetchall()
                insertd_id = row_d[0]
                Order_d = "select * from MD_Order where MD_Order.id = %d"%insertd_id
                cur.execute(Order_d)
                orders_d = cur.fetchall()
                receiver_d = datetime_offset_by_month(orders_d[0][2],1)
                cur.execute("insert into MD_Order " + "(product_id,order_code,qty,receiver_date,parentOrder_id,receiver_times,vip_code,"+
                           "receiver_area,receiver_address,receiver_tel,upload_status,remark) values(%d,%s,%d,%s,%d,%d,%s,%s,%s,%s,%d,%s)",(product_id,"MD"+ plantformId + str(-i),Qty,receiver_d,parentOrderId,i+1,vipCode,receiverArea,receiverAddress,receiverTell,0,Remark)) 
    else:
        CreateRecord("error","订单["+ platform_code +"]已存在！",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
        return None
    conn.commit()
    conn.close()
    return platform_code

#获取订单数据转为jsonList
def getDBData():
    conn=DBConnection()
    cur = conn.cursor()
    OrderList = "select * from MD_Order where MD_Order.order_status!=-1 and upload_status !=1"
    cur.execute(OrderList)
    orderList = cur.fetchall()
    CreateData_List=[]
    for i in list(range(0,len(orderList))):
        plantformId = orderList[i][1]
        quantity = orderList[i][14]
        receiverDate =orderList[i][2]
        order_status=orderList[i][3]
        remark=orderList[i][5]
        if(remark==None):
            remark=""
        parentOrderId=orderList[i][7]
        receiver_mobile=orderList[i][9]
        productId=orderList[i][10]
        vipCode=orderList[i][11]
        receiver_address=orderList[i][6]
        receiver_area=orderList[i][12]
        receiver_name=orderList[i][20]
        receiver_province=receiver_area[0:receiver_area.index("-")]
        receiver_area=receiver_area[receiver_area.index("-")+1:len(receiver_area)]
        receiver_city=receiver_area[0:receiver_area.index("-")]
        receiver_district=receiver_area[receiver_area.index("-")+1:len(receiver_area)]
        Product_Data=[]
        #时间戳
        paytime = time.mktime(receiverDate.timetuple())
        Payment_Data="[{\"payment\":0,\"paytime\":\""+str(paytime)[0:str(paytime).find(".")]+"000"+"\",\"pay_type_code\":\"zhifubao\"}]"
        #Payment_Data="[{\"payment\":0,\"paytime\":\"1522744133796\",\"pay_type_code\":\"001\"}]"
        ProductList="select * from MD_Product where Id=%d"%productId
        cur.execute(ProductList)
        ProductList = cur.fetchall()
        #添加订单产品
        if(len(ProductList)!=0):
            product_data={}
            for j in list(range(0,len(ProductList))):
                product_data="[{\"item_code\":\""+ProductList[j][1]+"\",\"qty\":%d,\"price\":0,\"note\":null,\"refund\":0,\"oid\":null,\"sku_code\":null}]"%quantity
                Product_Data.append(product_data)
                create_data = "{\"appkey\":\"" + AppId + "\",\"method\":\"gy.erp.trade.get\",\"sessionkey\":\"" + SessionKey + "\",\"order_type_code\":\"其它订单\",\"platform_code\":\""\
                + plantformId + "\",\"shop_code\":\"月月送\",\"vip_code\":\"" + vipCode + "\",\"buyer_memo\":\""+str(remark)+"\",\"warehouse_code\":\"107\",\"express_code\":\"STO\",\"receiver_name\":\""+receiver_name+"\",\"receiver_province\":\""\
                +receiver_province+"\",\"receiver_city\":\""+receiver_city+"\",\"receiver_district\":\""+receiver_district+"\",\"receiver_mobile\":\""+receiver_mobile+"\",\"receiver_zip\":\"200000\",\"receiver_address\":\""\
                +receiver_address+"\",\"deal_datetime\":\""+str(receiverDate)+"\",\"details\":"+str(product_data)+",\"payments\":" + str(Payment_Data) +"}"
        #判断发货日期
        receiverDate=receiverDate.strftime("%Y-%m-%d")
        if(receiverDate==time.strftime("%Y-%m-%d", time.localtime())):
            CreateData_List.append(create_data)
        #CreateData_List.append(create_data)#测试
    conn.commit()
    conn.close()
    return CreateData_List

#获取jsonList
def createOrder(orderList):
    #出错尝试
    try_times=0
    for i in range(0,len(orderList)):
        result=createSingleOrder(orderList[i],try_times)
        if(result!=True):
            #记录创建出错订单
            CreateRecord("Fail","订单: "+json.loads(orderList[i])["platform_code"]+"创建失败！",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'),"1")
        else:
            CreateRecord("UploadSuccess","订单: "+json.loads(orderList[i])["platform_code"]+"创建成功！",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'),"1")
        #更新订单数据
        platform_code=json.loads(orderList[i])
        platform_code=platform_code["platform_code"]
        conn=DBConnection()
        cur = conn.cursor()
        update_order="update MD_Order set upload_status=1 where order_code='%s'"%platform_code
        cur.execute(update_order)
        conn.commit()
        conn.close()
        #break
    return True

#创建单个ERP订单
def createSingleOrder(order,try_times):
    API_Url = "http://v2.api.guanyierp.com/rest/erp_open"
    info = order[:-1] + ",\"sign\":\"" + sign(order, AppSecret) + "\"}"
    print(info)
    headers = {"Content-type": "application/json"} 
    content = info.encode('utf-8')
    request = urllib.request.Request(url=API_Url, method='POST', data=content, headers=headers)
    response = urllib.request.urlopen(request)
    response_json = response.read()
    if(json.loads(response_json.decode("utf-8"))["success"]!=True):
        #出错尝试10次
        if(try_times>10):
            try_times=0
            return json.loads(response_json.decode("utf-8"))["errorCode"]+"/"+json.loads(response_json.decode("utf-8"))["errorDesc"]
        try_times+=1
        return createSingleOrder(order,try_times)
    return True

#查询数据库中前一天订单数据
def getExpressInfo(start_time,end_time):
    get_times=1
    suc_list=[]
    conn = DBConnection()
    cur = conn.cursor()
    OrderList="select * from MD_Order where delivery_state=0 and receiver_date>'"+start_time+"' and receiver_date<'"+end_time+"'"
    cur.execute(OrderList)
    orders = cur.fetchall()
    for i in list(range(0,len(orders))):
        express_information=getSingelExpressInfo(orders[i][1],get_times)
        if(express_information!=None):
            #更新订单数据
            update_order="update MD_Order set delivery_state=2,express_information='"+str(express_information)+"' where order_code='"+orders[i][1]+"'"
            suc_list.append(orders[i][1]+" ")
            cur.execute(update_order)
    cur = conn.cursor()
    conn.commit()
    conn.close()
    #写成功日志
    #CreateRecord(""+str(len(suc_list))+"个订单物流获取成功！",""+str(suc_list).replace('\'','')+"",""+datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')+"")
    max_record=20
    if(len(suc_list)>max_record):
        for i in range(0,len(suc_list)//max_record):
            CreateRecord("DownloadSuccess",""+ str(suc_list[i*max_record:i*max_record+max_record-1]).replace('\'','')+ "",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'),str(max_record))
        CreateRecord("DownloadSuccess",""+ str(suc_list[len(suc_list)//max_record*max_record:len(suc_list)]).replace('\'','')+ "",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'),str(len(suc_list)-len(suc_list)//max_record*max_record))
    else:
        CreateRecord("DownloadSuccess",""+ str(suc_list).replace('\'','')+ "",datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'),str(len(suc_list)))
    return True

#更新前一天订单物流信息
def getSingelExpressInfo(order_code,get_times):
    method = "gy.erp.trade.get"
    data = "{\"appkey\":\"" + AppId + "\",\"method\":\"" + method + "\",\"sessionkey\":\"" + SessionKey + "\",\"platform_code\":\""+order_code+"\"}"
    info = data[:-1] + ",\"sign\":\"" + sign(data,AppSecret) + "\"}"
    headers = {"Content-type": "application/json"} 
    content = info.encode('utf-8')
    request = urllib.request.Request(url=API_Url, method='POST', data=content, headers=headers)
    response = urllib.request.urlopen(request)
    response_json = response.read()
    response_json=json.loads(response_json.decode("utf-8"))
    if(response_json["success"]==True):
        for i in range(0,len(response_json["orders"])):
            #判断订单有无物流信息
            if(len(response_json["orders"][0]["deliverys"])!=0):
                express_name=response_json["orders"][0]["deliverys"][0]["express_name"]
                mail_no=response_json["orders"][0]["deliverys"][0]["mail_no"]
                express_information=express_name+':'+mail_no
                receiver_mobile = response_json["orders"][0]["receiver_mobile"]
                #print(send_Msg(mail_no,receiver_mobile)) # 发送短消息
                return express_information
            else:
                return None
    else:
        #延迟4秒，出错尝试5次
        time.sleep(5)
        if(get_times>10):
            print(response_json)
            get_times=0
            CreateRecord("Fail","订单: "+ order_code +" 物流信息获取失败！",""+datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')+"","1")
            return None
        get_times+=1
        return getSingelExpressInfo(order_code,get_times)

#日志记录
def CreateRecord(type,detail,time,amount):
    conn=DBConnection()
    cur = conn.cursor()
    record="insert into MD_Record (record_date,record_type,record_detail,record_amount) values ('"+time+"','"+type+"','"+detail+"','"+amount+"')"
    cur.execute(record)
    conn.commit()
    conn.close()

def datetime_offset_by_month(datetime1, n = 1):
    one_day = datetime.timedelta(days = 1)
    q,r = divmod(datetime1.month + n, 12)
    datetime2 = datetime.datetime(
        datetime1.year + q, r + 1, 1) - one_day
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2
    if datetime1.day >= datetime2.day:
        return datetime2
    return datetime2.replace(day = datetime1.day)

def findStr(string, subStr, findCnt):
    listStr = string.split(subStr,findCnt)
    return len(string)-len(listStr[-1])-len(subStr)

def send_Msg(text, mobile):
    sms_host = "sms.yunpian.com"
    Apikey = "2100e8a41c376ef6c6a18114853393d7"
    MsgUrl = "https://sms.yunpian.com/v2/sms/single_send.json"
    port = "443"
    MsgText = "【寿全斋】您的验证码是"+"text"
    Msgmobile = "15921503329"
    params = ({'apikey': Apikey, 'text': MsgText, 'mobile':Msgmobile})
    data = parse.urlencode(params).encode('utf-8')
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", MsgUrl, data, headers)
    response = conn.getresponse()
    response_str = response.read()
    response_str = json.loads(response_str.decode("utf-8"))
    conn.close()
    return response_str

if __name__ == '__main__':
    AppId = "130412" 
    AppSecret = "26d2e926f42a4f2181dd7d1b7f7d55c0"
    SessionKey = "8a503b3d9d0d4119be2868cc69a8ef5a"
    API_Url = "http://v2.api.guanyierp.com/rest/erp_open"
    y_Time = datetime.date.today() + datetime.timedelta(days=-1)
    Time =  y_Time.strftime("%Y-%m-%d 00:00:00")
    getExpressInfo(Time,datetime.date.today().strftime("%Y-%m-%d 00:00:00"))
    #getOrders(Time)
    #createOrder(getDBData())
    #input("Press Enter")