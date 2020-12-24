# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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