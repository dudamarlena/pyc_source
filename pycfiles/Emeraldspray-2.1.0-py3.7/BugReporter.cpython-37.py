# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Es\BugReporter.py
# Compiled at: 2019-12-18 21:44:29
# Size of source mod 2**32: 996 bytes
import requests, os, sys

class BugReporter:

    def __init__(self):
        if os.path.exists('error.log'):
            errorlog = open('error.log', mode='r', encoding='utf-8')
            sender = errorlog.read()
            requests.get('https://sc.ftqq.com/SCU44058T44cff9901b6466371f4ae9be28645f945c57ed47b8bb0.send?text=软件错误报告 & desp=' + sender)
            errorlog.close()
            os.remove('error.log')
            quit()
        else:
            requests.get('https://sc.ftqq.com/SCU44058T44cff9901b6466371f4ae9be28645f945c57ed47b8bb0.send?text=软件错误报告 & desp=未成功获取到错误报告')
            quit()