# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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