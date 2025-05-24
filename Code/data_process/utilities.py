'''
Descripttion: 
Author: Ruifeng Xu
version: 1.0
Date: 2024-11-22 23:34:26
LastEditors: Ruifeng Xu
LastEditTime: 2024-12-14 05:26:09
'''

import logging
import pandas as pd
import os
from datetime import  datetime
import re
from loguru import logger


def advanceday(x, day):

   day = int(day)
   if (int(x[4:7]) - day <= 0):
       x = str(int(x[:4]) - 1) + f"{((int(x[4:])+365)-day):03d}"
   else:
       x = str(int(x[:4])) + f"{(int(x[4:]) - day):03d}"
   return x
def delayday(x, day):
   day = int(day)
   if x!= -99 and x!= "":
       if (int(x[4:7]) + day >= 365):
           x = (str(int(x[:4]) + 1) + f"{(int(x[4:7])-365+day):03d}")
       else:
           x = str(int(x[:4])) + f"{(int(x[4:7])+day):03d}"
   return x
def differday(x, y):
   y_dir = int(x[:4]) - int(y[:4])
   day_dir = int(x[4:7]) - int(y[4:7]) + y_dir * 365
   return day_dir

def nafun(x, y):
   if x == -99 or x == None:
       x = y
   return x


def rad(df):
   # df = df[~df.duplicated(subset=['date'], keep='first')]
   cluname = df.columns[0]

   df = df.sort_values(by = cluname,ascending=True)
   df = df.drop_duplicates()
   return df
def rad_irrigation(df):
   # df = df[~df.duplicated(subset=['date'], keep='first')]
   cluname = df.columns[0]
   cluname_date = df.columns[1]
   df = df.sort_values(by = [cluname,cluname_date],ascending=[True,True])
   df = df.drop_duplicates()
   return df

def transformday(FDATE, FERTI, PDATE):

    if FERTI == 'R' and len(str(FDATE)) < 5:
        if PDATE == -99 or PDATE == None:
            PDATE = -99
        else:
            FDATE = delayday(PDATE, FDATE)
    else:
        FDATE = FDATE
    if FERTI == 'D' and len(str(FDATE)) == 7:
        if PDATE == -99 or PDATE == None:
            PDATE = -99
        else:
            FDATE = differday(FDATE, PDATE)
    else:
        FDATE = FDATE
    return FDATE

def rad_fertilization(df):
   # df = df[~df.duplicated(subset=['date'], keep='first')]
   cluname = df.columns[0]
   cluname_date = df.columns[1]
   df = df.sort_values(by = [cluname,cluname_date],ascending=[True,True])
   df = df.drop_duplicates()
   return df
