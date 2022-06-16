# -*- coding: utf-8 -*-
__author__ = "wowo"


import pytest
import json
import requests
import datetime
import bs4
import sys
import re
from time import sleep
sys.path.append("../")
from comm.ways import Way_a#公共文件
#关闭https证书报错
requests.packages.urllib3.disable_warnings()
###################################################
now_a=datetime.datetime.now().strftime('%Y/%m/%d/')
now_b=datetime.datetime.now().strftime('%Y年%m月%d日')
false=False
true=True
oa_user=Way_a().sql_select_login_user("wfj_user",'oa')
url_oa=oa_user["url"]
username_oa=oa_user["username"]
password_oa=oa_user["password"]
kl_user=Way_a().sql_select_login_user("wfj_user",'kl')
url_kl=kl_user["url"]
username_kl=kl_user["username"]
password_kl=kl_user["password"]




@pytest.fixture(scope='session')    
def oa_head():
    tohour=datetime.datetime.now().strftime('%H')
    #######################################################################################################
    sessions=requests.session()
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
            "Accept":"*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection":"keep-alive"
           }

    #######################################################################################################
    try:
        response=sessions.get(url=url_oa+"/wfj",headers=headers)
        soup=bs4.BeautifulSoup(response.text,'html.parser')
        magic_1=soup.input['value']
    except:
        raise
    #######################################################################################################
    try:
        data={"magic1":magic_1,
            "magic2":"Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/100.0.4896.60%20Safari/537.36__zh-CN",
            "redirect":"true"}
        response=sessions.post(url=url_oa+"/wfj",data=data,headers=headers)
        headers["Referer"]=response.url
        soup=bs4.BeautifulSoup(response.text,'html.parser')
        sessionId=eval(str(soup.find('body')).split('('or')')[1].split(',')[0])
        verificationCode=eval(str(soup.find('body')).split('('or')')[1].split(',')[1])
        validation_code=eval(str(soup.find('body')).split('('or')')[1].split(',')[2])
        print(sessionId,verificationCode,validation_code)
    except:
        raise
    #######################################################################################################
    try:
        sleep(1)
        headers['x-requested-with']='XMLHttpRequest'
        headers['Content-Type']='text/plain'
        url=url_oa+"/dnaserver?sessionId=%s&verificationCode=%s&entryName=wfj&uiType=browser2&serviceId=synchronize"%(sessionId,verificationCode)
        data={
                "validation-code":validation_code,
                "message-type":0,
                "client-info":{
                    "os-name":"windows",
                    "os-bit":32,
                    "client-language":"zh-CN",
                    "screen-width":1920,
                    "screen-height":1080,
                    "browser-type":"chrome",
                    "cookie-data":"",
                    "date-format":str(now_a),
                    "dpi-x":96
                }
            }
        response=sessions.post(url=url,data=json.dumps(data),headers=headers)
        response=response.json()
        validation_code=response['validation-code']
        eid=response['iframes'][0]
    except:
        raise
    ######################################################################################################
    try:
        data={
            "serviceId":"browser-script-render2",
            "sessionId":sessionId,
            "verificationCode":verificationCode,
            "entryName":"bap",
            "uiType":"browser2",
            "eid":eid
            }
        response=sessions.get(url=url_oa+"/dnaserver?",params=data,headers=headers)
        response=response.json()
        for i,n in enumerate(response['server-update']):
            if 'init' in n:
                if 'client_object_data' in n['init']:
                    if n['init']['client_object_data']['placeholder']=='用户名':
                        eid_login=response['server-update'][i-1]['eid']
                        eid_username=n['eid']
                    else:
                        pass
                    if n['init']['client_object_data']['placeholder']=='密码':
                        eid_password=n['eid']
                    else:
                        pass
                else:
                    pass
            else:
                pass
    except:
        raise
    #####################################################################################################
    try:
        sleep(1)
        data={
            "validation-code":validation_code,
            "message-type":1,
            "update-info":{
                "focus-eid":eid_password,
                "update-uielements":{
                    eid_username:{
                        "selectionStartedPosition":9,
                        "selectionEndedPosition":9,
                        "text":username_oa
                    },
                    eid_password:{
                        "selectionStartedPosition":10,
                        "selectionEndedPosition":10,
                        "text":password_oa
                    }
                },
                "actions":[
                    {
                        "eid":eid_login,
                        "name":"input_clientnotify_event"
                    }
                ]
            }
        }
        response=sessions.post(url=url,data=json.dumps(data),headers=headers)
        print('登录成功')
        response=response.json()
        validation_code=response['validation-code']
        eid=[]
        for i in response['server-update']:
            if 'init' in i:
                if 'text' in i['init']:
                    if i['init']['text']=='POS系统':
                        eid.append(i['eid'])
                    if i['init']['text']=='[T]统计分析':
                        eid.append(i['eid'])
                    else:
                        pass
                else:
                    pass
                
            else:
                pass
    except:
        raise
    eid_pos=eid[1]
    eid_statistical=eid[3]
    #####################################################################################################
    oa_head={"sessions":sessions,
                "headers":headers,
                "url":url,
                "eid_pos":eid_pos,
                "eid_statistical":eid_statistical,
                "validation_code":validation_code,
                "tohour":tohour}
    return oa_head
    


@pytest.fixture(scope='session')    
def kl_head():
    tohour=datetime.datetime.now().strftime('%H')
    #######################################################################################################
    sessions=requests.session()
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
            "Accept":"application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Referer": "http://10.88.101.5/",
            "Content-Type":"application/json;charset=UTF-8"
           }
    #######################################################################################################
    try:
        data={
                "loginName":username_kl,
                "password":password_kl
             }
        response=sessions.post(url=url_kl+"/report/users/login",data=json.dumps(data),headers=headers)
        response=response.json()
        cookies_dict={
                "userId":str(response['data']['user']['id']),
                "atoken":str(response['data']['atoken']),
                "rtoken":str(response['data']['rtoken']),
                "user_unid":str(response['data']['user_unid']),
                "user_type":str(response['data']['user_type']),
                "unid":str(response['data']['user']['unid']),
                "username":str(response['data']['user_name']),
                "orgId":str(response['data']['user']['accountId']),
                "accountName":"%E9%9B%86%E5%9B%A2",
                "mallName":"%E5%B7%B4%E4%B8%AD%E7%8E%8B%E5%BA%9C%E4%BA%95%E8%B4%AD%E7%89%A9%E4%B8%AD%E5%BF%83"
                    }
        sessions.cookies.update(cookies_dict)
        headers['authorization']=str(response['data']['atoken'])
    except:
        raise
    #######################################################################################################
    kl_head={"sessions":sessions,
                "headers":headers,
                "url":url_kl,
                "tohour":tohour
          }
    return kl_head