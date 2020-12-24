# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\lib\File.py
# Compiled at: 2018-11-23 10:10:08
import codecs, os

class FSO:

    def __int__(self):
        self.verison = 'v1.0'

    def createfile(self, file, txt):
        try:
            fso = codecs.open(file, 'w+', 'utf-8-sig')
            fso.write(txt)
            if fso:
                fso.close()
        except IOError:
            print 'Error: 没有找到文件或读取文件失败'

        if fso:
            fso.close()

    def readfile(self, file):
        try:
            file = os.path.abspath(file)
            fso = open(file, 'r')
            txt = fso.read()
            if txt[:3] == codecs.BOM_UTF8:
                txt = txt[3:]
            return txt
        except IOError:
            print 'Error: 没有找到文件或读取文件失败'
            return ''

        if fso:
            fso.close()