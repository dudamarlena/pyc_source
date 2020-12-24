# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/__init__.py
# Compiled at: 2011-03-23 00:31:36
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'

class Config:
    """ The singleton of configuration """

    class __impl:

        def __init__(self):
            self.template_dir = ''
            self.session_store = 'memcache'
            self.version = '0.3'
            self.app_name = ''

    __instance = None

    def __init__(self):
        if Config.__instance is None:
            Config.__instance = Config.__impl()
        self.__dict__['_Config__instance'] = Config.__instance
        return

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)