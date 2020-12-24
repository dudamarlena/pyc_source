# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/sr/config.py
# Compiled at: 2019-03-23 05:34:26
"""
配置文件
"""
import os, time
project_path = os.path.abspath(os.path.dirname(__file__))
screen_folder = os.path.join(project_path, 'screen_folder')
if not os.path.exists(screen_folder):
    os.mkdir(screen_folder)
screen_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
screen_png = os.path.join(screen_folder, str(screen_time + '_截图.png'))
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
chrome_driver_path = PATH('../entity/chromedriver_mac')