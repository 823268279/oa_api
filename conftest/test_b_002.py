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
#去年今日
def last_year_today():
    year_x=int(datetime.datetime.now().strftime('%Y'))-1
    month_x=int(datetime.datetime.now().strftime('%m'))
    day_x=int(datetime.datetime.now().strftime('%d'))
    today_x=datetime.date(year_x,month_x,day_x)
    return today_x,year_x,month_x,day_x
last_year_today_date=last_year_today()[0]
toyear=last_year_today()[1]
tomonth=last_year_today()[2]
today=last_year_today()[3]




def test_a(oa_head):
    shops_type=1
    sum=true# #false表示都不选择
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
                    if i['init']['text']=='时段销售_按商户':
                        eid_245=i['eid']
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
                        "eid":eid_245,
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
        eid_484=response['iframes'][1]
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
        eid_list=[]
        for i,n in enumerate(response['server-update']):
            if 'init' in n:
                if 'text_description' in n['init']:
                    eid_list.append(n['eid'])
                else:
                    pass
                if 'text' in n['init']:
                    if n['init']['text'] == '年  ':
                        eid_495=response['server-update'][i-1]['eid']
                    else:  
                        pass
                    if n['init']['text'] == '月  ':
                        eid_497=response['server-update'][i-1]['eid']
                    else:
                        pass
                    if n['init']['text']=='确定':
                        eid_556=n['eid']
                    else:
                        pass
        eid_488=eid_list[0]
        eid_516=eid_list[2]
        eid_540=eid_list[-2]
    except:
        raise
    ##################################################################################################################
    try:
        # #修改日期
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":eid_516,
                    "update-uielements":{
                        eid_488:{
                            "text_description":"%s年%s月%s日"%(toyear,tomonth,today),
                            "selectionStartedPosition":6,
                            "selectionEndedPosition":6,
                            "text":"%s-%s-%s"%(toyear,tomonth,today),
                            "popup_visible":false
                        },
                        eid_495:{
                            "text":toyear,
                            "selection":toyear
                        },
                        eid_497:{
                            "text":tomonth,
                            "selection":tomonth
                        },
                        eid_516:{
                            "selectionStartedPosition":1,
                            "selectionEndedPosition":1,
                            "text":"1"
                        }
                    },
                    "actions":[
                        {
                            "eid":eid_516,
                            "name":"input_text_event",
                            "value":{
                                "custom1":1
                            }
                        }
                    ]
                }
            }   
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        eid_516=response['focus-eid']
    except:
        raise
    ##################################################################################################################
    try:
        #修改截至时间
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":eid_516,
                    "update-uielements":{
                        eid_516:{
                            "text":str(oa_head['tohour']),
                            "selectionStartedPosition":2,
                            "selectionEndedPosition":2
                        },
                    },
                    "actions":[
                        {
                            "eid":eid_516,
                            "name":"input_text_event",
                            "value":{
                                "custom1":1
                            }
                        }
                    ]
                }
            }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
    except:
        raise
    ##################################################################################################################
    try:
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":eid_540,
                    "update-uielements":{
                        eid_516:{
                            "popup_visible":false,
                            "client_object":{
                                "INPUT_DATA":{
                                    "KEYUP":false,
                                    "FOCUSLOST":true
                                }
                            }
                        }
                    },
                    "actions":[
                        {
                            "eid":eid_516,
                            "name":"input_panel_event",
                            "value":{
                                "method-name":"panelClose",
                                "custom3":"popup_close_cancel"
                            }
                        },
                        {
                            "eid":eid_516,
                            "name":"input_clientnotify_event"
                        }
                    ]
                }
            }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        for i in response['server-update']:
            if i['type']==1 and i['etype']=='LWList':
                eid_572=i['eid']
        for i in response['server-update']:
            if 'update'in i:
                if 'client_data'in i['update'][0]:
                    eid_514=i['eid']
                    client_data=i['update'][0]['client_data']
                else:
                    pass
            else:
                pass
    except:
        raise
    #################################################################################################################
    try:
        #修改商户类型
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":eid_540,
                    "update-uielements":{
                        eid_514:{
                            "client_data":str(client_data)
                        },
                        eid_540:{
                            "text":str(shops_type)
                        }
                    },
                    "actions":[
                        {
                            "eid":eid_540,
                            "name":"input_text_event",
                            "value":{
                                "custom1":1
                            }
                        }
                    ]
                }
            }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
    except:
        raise
    #################################################################################################################
    try:
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":"_e_556",
                    "update-uielements":{
                        eid_540:{
                            "selectionStartedPosition":1,
                            "selectionEndedPosition":1,
                            "popup_visible":false,
                            "client_object":{
                                "INPUT_DATA":{
                                    "KEYUP":false,
                                    "FOCUSLOST":true
                                }
                            }
                        },
                        "_e_556":{
                            "selection":false
                        }
                    },
                    "actions":[
                        {
                            "eid":eid_540,
                            "name":"input_panel_event",
                            "value":{
                                "method-name":"panelClose",
                                "custom3":"popup_close_cancel"
                            }
                        },
                        {
                            "eid":eid_540,
                            "name":"input_clientnotify_event"
                        },
                        {
                            "eid":"_e_556",
                            "name":"input_action_event"
                        }
                    ]
                }
            }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        eid_581=response['iframes'][0]
    except:
        raise
    #################################################################################################################
    try:
        data={
            "serviceId":"browser-script-render2",
            "sessionId":sessionId,
            "verificationCode":verificationCode,
            "entryName":"bap",
            "uiType":"browser2",
            "eid":eid_581
            }
        response=oa_head['sessions'].get(url="https://slb.wfjmall.cn:9718/dnaserver?",params=data,headers=oa_head['headers'])
        response=response.json()
        for i,n in enumerate(response['server-update']):
            if 'init' in n:
                if 'text_description' in n['init']:
                    if '年'and'月'and'日' in n['init']['text_description']:
                        eid_587=n['eid']
                        date_text_description=n['init']['text_description']
                        print('查询时间：%s'% date_text_description)
                        year_text=(n['init']['text']).split('-')[0]
                        month_text=(n['init']['text']).split('-')[1]
                    else:
                        pass
                    if n['init']['text_description'] in ['联营','租赁','联营,租赁']:
                        shops_type_text_description=n['init']['text_description']
                        print('查询商户类型：%s'% shops_type_text_description)
                    else:
                        pass
                    if n['init']['text_description'] in ['12','15','18','20','22']:
                        as_of_time_text_description=n['init']['text_description']
                        print('截至时间：%s'% as_of_time_text_description)
                    else:
                        pass
                else:
                    pass
                if 'text' in n['init']:
                    if n['init']['text'] == '年  ':
                        eid_594=response['server-update'][i-1]['eid']
                    else:  
                        pass
                    if n['init']['text'] == '月  ':
                        eid_596=response['server-update'][i-1]['eid']
                    else:
                        pass
                else:
                    pass
            else:
                pass
    except:
        raise
    ################################################################################################################
    try:
        data={
            "validation-code":validation_code,
            "message-type":1,
            "update-info":{
                "focus-eid":"",
                "update-uielements":{
                    eid_587:{
                        "text_description":date_text_description
                    },
                    eid_594:{
                        "text":year_text,
                        "selection":year_text
                    },
                    eid_596:{
                        "text":month_text,
                        "selection":month_text
                    },
                },
                "actions":[

                ]
            }
        }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        if len(response['server-update'][1]['update'])<2:
            response_xx=response['server-update'][1]['update'][0]
            def get_data(data):
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
                return df_data
            df_money=get_data(response_xx)
            data={
                    "time":"%s_%s_ly"%(last_year_today_date,oa_head['tohour']),
                    "sale":0.00
                 }
            Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
            print('没有数据')
        else:
            response_xx=eval(response['server-update'][1]['update'][2]['fullUpdate']['initValue'])['cells']['rowList']
            def get_data(data):
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
                return df_data
            df_money=get_data(response_xx)
            data={
                    "time":"%s_%s_ly"%(last_year_today_date,oa_head['tohour']),
                    "sale":df_money.loc[0,'折扣后金额']
                 }
            Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
            print(df_money.loc[0,'折扣后金额'])
    except:
        raise
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    
    

def test_b(oa_head):
    shops_type=3
    sum=true# #false表示都不选择
    #####################################################################################################
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
    #####################################################################################################
    try:
        response=oa_head['sessions'].get(url='http://slb.wfjmall.cn:9910'+ data_url,headers=oa_head['headers'])
        response_referer=response.url
        soup=bs4.BeautifulSoup(response.text,'html.parser')
        bap_url=soup.select('form[id=logonForm]')[0]['action']
    except:
        raise
    #####################################################################################################
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
    #####################################################################################################
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
                    if i['init']['text']=='时段销售_按商户':
                        eid_245=i['eid']
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
                        "eid":eid_245,
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
        eid_484=response['iframes'][1]
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
        eid_list=[]
        for i,n in enumerate(response['server-update']):
            if 'init' in n:
                if 'text_description' in n['init']:
                    eid_list.append(n['eid'])
                else:
                    pass
                if 'text' in n['init']:
                    if n['init']['text'] == '年  ':
                        eid_495=response['server-update'][i-1]['eid']
                    else:  
                        pass
                    if n['init']['text'] == '月  ':
                        eid_497=response['server-update'][i-1]['eid']
                    else:
                        pass
                    if n['init']['text']=='确定':
                        eid_556=n['eid']
                    else:
                        pass
        eid_488=eid_list[0]
        eid_516=eid_list[2]
        eid_540=eid_list[-2]
    except:
        raise
    ##################################################################################################################
    try:
        # #修改日期
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":eid_516,
                    "update-uielements":{
                        eid_488:{
                            "text_description":"%s年%s月%s日"%(toyear,tomonth,today),
                            "selectionStartedPosition":6,
                            "selectionEndedPosition":6,
                            "text":"%s-%s-%s"%(toyear,tomonth,today),
                            "popup_visible":false
                        },
                        eid_495:{
                            "text":toyear,
                            "selection":toyear
                        },
                        eid_497:{
                            "text":tomonth,
                            "selection":tomonth
                        },
                        eid_516:{
                            "selectionStartedPosition":1,
                            "selectionEndedPosition":1,
                            "text":"1"
                        }
                    },
                    "actions":[
                        {
                            "eid":eid_516,
                            "name":"input_text_event",
                            "value":{
                                "custom1":1
                            }
                        }
                    ]
                }
            }   
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        eid_516=response['focus-eid']
    except:
        raise
    ##################################################################################################################
    try:
        #修改截至时间
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":eid_516,
                    "update-uielements":{
                        eid_516:{
                            "text":str(oa_head['tohour']),
                            "selectionStartedPosition":2,
                            "selectionEndedPosition":2
                        },
                    },
                    "actions":[
                        {
                            "eid":eid_516,
                            "name":"input_text_event",
                            "value":{
                                "custom1":1
                            }
                        }
                    ]
                }
            }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
    except:
        raise
    ##################################################################################################################
    try:
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":eid_540,
                    "update-uielements":{
                        eid_516:{
                            "popup_visible":false,
                            "client_object":{
                                "INPUT_DATA":{
                                    "KEYUP":false,
                                    "FOCUSLOST":true
                                }
                            }
                        }
                    },
                    "actions":[
                        {
                            "eid":eid_516,
                            "name":"input_panel_event",
                            "value":{
                                "method-name":"panelClose",
                                "custom3":"popup_close_cancel"
                            }
                        },
                        {
                            "eid":eid_516,
                            "name":"input_clientnotify_event"
                        }
                    ]
                }
            }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        for i in response['server-update']:
            if i['type']==1 and i['etype']=='LWList':
                eid_572=i['eid']
        for i in response['server-update']:
            if 'update'in i:
                if 'client_data'in i['update'][0]:
                    eid_514=i['eid']
                    client_data=i['update'][0]['client_data']
                else:
                    pass
            else:
                pass
    except:
        raise
    #################################################################################################################
    try:
        #修改商户类型
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":eid_540,
                    "update-uielements":{
                        eid_514:{
                            "client_data":str(client_data)
                        },
                        eid_540:{
                            "text":str(shops_type)
                        }
                    },
                    "actions":[
                        {
                            "eid":eid_540,
                            "name":"input_text_event",
                            "value":{
                                "custom1":1
                            }
                        }
                    ]
                }
            }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
    except:
        raise
    #################################################################################################################
    try:
        data={
                "validation-code":validation_code,
                "message-type":1,
                "update-info":{
                    "focus-eid":"_e_556",
                    "update-uielements":{
                        eid_540:{
                            "selectionStartedPosition":1,
                            "selectionEndedPosition":1,
                            "popup_visible":false,
                            "client_object":{
                                "INPUT_DATA":{
                                    "KEYUP":false,
                                    "FOCUSLOST":true
                                }
                            }
                        },
                        "_e_556":{
                            "selection":false
                        }
                    },
                    "actions":[
                        {
                            "eid":eid_540,
                            "name":"input_panel_event",
                            "value":{
                                "method-name":"panelClose",
                                "custom3":"popup_close_cancel"
                            }
                        },
                        {
                            "eid":eid_540,
                            "name":"input_clientnotify_event"
                        },
                        {
                            "eid":"_e_556",
                            "name":"input_action_event"
                        }
                    ]
                }
            }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        eid_581=response['iframes'][0]
    except:
        raise
    #################################################################################################################
    try:
        data={
            "serviceId":"browser-script-render2",
            "sessionId":sessionId,
            "verificationCode":verificationCode,
            "entryName":"bap",
            "uiType":"browser2",
            "eid":eid_581
            }
        response=oa_head['sessions'].get(url="https://slb.wfjmall.cn:9718/dnaserver?",params=data,headers=oa_head['headers'])
        response=response.json()
        for i,n in enumerate(response['server-update']):
            if 'init' in n:
                if 'text_description' in n['init']:
                    if '年'and'月'and'日' in n['init']['text_description']:
                        eid_587=n['eid']
                        date_text_description=n['init']['text_description']
                        print('查询时间：%s'% date_text_description)
                        year_text=(n['init']['text']).split('-')[0]
                        month_text=(n['init']['text']).split('-')[1]
                    else:
                        pass
                    if n['init']['text_description'] in ['联营','租赁','联营,租赁']:
                        shops_type_text_description=n['init']['text_description']
                        print('查询商户类型：%s'% shops_type_text_description)
                    else:
                        pass
                    if n['init']['text_description'] in ['12','15','18','20','22']:
                        as_of_time_text_description=n['init']['text_description']
                        print('截至时间：%s'% as_of_time_text_description)
                    else:
                        pass
                else:
                    pass
                if 'text' in n['init']:
                    if n['init']['text'] == '年  ':
                        eid_594=response['server-update'][i-1]['eid']
                    else:  
                        pass
                    if n['init']['text'] == '月  ':
                        eid_596=response['server-update'][i-1]['eid']
                    else:
                        pass
                else:
                    pass
            else:
                pass
    except:
        raise
    ################################################################################################################
    try:
        data={
            "validation-code":validation_code,
            "message-type":1,
            "update-info":{
                "focus-eid":"",
                "update-uielements":{
                    eid_587:{
                        "text_description":date_text_description
                    },
                    eid_594:{
                        "text":year_text,
                        "selection":year_text
                    },
                    eid_596:{
                        "text":month_text,
                        "selection":month_text
                    },
                },
                "actions":[

                ]
            }
        }
        response=oa_head['sessions'].post(url=url,data=json.dumps(data),headers=oa_head['headers'])
        response=response.json()
        validation_code=response['validation-code']
        if len(response['server-update'][1]['update'])<2:
            response_xx=response['server-update'][1]['update'][0]
            def get_data(data):
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
                return df_data
            df_money=get_data(response_xx)
            data={
                    "time":"%s_%s_zl"%(last_year_today_date,oa_head['tohour']),
                    "sale":0.00
                 }
            Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
            print('没有数据')
        else:
            response_xx=eval(response['server-update'][1]['update'][2]['fullUpdate']['initValue'])['cells']['rowList']
            def get_data(data):
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
                return df_data
            df_money=get_data(response_xx)
            data={
                    "time":"%s_%s_zl"%(last_year_today_date,oa_head['tohour']),
                    "sale":df_money.loc[0,'折扣后金额']
                 }
            Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
            print(df_money.loc[0,'折扣后金额'])
    except:
        raise
    ##################################################################################################################
