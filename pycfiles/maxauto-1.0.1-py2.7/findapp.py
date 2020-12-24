# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/max/report/findapp.py
# Compiled at: 2018-12-05 10:16:00
"""
查询app路径
"""
import os

def find_app(folder_path):
    app_path = ''
    for file in os.listdir(folder_path):
        if file.startswith('app_'):
            app_path = os.path.join(folder_path, file)
            print ('app路径:{}').format(app_path)
            break

    return app_path