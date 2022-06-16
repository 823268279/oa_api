# -*- coding: utf-8 -*-
__author__ = "wowo"
import pytest
import datetime
import os
import sys
import time
import smtplib
import schedule
import pandas as pd
from calendar import calendar, month
from openpyxl import load_workbook
from openpyxl.styles import *
from zhdate import ZhDate
import calendar 
sys.path.append("../")
from comm.ways import Way_a,Way_b,Smtp,DataBase_user_add#公共文件

# DataBase_user_add().database_qq_email()
# DataBase_user_add().database_user()

def start_a():
    if __name__ == "__main__":
        now_time='%s' % datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        print('start:%s'% str(now_time))
        pytest.main(['-s','-v','../conftest/test_a_001.py::test_a'],)
        pytest.main(['-s','-v','../conftest/test_a_001.py::test_b'],)
        pytest.main(['-s','-v','../conftest/test_a_002.py::test_a'],)
        pytest.main(['-s','-v','../conftest/test_a_002.py::test_b'],)
        pytest.main(['-s','-v','../conftest/test_a_003.py::test_a'],)
        pytest.main(['-s','-v','../conftest/test_a_003.py::test_b'],)
        pytest.main(['-s','-v','../conftest/test_a_004.py::test_a'],)
        pytest.main(['-s','-v','../conftest/test_a_004.py::test_b'],)
        pytest.main(['-s','-v','../conftest/test_a_006.py'],)
        Way_a().create_excel()
        Smtp().send_mail_img()
        print('end:%s'% str(now_time))



def start_b():
    if __name__ == "__main__":
        now_time='%s' % datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        print('start:%s'% str(now_time))
        pytest.main(['-s','-v','../conftest/test_b_001.py::test_a'],)
        pytest.main(['-s','-v','../conftest/test_b_001.py::test_b'],)
        pytest.main(['-s','-v','../conftest/test_b_002.py::test_a'],)
        pytest.main(['-s','-v','../conftest/test_b_002.py::test_b'],)
        pytest.main(['-s','-v','../conftest/test_b_003.py::test_a'],)
        pytest.main(['-s','-v','../conftest/test_b_003.py::test_b'],)
        pytest.main(['-s','-v','../conftest/test_b_004.py::test_a'],)
        pytest.main(['-s','-v','../conftest/test_b_004.py::test_b'],)
        pytest.main(['-s','-v','../conftest/test_b_006.py'],)
        Way_b().create_excel()
        Smtp().send_mail_img()
        print('end:%s'% str(now_time))



#每天的10:30执行一次任务  
schedule.every().day.at("09:30").do(start_a)  
#每天的10:30执行一次任务  
schedule.every().day.at("12:01").do(start_b)   
#每天的10:30执行一次任务  
schedule.every().day.at("15:01").do(start_b)  
#每天的10:30执行一次任务  
schedule.every().day.at("18:01").do(start_b)  
#每天的10:30执行一次任务  
schedule.every().day.at("20:01").do(start_b)  
#每天的10:00执行一次任务  
schedule.every().day.at("22:00").do(start_b)  
print('wait......')
while True:
    #运行所有可以运行的任务
    run_pending: schedule.run_pending() 