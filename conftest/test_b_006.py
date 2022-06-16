import pytest
import pandas as pd
import json
import requests
import datetime
import bs4
import sys
import re
from time import sleep
true=True
false=False
null=None
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
def last_year_today():
    year_x=int(datetime.datetime.now().strftime('%Y'))-1
    month_x=int(datetime.datetime.now().strftime('%m'))
    day_x=int(datetime.datetime.now().strftime('%d'))
    today_x=datetime.date(year_x,month_x,day_x)
    return today_x,year_x,month_x,day_x
last_year_today_date=last_year_today()[0]
def last_year_tomorrow():
    year_x=int(datetime.datetime.now().strftime('%Y'))-1
    month_x=int(datetime.datetime.now().strftime('%m'))
    day_x=int(datetime.datetime.now().strftime('%d'))+1
    today_x=datetime.date(year_x,month_x,day_x)
    return today_x,year_x,month_x,day_x
last_year_tomorrow_date=last_year_tomorrow()[0]
#######################################################################################################
def test_a(kl_head):
    try:
        
        data={
                "_t":"1652360355",
                "orgIds":"2",
                "date":str(today_date),
                "chartIds":"172,173,175,176,178,180,189,190,191"
            }

        response=kl_head['sessions'].get(url=kl_head['url']+"/report/report/day/mall?",params=data,headers=kl_head['headers'])
        response=response.json()
        today_kl={}
        tomorrow_kl={}
        Last_week_kl={}
        for x in response['data']['body']['customeradd']['series']:
            if x['name']=='当日':
                for i,n in enumerate(range(8,23)):
                    if n< 21:
                        today_kl['%s:00'% n]=x['data'][i]
                    else:
                        today_kl['%s:00'% n]=response['data']['head']['dayInnum']
            elif x['name']=='昨日':
                for i,n in enumerate(range(8,23)):
                    tomorrow_kl['%s:00'% n]=x['data'][i]
            elif x['name']=='上周同期':
                for i,n in enumerate(range(8,23)):
                    Last_week_kl['%s:00'% n]=x['data'][i]
            else:
                '没有数据'

        data=[today_kl,tomorrow_kl,Last_week_kl]
        df=pd.DataFrame(data,index=['当日','昨日','上周同期'])
        number=int(df.loc['当日','%d:00'% (int(kl_head['tohour'])-1)])
        data={
                    "time":"%s_%s_kl"%(today_date,kl_head['tohour']),
                    "sale":number
                 }
        Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
        print('时间：%s_%s \n 客流：%s'%(today_date,kl_head['tohour'],number))
    except:
        raise
#######################################################################################################
def test_b(kl_head):
    try:
        
        data={
                "_t":"1652360355",
                "orgIds":"2",
                "date":str(last_year_today_date),
                "chartIds":"172,173,175,176,178,180,189,190,191"
            }

        response=kl_head['sessions'].get(url=kl_head['url']+"/report/report/day/mall?",params=data,headers=kl_head['headers'])
        response=response.json()
        today_kl={}
        tomorrow_kl={}
        Last_week_kl={}
        for x in response['data']['body']['customeradd']['series']:
            if x['name']=='当日':
                for i,n in enumerate(range(8,23)):
                    if n< 21:
                        today_kl['%s:00'% n]=x['data'][i]
                    else:
                        today_kl['%s:00'% n]=response['data']['head']['dayInnum']
            elif x['name']=='昨日':
                for i,n in enumerate(range(8,23)):
                    tomorrow_kl['%s:00'% n]=x['data'][i]
            elif x['name']=='上周同期':
                for i,n in enumerate(range(8,23)):
                    Last_week_kl['%s:00'% n]=x['data'][i]
            else:
                '没有数据'

        data=[today_kl,tomorrow_kl,Last_week_kl]
        df=pd.DataFrame(data,index=['当日','昨日','上周同期'])
        number=int(df.loc['当日','%d:00'% (int(kl_head['tohour'])-1)])
        data={
                    "time":"%s_%s_kl"%(last_year_today_date,kl_head['tohour']),
                    "sale":number
                 }
        Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
        print('时间：%s_%s \n 客流：%s'%(last_year_today_date,kl_head['tohour'],number))
    except:
        raise
#######################################################################################################
def test_c(kl_head):
    try:
        
        data={
                "_t":"1652360355",
                "orgIds":"2",
                "date":str(last_year_tomorrow_date),
                "chartIds":"172,173,175,176,178,180,189,190,191"
            }

        response=kl_head['sessions'].get(url=kl_head['url']+"/report/report/day/mall?",params=data,headers=kl_head['headers'])
        response=response.json()
        today_kl={}
        tomorrow_kl={}
        Last_week_kl={}
        for x in response['data']['body']['customeradd']['series']:
            if x['name']=='当日':
                for i,n in enumerate(range(8,23)):
                    if n< 21:
                        today_kl['%s:00'% n]=x['data'][i]
                    else:
                        today_kl['%s:00'% n]=response['data']['head']['dayInnum']
            elif x['name']=='昨日':
                for i,n in enumerate(range(8,23)):
                    tomorrow_kl['%s:00'% n]=x['data'][i]
            elif x['name']=='上周同期':
                for i,n in enumerate(range(8,23)):
                    Last_week_kl['%s:00'% n]=x['data'][i]
            else:
                '没有数据'

        data=[today_kl,tomorrow_kl,Last_week_kl]
        df=pd.DataFrame(data,index=['当日','昨日','上周同期'])
        number=int(df.loc['当日','%d:00'% (int(kl_head['tohour'])-1)])
        data={
                    "time":"%s_%s_kl"%(last_year_tomorrow_date,kl_head['tohour']),
                    "sale":number
                 }
        Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
        print('时间：%s_%s \n 客流：%s'%(last_year_tomorrow_date,kl_head['tohour'],number))
    except:
        raise
#######################################################################################################