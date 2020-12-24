# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/util.py
# Compiled at: 2018-08-16 20:17:34
import datetime

def print_time(message):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print '%s:%s' % (nowTime, message)