import pytest
import pandas as pd
import json
import requests
import datetime
import bs4
import sys
import re
from time import sleep
now_a=datetime.datetime.now().strftime('%Y/%m/%d/')
now_b=datetime.datetime.now().strftime('%Y年%m月%d日')
false=False
true=True
sys.path.append("../")
from comm.ways import Way_a#公共文件
configs=Way_a().config()
def today():
    year_x=int(datetime.datetime.now().strftime('%Y'))
    month_x=int(datetime.datetime.now().strftime('%m'))
    day_x=int(datetime.datetime.now().strftime('%d'))
    today_x=datetime.date(year_x,month_x,day_x)
    return today_x,year_x,month_x,day_x
today_date=today()[0]
toyear=today()[1]
tomonth=today()[2]
today=today()[3]




def test_a(oa_head):
    ##################################################################################################################
    try:
        data={
            "validation-code":oa_head['validation_code'],
            "message-type":1,
            "update-info":{
                "focus-eid":"",
                "update-uielements":{
                },
                "actions":[
                    {
                        "eid":oa_head['eid_pos'],
                        "name":"input_click_event",
                        "value":{
                            "key-ctrl":false,
                            "key-shift":false,
                            "key-alt":false
                        }
                    }
                ]
            }
        }
        response=oa_head['sessions'].post(url=oa_head['url'],data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        for i in response['server-update']:
            if 'init' in i:
                if 'url' in i['init']:
                    data_url=i['init']['url']         
                else:
                    pass
            else:
                pass 
    except:
        raise
    ##################################################################################################################
    try:
        response=oa_head['sessions'].get(url='http://slb.wfjmall.cn:9910'+ data_url,headers=oa_head['headers'])
        response_referer=response.url
        soup=bs4.BeautifulSoup(response.text,'html.parser')
        bap_url=soup.select('form[id=logonForm]')[0]['action']
    except:
        raise
    ##################################################################################################################
    try:
        sleep(1)
        print('登录收银机')
        oa_head['headers']['Referer']=response_referer
        response=oa_head['sessions'].post(url=bap_url,headers=oa_head['headers'],verify=False)
        soup=bs4.BeautifulSoup(response.text,'html.parser')
        sessionId=soup.select('input[name=sessionId]')[0]['value']
        verificationCode=soup.select('input[name=verificationCode]')[0]['value']
        entryName=soup.select('input[name=entryName]')[0]['value']
        entryArgs=soup.select('input[name=entryArgs]')[0]['value']
        redirect=soup.select('input[name=redirect]')[0]['value']
    except:
        raise
    ##################################################################################################################
    try:
        oa_head['headers']["Referer"]=response.url
        data={"sessionId":sessionId,
                "verificationCode":verificationCode,
                "entryName":entryName,
                "entryArgs":entryArgs,
                "userAgent":oa_head['headers']['User-Agent'],
                "clientLanguage":"zh-CN",
                "redirect":redirect}
        response=oa_head['sessions'].post(url='https://slb.wfjmall.cn:9718/bap',params=data,headers=oa_head['headers'],verify=False)
        soup=bs4.BeautifulSoup(response.text,'html.parser')
        sessionId=eval(str(soup.find('body')).split('('or')')[1].split(',')[0])
        verificationCode=eval(str(soup.find('body')).split('('or')')[1].split(',')[1])
        validation_code=eval(str(soup.find('body')).split('('or')')[1].split(',')[2])
    except:
        raise
    ##################################################################################################################
    url="https://slb.wfjmall.cn:9718/dnaserver?sessionId=%s&verificationCode=%s&entryName=bap&uiType=browser2&serviceId=synchronize"%(sessionId,verificationCode)
    ##################################################################################################################
    try:
        data={
            "validation-code":validation_code,
            "message-type":0,
            "client-info":{
                "os-name":"windows",
                "os-bit":32,
                "client-language":"zh-CN",
                "screen-width":1920,
                "screen-height":1080,
                "view-width":1880,
                "view-height":563,
                "browser-type":"chrome",
                "browser-version":86,
                "cookie-data":"",
                "date-format":now_a,
                "dpi-x":96
            }
        }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        for i in response['server-update']:
            if 'init' in i:
                if 'text' in i['init']:
                    if i['init']['text']=='每日毛利查询':
                        eid_258=i['eid']
                        break
                    else:
                        pass
                else:
                    pass
            else:
                pass
    except:
        raise
    ##################################################################################################################
    try:
        data={
            "validation-code":validation_code,
            "message-type":1,
            "update-info":{
                "focus-eid":"_e_69",
                "update-uielements":{
                },
                "actions":[
                    {
                        "eid":eid_258,
                        "name":"input_click_event",
                        "value":{
                            "key-ctrl":false,
                            "key-shift":false,
                            "key-alt":false
                        }
                    }
                ]
            }
        }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        eid_484=response['iframes'][-1]
    except:
        raise
    ##################################################################################################################
    try:
        data={
            "serviceId":"browser-script-render2",
            "sessionId":sessionId,
            "verificationCode":verificationCode,
            "entryName":"bap",
            "uiType":"browser2",
            "eid":eid_484
            }
        response=oa_head['sessions'].get(url="https://slb.wfjmall.cn:9718/dnaserver?",params=data,headers=oa_head['headers'])
        response=response.json()
        list_date=[]
        list_year=[]
        list_month=[]
        for i,n in enumerate(response['server-update']):
            if 'init' in n:
                if 'text_description' in n['init']:
                    if '年'and'月'and'日' in n['init']['text_description']:
                        eid=n['eid']
                        list_date.append(eid)
                    else:
                        pass
                else:
                    pass
                if 'text' in n['init']:
                    if n['init']['text'] == '年  ':
                        eid=response['server-update'][i-1]['eid']
                        list_year.append(eid)
                    else:  
                        pass
                    if n['init']['text'] == '月  ':
                        eid=response['server-update'][i-1]['eid']
                        list_month.append(eid)
                    else:
                        pass
                    if n['init']['text']=='确定':
                        eid_566=n['eid']
                    else:
                        pass
                else:
                    pass
            else:
                pass
        eid_520=list_date[0]
        eid_538=list_date[1]
        eid_527=list_year[0]
        eid_545=list_year[1]
        eid_529=list_month[0]
        eid_547=list_month[1]
    except:
        raise
    ##################################################################################################################
    data={
            "validation-code":validation_code,
            "message-type":1,
            "update-info":{
                "focus-eid":eid_566,
                "update-uielements":{
                    eid_520:{
                        "text_description":"%s年%s月%s日"%(toyear,tomonth,today),
                        "popup_visible":false,
                        "selectionStartedPosition":10,
                        "selectionEndedPosition":10,
                        "text":"%s-%s-%s"%(toyear,tomonth,today)
                    },
                    eid_527:{
                        "text":toyear,
                        "selection":toyear
                    },
                    eid_529:{
                        "text":tomonth,
                        "selection":tomonth
                    },
                    eid_538:{
                        "text_description":"%s年%s月%s日"%(toyear,tomonth,today),
                        "popup_visible":false,
                        "selectionStartedPosition":10,
                        "selectionEndedPosition":10,
                        "text":"%s-%s-%s"%(toyear,tomonth,today)
                    },
                    eid_545:{
                        "text":toyear,
                        "selection":toyear
                    },
                    eid_547:{
                        "text":tomonth,
                        "selection":tomonth
                    },

                    eid_566:{
                        "selection":false
                    }
                },
                "actions":[
                    {
                        "eid":eid_566,
                        "name":"input_action_event"
                    }
                ]
            }
        }
    response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
    response=response.json()
    validation_code=response['validation-code']
    eid_582=response['iframes'][0]
    ##################################################################################################################
    try:
        data={
            "serviceId":"browser-script-render2",
            "sessionId":sessionId,
            "verificationCode":verificationCode,
            "entryName":"bap",
            "uiType":"browser2",
            "eid":eid_582
            }
        response=oa_head['sessions'].get(url="https://slb.wfjmall.cn:9718/dnaserver?",params=data,headers=oa_head['headers'])
        response=response.json()
        list_date=[]
        list_year=[]
        list_month=[]
        for i,n in enumerate(response['server-update']):
            if 'init' in n:
                if 'text_description' in n['init']:
                    if '年'and'月'and'日' in n['init']['text_description']:
                        eid=n['eid']
                        list_date.append(eid)
                        print(n['init']['text_description'])
                    else:
                        pass
                else:
                    pass
                if 'text' in n['init']:
                    if n['init']['text'] == '年  ':
                        eid=response['server-update'][i-1]['eid']
                        list_year.append(eid)
                    else:  
                        pass
                    if n['init']['text'] == '月  ':
                        eid=response['server-update'][i-1]['eid']
                        list_month.append(eid)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        eid_620=list_date[0]
        eid_638=list_date[1]
        eid_627=list_year[0]
        eid_645=list_year[1]
        eid_629=list_month[0]
        eid_647=list_month[1]
        
    except:
        raise
    ##################################################################################################################
    try:
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":"",
                    "update-uielements":{
                        eid_620:{
                            "text_description":"%s年%s月%s日"%(toyear,tomonth,today)
                        },
                        eid_627:{
                            "text":toyear,
                            "selection":toyear
                        },
                        eid_629:{
                            "text":tomonth,
                            "selection":tomonth
                        },
                        eid_638:{
                            "text_description":"%s年%s月%s日"%(toyear,tomonth,today)
                        },
                        eid_645:{
                            "text":toyear,
                            "selection":toyear
                        },
                        eid_647:{
                            "text":tomonth,
                            "selection":tomonth
                        },
                    },
                    "actions":[

                    ]
                }
            }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        for x in response['server-update']:
            if x['etype']=='GridGC':
                for y in x['update']:
                    if 'fullUpdate' in y:
                        if len(eval(y['fullUpdate']['initValue'])['cells']['rowList'])<4:
                            data=eval(y['fullUpdate']['initValue'])['cells']['rowList']
                            columns_x=[]
                            data_list_a=[]
                            for i,n in enumerate(data):
                                if i==0:
                                    continue
                                elif i==1:
                                    for z,c in enumerate(n):
                                        if z==0:
                                            continue
                                        else:
                                            columns_x.append(c['1'])
                                else:
                                    data_list_b=[]
                                    data_list_a.append(data_list_b)
                                    for q,e in enumerate(n):
                                        if q==0:
                                            continue
                                        else:
                                            data_list_b.append(e['1'])

                            df_data=pd.DataFrame(data_list_a,columns=columns_x)
                            data={
                                        "time":"%s_%s_rml"%(today_date,oa_head['tohour']),
                                        "sale":0.00
                                     }
                            Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
                            print('没有数据')
                        else:
                            data=eval(y['fullUpdate']['initValue'])['cells']['rowList']
                            columns_x=[]
                            data_list_a=[]
                            for i,n in enumerate(data):
                                if i==0:
                                    continue
                                elif i==1:
                                    for z,c in enumerate(n):
                                        if z==0:
                                            continue
                                        else:
                                            columns_x.append(c['1'])
                                else:
                                    data_list_b=[]
                                    data_list_a.append(data_list_b)
                                    for q,e in enumerate(n):
                                        if q==0:
                                            continue
                                        else:
                                            data_list_b.append(e['1'])

                            df_data=pd.DataFrame(data_list_a,columns=columns_x)
                            data={
                                        "time":"%s_%s_rml"%(today_date,oa_head['tohour']),
                                        "sale":df_data.loc[0,'调整后毛利']
                                     }
                            Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
                            print("日毛利：%s" % df_data.loc[0,'调整后毛利'])
                    else:
                        pass
            else:
                pass
    except:
        raise
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    
    

def test_b(oa_head):
    ##################################################################################################################
    try:
        data={
            "validation-code":oa_head['validation_code'],
            "message-type":1,
            "update-info":{
                "focus-eid":"",
                "update-uielements":{
                },
                "actions":[
                    {
                        "eid":oa_head['eid_pos'],
                        "name":"input_click_event",
                        "value":{
                            "key-ctrl":false,
                            "key-shift":false,
                            "key-alt":false
                        }
                    }
                ]
            }
        }
        response=oa_head['sessions'].post(url=oa_head['url'],data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        for i in response['server-update']:
            if 'init' in i:
                if 'url' in i['init']:
                    data_url=i['init']['url']         
                else:
                    pass
            else:
                pass 
    except:
        raise
    ##################################################################################################################
    try:
        response=oa_head['sessions'].get(url='http://slb.wfjmall.cn:9910'+ data_url,headers=oa_head['headers'])
        response_referer=response.url
        soup=bs4.BeautifulSoup(response.text,'html.parser')
        bap_url=soup.select('form[id=logonForm]')[0]['action']
    except:
        raise
    ##################################################################################################################
    try:
        sleep(1)
        print('登录收银机')
        oa_head['headers']['Referer']=response_referer
        response=oa_head['sessions'].post(url=bap_url,headers=oa_head['headers'],verify=False)
        soup=bs4.BeautifulSoup(response.text,'html.parser')
        sessionId=soup.select('input[name=sessionId]')[0]['value']
        verificationCode=soup.select('input[name=verificationCode]')[0]['value']
        entryName=soup.select('input[name=entryName]')[0]['value']
        entryArgs=soup.select('input[name=entryArgs]')[0]['value']
        redirect=soup.select('input[name=redirect]')[0]['value']
    except:
        raise
    ##################################################################################################################
    try:
        oa_head['headers']["Referer"]=response.url
        data={"sessionId":sessionId,
                "verificationCode":verificationCode,
                "entryName":entryName,
                "entryArgs":entryArgs,
                "userAgent":oa_head['headers']['User-Agent'],
                "clientLanguage":"zh-CN",
                "redirect":redirect}
        response=oa_head['sessions'].post(url='https://slb.wfjmall.cn:9718/bap',params=data,headers=oa_head['headers'],verify=False)
        soup=bs4.BeautifulSoup(response.text,'html.parser')
        sessionId=eval(str(soup.find('body')).split('('or')')[1].split(',')[0])
        verificationCode=eval(str(soup.find('body')).split('('or')')[1].split(',')[1])
        validation_code=eval(str(soup.find('body')).split('('or')')[1].split(',')[2])
    except:
        raise
    ##################################################################################################################
    url="https://slb.wfjmall.cn:9718/dnaserver?sessionId=%s&verificationCode=%s&entryName=bap&uiType=browser2&serviceId=synchronize"%(sessionId,verificationCode)
    ##################################################################################################################
    try:
        data={
            "validation-code":validation_code,
            "message-type":0,
            "client-info":{
                "os-name":"windows",
                "os-bit":32,
                "client-language":"zh-CN",
                "screen-width":1920,
                "screen-height":1080,
                "view-width":1880,
                "view-height":563,
                "browser-type":"chrome",
                "browser-version":86,
                "cookie-data":"",
                "date-format":now_a,
                "dpi-x":96
            }
        }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        for i in response['server-update']:
            if 'init' in i:
                if 'text' in i['init']:
                    if i['init']['text']=='每日毛利查询':
                        eid_258=i['eid']
                        break
                    else:
                        pass
                else:
                    pass
            else:
                pass
    except:
        raise
    ##################################################################################################################
    try:
        data={
            "validation-code":validation_code,
            "message-type":1,
            "update-info":{
                "focus-eid":"_e_69",
                "update-uielements":{
                },
                "actions":[
                    {
                        "eid":eid_258,
                        "name":"input_click_event",
                        "value":{
                            "key-ctrl":false,
                            "key-shift":false,
                            "key-alt":false
                        }
                    }
                ]
            }
        }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        eid_484=response['iframes'][-1]
    except:
        raise
    ##################################################################################################################
    try:
        data={
            "serviceId":"browser-script-render2",
            "sessionId":sessionId,
            "verificationCode":verificationCode,
            "entryName":"bap",
            "uiType":"browser2",
            "eid":eid_484
            }
        response=oa_head['sessions'].get(url="https://slb.wfjmall.cn:9718/dnaserver?",params=data,headers=oa_head['headers'])
        response=response.json()
        list_date=[]
        list_year=[]
        list_month=[]
        for i,n in enumerate(response['server-update']):
            if 'init' in n:
                if 'text_description' in n['init']:
                    if '年'and'月'and'日' in n['init']['text_description']:
                        eid=n['eid']
                        list_date.append(eid)
                    else:
                        pass
                else:
                    pass
                if 'text' in n['init']:
                    if n['init']['text'] == '年  ':
                        eid=response['server-update'][i-1]['eid']
                        list_year.append(eid)
                    else:  
                        pass
                    if n['init']['text'] == '月  ':
                        eid=response['server-update'][i-1]['eid']
                        list_month.append(eid)
                    else:
                        pass
                    if n['init']['text']=='确定':
                        eid_566=n['eid']
                    else:
                        pass
                else:
                    pass
            else:
                pass
        eid_520=list_date[0]
        eid_538=list_date[1]
        eid_527=list_year[0]
        eid_545=list_year[1]
        eid_529=list_month[0]
        eid_547=list_month[1]
    except:
        raise
    ##################################################################################################################
    data={
            "validation-code":validation_code,
            "message-type":1,
            "update-info":{
                "focus-eid":eid_566,
                "update-uielements":{
                    eid_520:{
                        "text_description":"%s年%s月1日"%(toyear,tomonth),
                        "popup_visible":false,
                        "selectionStartedPosition":10,
                        "selectionEndedPosition":10,
                        "text":"%s-%s-01"%(toyear,tomonth)
                    },
                    eid_527:{
                        "text":toyear,
                        "selection":toyear
                    },
                    eid_529:{
                        "text":tomonth,
                        "selection":tomonth
                    },
                    eid_538:{
                        "text_description":"%s年%s月%s日"%(toyear,tomonth,today),
                        "popup_visible":false,
                        "selectionStartedPosition":10,
                        "selectionEndedPosition":10,
                        "text":"%s-%s-%s"%(toyear,tomonth,today)
                    },
                    eid_545:{
                        "text":toyear,
                        "selection":toyear
                    },
                    eid_547:{
                        "text":tomonth,
                        "selection":tomonth
                    },

                    eid_566:{
                        "selection":false
                    }
                },
                "actions":[
                    {
                        "eid":eid_566,
                        "name":"input_action_event"
                    }
                ]
            }
        }
    response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
    response=response.json()
    validation_code=response['validation-code']
    eid_582=response['iframes'][0]
    ##################################################################################################################
    try:
        data={
            "serviceId":"browser-script-render2",
            "sessionId":sessionId,
            "verificationCode":verificationCode,
            "entryName":"bap",
            "uiType":"browser2",
            "eid":eid_582
            }
        response=oa_head['sessions'].get(url="https://slb.wfjmall.cn:9718/dnaserver?",params=data,headers=oa_head['headers'])
        response=response.json()
        list_date=[]
        list_year=[]
        list_month=[]
        for i,n in enumerate(response['server-update']):
            if 'init' in n:
                if 'text_description' in n['init']:
                    if '年'and'月'and'日' in n['init']['text_description']:
                        eid=n['eid']
                        list_date.append(eid)
                        print(n['init']['text_description'])
                    else:
                        pass
                else:
                    pass
                if 'text' in n['init']:
                    if n['init']['text'] == '年  ':
                        eid=response['server-update'][i-1]['eid']
                        list_year.append(eid)
                    else:  
                        pass
                    if n['init']['text'] == '月  ':
                        eid=response['server-update'][i-1]['eid']
                        list_month.append(eid)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        eid_620=list_date[0]
        eid_638=list_date[1]
        eid_627=list_year[0]
        eid_645=list_year[1]
        eid_629=list_month[0]
        eid_647=list_month[1]
        
    except:
        raise
    ##################################################################################################################
    try:
        data={
            "validation-code":validation_code,
            "message-type":1,
            "update-info":{
                "focus-eid":"",
                "update-uielements":{
                    eid_620:{
                        "text_description":"%s年%s月1日"%(toyear,tomonth)
                    },
                    eid_627:{
                        "text":toyear,
                        "selection":toyear
                    },
                    eid_629:{
                        "text":tomonth,
                        "selection":tomonth
                    },
                    eid_638:{
                        "text_description":"%s年%s月%s日"%(toyear,tomonth,today)
                    },
                    eid_645:{
                        "text":toyear,
                        "selection":toyear
                    },
                    eid_647:{
                        "text":tomonth,
                        "selection":tomonth
                    },
                },
                "actions":[

                ]
            }
        }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        for x in response['server-update']:
            if x['etype']=='GridGC':
                for y in x['update']:
                    if 'fullUpdate' in y:
                        if len(eval(y['fullUpdate']['initValue'])['cells']['rowList'])<4:
                            data=eval(y['fullUpdate']['initValue'])['cells']['rowList']
                            columns_x=[]
                            data_list_a=[]
                            for i,n in enumerate(data):
                                if i==0:
                                    continue
                                elif i==1:
                                    for z,c in enumerate(n):
                                        if z==0:
                                            continue
                                        else:
                                            columns_x.append(c['1'])
                                else:
                                    data_list_b=[]
                                    data_list_a.append(data_list_b)
                                    for q,e in enumerate(n):
                                        if q==0:
                                            continue
                                        else:
                                            data_list_b.append(e['1'])

                            df_data=pd.DataFrame(data_list_a,columns=columns_x)
                            data={
                                        "time":"%s_%s_yml"%(today_date,oa_head['tohour']),
                                        "sale":0.00
                                     }
                            Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
                            print('没有数据')
                        else:
                            data=eval(y['fullUpdate']['initValue'])['cells']['rowList']
                            columns_x=[]
                            data_list_a=[]
                            for i,n in enumerate(data):
                                if i==0:
                                    continue
                                elif i==1:
                                    for z,c in enumerate(n):
                                        if z==0:
                                            continue
                                        else:
                                            columns_x.append(c['1'])
                                else:
                                    data_list_b=[]
                                    data_list_a.append(data_list_b)
                                    for q,e in enumerate(n):
                                        if q==0:
                                            continue
                                        else:
                                            data_list_b.append(e['1'])

                            df_data=pd.DataFrame(data_list_a,columns=columns_x)
                            data={
                                        "time":"%s_%s_yml"%(today_date,oa_head['tohour']),
                                        "sale":df_data.loc[0,'调整后毛利']
                                     }
                            Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
                            print("月毛利：%s"% df_data.loc[0,'调整后毛利'])
                    else:
                        pass
            else:
                pass
    except:
        raise