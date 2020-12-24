# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/property.py
# Compiled at: 2009-05-04 14:30:04
from zope.component import getUtility
from interfaces import ITemplates

class PersistentTemplate(object):
    __module__ = __name__

    def __init__(self, storage_name, template_name):
        self.__storage_name = storage_name
        self.__template_name = template_name

    def __get__(self, inst, klass):
        templates = getUtility(ITemplates, self.__storage_name)

        def compileTemplate(data={}):
            return templates.compileTemplate(self.__template_name, data)

        return compileTemplate