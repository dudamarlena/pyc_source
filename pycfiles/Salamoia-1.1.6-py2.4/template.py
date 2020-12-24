# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/template.py
# Compiled at: 2007-12-02 16:26:58
import shelve, os

class TemplateEngine(object):
    __module__ = __name__

    def __init__(self, varPath, filename='Templates.db'):
        self.myInfo = []
        self.filename = os.path.join(varPath, filename)

    def list(self):
        try:
            data = shelve.open(self.filename)
        except:
            raise 'Db not found'

        keys = data.keys()
        data.close()
        return keys

    def add(self, key, thing):
        try:
            data = shelve.open(self.filename)
        except:
            raise 'File not found'

        if data.has_key(key):
            data[key] = thing
            data.close()
        else:
            data[key] = thing
            data.close()

    def get(self, key):
        data = shelve.open(self.filename)
        if data.has_key(key):
            ret = data[key]
            data.close()
            return ret
        else:
            return
        return

    def pop(self, key):
        data = shelve.open(self.filename)
        if data.has_key(key):
            ret = data.pop(key)
            data.close()
            return ret
        else:
            return
        return

    def __repr__(self):
        return '<%s:filename=%s>' % (self.__class__.__name__, self.filename)


from salamoia.tests import *
runDocTests()