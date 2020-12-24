# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\documentation.py
# Compiled at: 2015-05-13 08:51:42
# Size of source mod 2**32: 178 bytes
import os, subprocess

def handler(page):
    if page == 'index':
        subprocess.Popen(os.path.dirname(__file__) + '/doc/_build/html/index.html', shell=True)