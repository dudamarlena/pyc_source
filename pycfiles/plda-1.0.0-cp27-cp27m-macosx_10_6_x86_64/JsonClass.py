# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\lib\JsonClass.py
# Compiled at: 2019-02-24 22:43:02
import json, codecs, os

class CJSON:
    data = {}

    def __int__(self):
        self.__doc__ = 'v1.0'

    def loadstr(self, txt):
        return json.loads(txt)

    def loadstr2(self, txt):
        self.data = json.loads(txt)

    def loadfile(self, filepath):
        try:
            fso = open(filepath, 'r')
            txt = fso.read()
            if txt[:3] == codecs.BOM_UTF8:
                txt = txt[3:]
            jsonstring = txt
            data = json.loads(jsonstring)
        except UnicodeDecodeError as EOFError:
            data = json.loads(txt)
            print EOFError.message
            return {}
        except IOError:
            print 'Error: 没有找到文件或读取文件失败'
            return {}

        if fso:
            fso.close()
            return data

    def outputjson(self, data):
        t = json.dumps(data, sort_keys=False)
        return json.dumps(json.loads(t), ensure_ascii=False, indent=4)

    def outputjson_min(self, data):
        t = json.dumps(data, sort_keys=False)
        return json.dumps(json.loads(t), ensure_ascii=False)

    def outputjson_max(self, data):
        t = json.dumps(data, sort_keys=False)
        return json.dumps(json.loads(t), ensure_ascii=False, indent=4)

    def loadfile2(self, filepath):
        try:
            fso = open(filepath, 'r')
            txt = fso.read()
            if txt[:3] == codecs.BOM_UTF8:
                txt = txt[3:]
            jsonstring = txt.decode('gb2312')
            self.data = json.loads(jsonstring)
        finally:
            if fso:
                fso.close()

    def outputjson2(self):
        return json.dumps(self.data, sort_keys=False)

    def writefile(self, data, filepath):
        txt = self.outputjson(data)
        try:
            try:
                fso = codecs.open(filepath, 'w+', 'utf-8')
                fso.write(txt)
            except IOError:
                print 'Error: 没有找到文件或读取文件失败'

        finally:
            if fso:
                fso.close()

    def compress(self, s):
        pass