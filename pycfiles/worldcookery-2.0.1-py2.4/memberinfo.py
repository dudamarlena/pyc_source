# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/memberinfo.py
# Compiled at: 2006-09-21 05:27:39
from persistent.dict import PersistentDict
from zope.interface import implements
from zope.component import adapts
from zope.security.interfaces import IPrincipal
from zope.annotation.interfaces import IAnnotations
from worldcookery.interfaces import IMemberInfo
KEY = 'worldcookery.memberinfo'

class MappingProperty(object):
    __module__ = __name__

    def __init__(self, name):
        self.name = name

    def __get__(self, inst, class_=None):
        return inst.mapping[self.name]

    def __set__(self, inst, value):
        inst.mapping[self.name] = value


class MemberInfo(object):
    __module__ = __name__
    implements(IMemberInfo)
    adapts(IPrincipal)

    def __init__(self, context):
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            blank = {'first': '', 'last': '', 'email': ''}
            mapping = annotations[KEY] = PersistentDict(blank)
        self.mapping = mapping
        return

    first = MappingProperty('first')
    last = MappingProperty('last')
    email = MappingProperty('email')