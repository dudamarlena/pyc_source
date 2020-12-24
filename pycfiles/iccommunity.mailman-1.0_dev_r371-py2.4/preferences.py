# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mailman/preferences.py
# Compiled at: 2008-10-06 10:31:17
from zope.interface import implements
from zope.component import getUtility
from OFS.SimpleItem import SimpleItem
from zope.schema.fieldproperty import FieldProperty
from zope.component import queryUtility
from iccommunity.core.fieldproperty import ToolDependentFieldProperty, AnnotatableFieldProperty, AuthenticatedMemberFieldProperty
from iccommunity.mailman import interfaces
from iccommunity.mailman.interfaces import IicCommunityMailman
from iccommunity.core.annotations import KeywordBasedAnnotations
_marker = object()

class HostFieldProperty(object):
    __module__ = __name__

    def __init__(self, field, name=None):
        if name is None:
            name = field.__name__
        self.__field = field
        self.__name = name
        return

    def __get__(self, inst, klass):
        if inst is None:
            return self
        value = inst.__dict__.get(self.__name, _marker)
        if value is _marker:
            field = self.__field.bind(inst)
            value = getattr(field, 'default', _marker)
            if value is _marker:
                raise AttributeError(self.__name)
        return value

    def __set__(self, inst, value):
        field = self.__field.bind(inst)
        field.validate(value)
        utility = queryUtility(IicCommunityMailman)
        utility.set_host(value)
        if field.readonly and inst.__dict__.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')
        inst.__dict__[self.__name] = value

    def __getattr__(self, name):
        return getattr(self.__field, name)


class icCommunityManagementMailmanPersistence(SimpleItem):
    __module__ = __name__
    implements(interfaces.IicCommunityManagementMailman)
    host = HostFieldProperty(interfaces.IicCommunityManagementMailman['host'])
    available_lists = ToolDependentFieldProperty(interfaces.IicCommunityManagementMailman['available_lists'])


def icCommunityManagementMailmanPersistenceFactory(context):
    pcm = getUtility(interfaces.IicCommunityManagementMailman, name='iccommunity.configuration', context=context)
    return pcm


class icCommunityManagementMailmanUserListsPersistenceFactory(KeywordBasedAnnotations):
    __module__ = __name__
    implements(interfaces.IicCommunityManagementMailman)
    subscribed_lists = AuthenticatedMemberFieldProperty(interfaces.IicCommunityMailmanUserLists['subscribed_lists'], 'iccommunity.mailman.subscribed_lists')