# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\js\dijit\model.py
# Compiled at: 2013-06-05 12:09:39
from .. import Object, Dojo

class ObjectStoreModel(Object, Dojo):
    require = [
     'dijit/tree/ObjectStoreModel']

    def X_new(self):
        if self.name is None:
            name = ''
        else:
            name = 'var %s = ' % self.name
        self.loc = name + 'new %s(%s)' % (self.__class__.__name__,
         self.js_options())
        return

    def X__init__(self, name=None, **options):
        self.name = name
        self.options = options
        self.new()