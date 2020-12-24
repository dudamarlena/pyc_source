# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/aliaspickler.py
# Compiled at: 2018-04-20 03:19:42
import pickle
from six.moves import cStringIO as StringIO

class AliasUnpickler(pickle.Unpickler):

    def __init__(self, aliases, *args, **kw):
        pickle.Unpickler.__init__(self, *args, **kw)
        self.aliases = aliases

    def find_class(self, module, name):
        module, name = self.aliases.get((module, name), (module, name))
        return pickle.Unpickler.find_class(self, module, name)


class AliasPickleModule(object):

    def __init__(self, aliases):
        self.aliases = aliases

    def dump(self, obj, fileobj, protocol=0):
        return pickle.dump(obj, fileobj, protocol)

    def dumps(self, obj, protocol=0):
        return pickle.dumps(obj, protocol)

    def load(self, fileobj):
        return AliasUnpickler(self.aliases, fileobj).load()

    def loads(self, string):
        fileobj = StringIO(string)
        return AliasUnpickler(self.aliases, fileobj).load()