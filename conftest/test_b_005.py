import pytest
import pandas as pd
import json
import requests
import datetime
import bs4
import re
from time import sleep
now_a=datetime.datetime.now().strftime('%Y/%m/%d/')
now_b=datetime.datetime.now().strftime('%Y年%m月%d日')
false=False
true=True
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
            "validation-code":head['validation_code'],
            "message-type":1,
            "update-info":{
                "focus-eid":"",
                "update-uielements":{
                },
                "actions":[
                    {
                        "eid":head['eid_statistical'],
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
        response=head['sessions'].post(url=head['url'],data=json.dumps(data),headers=head['headers'])
        file=open('./zz.text',mode='w')
        file.write(response.text)
        file.close()
        

        print(response.url)
        print(head['url'])
        print(head['headers'])
        response=response.json()
        validation_code=response['validation-code']
    except:
        raise
    ##################################################################################################################
    try:
        data={
            "validation-code":head['validation_code'],
            "message-type":1,
            "update-info":{
                "focus-eid":"",
                "update-uielements":{
                },
                "actions":[
                    {
                        "eid":"_e_542",
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
        response=head['sessions'].post(url=head['url'],data=json.dumps(data),headers=head['headers'])
        # response=response.json()
        # validation_code=response['validation-code']
        print(response)
        print(response.text)
    except:
        raise
    ##################################################################################################################
    
    ##################################################################################################################
    
    ##################################################################################################################
    
    ##################################################################################################################