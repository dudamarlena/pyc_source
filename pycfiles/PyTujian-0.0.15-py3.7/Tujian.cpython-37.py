# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyTujian/Tujian.py
# Compiled at: 2020-04-18 06:54:29
# Size of source mod 2**32: 868 bytes
from . import Http, print2
import sys

def getData(url):
    print2.print2.message('获取中...')
    data = Http.getJson(url)
    print2.print2.message('\r')
    if data == 1:
        return 1
    return data


def getSort():
    try:
        return getData('https://v2.api.dailypics.cn/sort')['result']
    except:
        return 1


def getToday():
    return getData('https://v2.api.dailypics.cn/today')


def getSortList():
    data = getSort()
    if data == 1:
        return 1
    sort = {}
    for v in data:
        sort[v['TID']] = v['T_NAME']

    return sort


def getArchive(TID, page):
    return getData('https://v2.api.dailypics.cn/list/?page=%s&size=15&sort=%s' % (page, TID))


def getWebLink(PID):
    return 'https://www.dailypics.cn/member/id/%s' % PID


def getPicData(PID):
    return getData('https://v2.api.dailypics.cn/member?id=%s' % PID)