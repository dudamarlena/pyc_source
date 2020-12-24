# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/maxipago/client.py
# Compiled at: 2018-07-08 23:37:16
# Size of source mod 2**32: 777 bytes


class Maxipago(object):

    def __init__(self, maxid, api_key, api_version='3.1.1.15', sandbox=False):
        self.maxid = maxid
        self.api_key = api_key
        self.api_version = api_version
        self.sandbox = sandbox

    def __getattr__(self, name):
        try:
            class_name = ''.join([n.title() for n in name.split('_') + ['manager']])
            module = __import__(('maxipago.managers.{0}'.format(name)), fromlist=[''])
            klass = getattr(module, class_name)
            return klass(self.maxid, self.api_key, self.api_version, self.sandbox)
        except ImportError:
            if name in self.__dict__:
                return self.__dict__.get('name')
        except AttributeError:
            raise AttributeError