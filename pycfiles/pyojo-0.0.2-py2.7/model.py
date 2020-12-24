# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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