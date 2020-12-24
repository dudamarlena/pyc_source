# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/adverlet.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from zope.event import notify
from zope.interface import implements
from zope.component import queryUtility
from rwproperty import setproperty, getproperty
from zope.schema.fieldproperty import FieldProperty
from interfaces import IAdverlet, ISourceStorage
from events import SourceModifiedEvent

class Adverlet(object):
    """ See ice.adverlet.interfaces.IAdverlet """
    __module__ = __name__
    implements(IAdverlet)
    __name__ = __parent__ = None
    description = FieldProperty(IAdverlet['description'])
    default = FieldProperty(IAdverlet['default'])
    wysiwyg = FieldProperty(IAdverlet['wysiwyg'])
    newlines = FieldProperty(IAdverlet['newlines'])

    @setproperty
    def source(self, html):
        storage = queryUtility(ISourceStorage)
        if storage:
            storage.sources[self.__name__] = html
            notify(SourceModifiedEvent(self.__name__))

    @getproperty
    def source(self):
        storage = queryUtility(ISourceStorage)
        if storage and self.__name__ in storage.sources:
            return storage.sources[self.__name__]
        return