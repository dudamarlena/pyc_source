# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grad03/fengl/AIMES_project/aimes.bundle/src/aimes/bundle/exceptions.py
# Compiled at: 2015-08-31 13:40:26
__author__ = 'Francis Liu'
__copyright__ = 'Copyright 2013-2015, The AIMES Project'
__license__ = 'MIT'

class BundleException(Exception):

    def __init__(self, msg, obj=None):
        Exception.__init__(self, msg)
        self._obj = obj
        self.message = msg

    def get_object(self):
        return self._obj

    def get_message(self):
        return self.message

    def __str__(self):
        return self.get_message()