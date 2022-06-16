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
# 今年昨天
year=int(datetime.datetime.now().strftime('%Y'))
month=int(datetime.datetime.now().strftime('%m'))
day=int(datetime.datetime.now().strftime('%d')) 
last_year_yesterday=int(day)-1
if month==1 and last_year_yesterday==0:
    last_year=year-1
    last_year_month=12
    last_year_yesterday=calendar.monthrange(last_year,last_year_month)[-1]
    last_year_yesterday_date=datetime.date(last_year,last_year_month,last_year_yesterday)
elif last_year_yesterday==0:
    last_year=year
    last_year_month=month-1
    last_year_yesterday=calendar.monthrange(last_year,last_year_month)[-1]
    last_year_yesterday_date=datetime.date(last_year,last_year_month,last_year_yesterday)
else:
    last_year=year
    last_year_month=month
    last_year_yesterday_date=datetime.date(last_year,last_year_month,last_year_yesterday)
today_date=last_year_yesterday_date
# 去年昨日
year=int(datetime.datetime.now().strftime('%Y'))
month=int(datetime.datetime.now().strftime('%m'))
day=int(datetime.datetime.now().strftime('%d')) 
last_year=int(year)-1
last_year_yesterday=int(day)-1
if month==1 and last_year_yesterday==0:
    last_year=last_year-1
    last_year_month=12
    last_year_yesterday=calendar.monthrange(last_year,last_year_month)[-1]
    last_year_yesterday_date=datetime.date(last_year,last_year_month,last_year_yesterday)
elif last_year_yesterday==0:
    last_year=last_year
    last_year_month=month-1
    last_year_yesterday=calendar.monthrange(last_year,last_year_month)[-1]
    last_year_yesterday_date=datetime.date(last_year,last_year_month,last_year_yesterday)
else:
    last_year=last_year
    last_year_month=month
    last_year_yesterday_date=datetime.date(last_year,last_year_month,last_year_yesterday)
last_year_today_date=last_year_yesterday_date
# 去年今日
year=int(datetime.datetime.now().strftime('%Y'))
month=int(datetime.datetime.now().strftime('%m'))
day=int(datetime.datetime.now().strftime('%d')) 
last_year=int(year)-1
last_year_month=month
last_year_today=day
last_year_tomorrow_date=datetime.date(last_year,last_year_month,last_year_today)
tohour=22


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
        number=int(df.loc['当日','%d:00'% (int(tohour)-1)])
        data={
                    "time":"%s_%s_kl"%(today_date,tohour),
                    "sale":number
                 }
        Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
        print('时间：%s_%s \n 客流：%s'%(today_date,tohour,number))
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
        number=int(df.loc['当日','%d:00'% (int(tohour)-1)])
        data={
                    "time":"%s_%s_kl"%(last_year_today_date,tohour),
                    "sale":number
                 }
        Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
        print('时间：%s_%s \n 客流：%s'%(last_year_today_date,tohour,number))
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
        number=int(df.loc['当日','%d:00'% (int(tohour)-1)])
        data={
                    "time":"%s_%s_kl"%(last_year_tomorrow_date,tohour),
                    "sale":number
                 }
        Way_a().sql_insert(configs['database_config']['period_of_time_sale_table'],data)
        print('时间：%s_%s \n 客流：%s'%(last_year_tomorrow_date,tohour,number))
    except:
        raise
#######################################################################################################