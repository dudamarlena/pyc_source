# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelleconnector/investmentcategory.py
# Compiled at: 2020-01-24 12:19:03
# Size of source mod 2**32: 2852 bytes
"""
Created on Mon Jul 15 23:14:15 2019
This program identifies various investment categories
 based on rating and region
@author: debmishra
"""
from lykkelleconf.connecteod import connect
import psycopg2 as pgs
grade = {'AAA':'Prime', 
 'AA+':'High Grade',  'AA':'High Grade',  'AA-':'High Grade', 
 'A+':'UM Grade',  'A':'UM Grade',  'A-':'UM Grade', 
 'BBB+':'LM Grade',  'BBB':'LM Grade',  'BBB-':'LM Grade', 
 'BB+':'Non-Inv Grade',  'BB':'Non-Inv Grade', 
 'BB-':'Non-Inv Grade',  'B+':'High Yield', 
 'B':'High Yield',  'B-':'High Yield', 
 'NR':'Not Rated'}

class investmentcategory:

    def __init__(self):
        conn = connect.create()
        cursor = conn.cursor()
        with conn:
            sel = 'select country, region, rating from benchmark_all'
            cursor.execute(sel)
            myselection = cursor.fetchall()
            length = len(myselection)
            c = 0
            brow = []
            for i in range(length):
                mysel = myselection[i]
                country = mysel[0]
                region = mysel[1]
                rating = mysel[2]
                if region == 'Europe':
                    inv_category = 'EU_' + grade.get(rating, 'Sub-Prime')
                else:
                    if region == 'Asia':
                        inv_category = 'AS_' + grade.get(rating, 'Sub-Prime')
                    else:
                        if region == 'Africa':
                            inv_category = 'AF_' + grade.get(rating, 'Sub-Prime')
                        else:
                            if region == 'NAmerica':
                                inv_category = 'NA_' + grade.get(rating, 'Sub-Prime')
                            else:
                                if region == 'SAmerica':
                                    inv_category = 'SA_' + grade.get(rating, 'Sub-Prime')
                                else:
                                    if region == 'Oceania':
                                        inv_category = 'OC_' + grade.get(rating, 'Sub-Prime')
                                    else:
                                        print('unknown region ' + region + '. Adjust region in the benchmark_all table')
                                        inv_category = None
                upd = 'update benchmark_all set mkt_type=%s where country=%s and region =%s and rating =%s'
                try:
                    cursor.execute(upd, (inv_category, country, region, rating))
                    c = c + 1
                except pgs.Error as e:
                    try:
                        print(e.pgerror)
                        brow.append(country)
                    finally:
                        e = None
                        del e

            print('updated investment category for ', c, 'records successfully')
            if brow != []:
                print('could not update few records and they are ', brow)
            else:
                print('all records successfully loaded')
        print('postgres connection closed')