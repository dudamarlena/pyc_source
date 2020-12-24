# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\workspace\test01\xmind2Excel\xmind2Excel\main.py
# Compiled at: 2019-07-02 07:31:52
# Size of source mod 2**32: 621 bytes
__author__ = '8034.com'
__date__ = '2018-11-08'
import sys
print(sys.getdefaultencoding())
import os
FILE_PATH = os.path.dirname(os.path.realpath(__file__))

class Main(object):
    if sys.version[:1] > '2':
        from xmind2Excel.ui3 import Application
    else:
        from xmind2Excel.ui3 import Application
    app = Application()
    app.master.title('Xmind转为xls文件-通用版')
    favicon_path = os.path.join(FILE_PATH, 'favicon.ico')
    app.master.iconbitmap(favicon_path)
    app.master.mainloop()