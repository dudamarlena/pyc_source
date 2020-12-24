# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/xapian/tests.py
# Compiled at: 2008-09-11 20:29:58
import unittest, doctest, shutil
from zope.app.testing import placelesssetup, ztapi
from zope.testing.doctestunit import DocFileSuite
from zope import interface, component
from zope.lifecycleevent import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent
import transaction, interfaces, subscriber, operation

def setUp(test):
    placelesssetup.setUp()
    ztapi.provideAdapter(interfaces.IIndexable, interfaces.IOperationFactory, operation.OperationFactory)
    ztapi.subscribe((interfaces.IIndexable, IObjectAddedEvent), None, subscriber.objectAdded)
    ztapi.subscribe((interfaces.IIndexable, IObjectModifiedEvent), None, subscriber.objectModified)
    ztapi.subscribe((interfaces.IIndexable, IObjectRemovedEvent), None, subscriber.objectDeleted)
    return


def tearDown(test):
    placelesssetup.tearDown()
    shutil.rmtree('tmp.idx')


def test_suite():
    globs = dict(implements=interface.implements, component=component, transaction=transaction, interfaces=interfaces)
    return unittest.TestSuite((
     DocFileSuite('readme.txt', setUp=setUp, tearDown=tearDown, globs=globs, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),))