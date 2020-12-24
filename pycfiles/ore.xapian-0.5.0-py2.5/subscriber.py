# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/xapian/subscriber.py
# Compiled at: 2008-09-22 12:26:21
import interfaces
from zope.security.proxy import removeSecurityProxy

def objectAdded(object, event):
    if removeSecurityProxy:
        object = removeSecurityProxy(object)
    interfaces.IOperationFactory(object).add()


def objectModified(object, event):
    if removeSecurityProxy:
        object = removeSecurityProxy(object)
    interfaces.IOperationFactory(object).modify()


def objectDeleted(object, event):
    if removeSecurityProxy:
        object = removeSecurityProxy(object)
    interfaces.IOperationFactory(object).remove()