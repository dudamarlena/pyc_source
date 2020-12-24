# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/util.py
# Compiled at: 2018-08-16 20:17:34
import datetime

def print_time(message):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print '%s:%s' % (nowTime, message)