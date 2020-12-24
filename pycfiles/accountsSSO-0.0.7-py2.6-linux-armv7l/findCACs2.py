# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/accountingModules/findCACs2.py
# Compiled at: 2012-04-13 07:37:24
import sys, csv, time, datetime, re, numpy as np
from accountingModules.structures import *
from accountingModules.myUtilities import stringToDate, addMonthsToDate
import accountingModules.theGlobals as globalConf

def find_active_cacs(projdb, keyword, date_start, date_end):
    date_to = stringToDate(date_end, '%Y%m%d')
    date_from = stringToDate(date_start, '%Y%m%d')
    cac_dict = {}
    cac_reader = csv.reader(open(projdb, 'r'), delimiter='\t')
    cluster = globalConf.cluster
    cores_per_node = int(globalConf.cores_per_node)
    for row in cac_reader:
        try:
            if re.search(keyword, str(row)):
                if row[7] == cluster:
                    theCAC = Cac_details()
                    cac_startDate = str(row[4])
                    cac_duration = int(row[5])
                    cac_startDate = stringToDate(cac_startDate, '%Y%m%d')
                    expiryDate = addMonthsToDate(cac_startDate, cac_duration)
                    if expiryDate > date_from and cac_startDate < date_to:
                        theCAC.setStartDate(cac_startDate)
                        theCAC.setExpiryDate(expiryDate)
                        theCAC.setPI(row[1])
                        nodehours = int(row[3])
                        corehours = nodehours * cores_per_node
                        theCAC.setAllocatedHours(corehours)
                        cac_dict[row[0]] = theCAC
        except:
            raise

    return cac_dict