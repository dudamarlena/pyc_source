# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/browser/simplewidgetfactory.py
# Compiled at: 2008-12-22 08:23:20
"""Simple Widget Factories module for the Zope 3 based ks.widget package

$Id: simplewidgetfactory.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
__credits__ = 'Based heavily on zope.app.form.browser.objectwidget.ObjectWidget'
import zope.component
from zope.app.form import CustomWidgetFactory
from zope.app.form.interfaces import IInputWidget, IDisplayWidget
import logging
logger = logging.getLogger('ks.widget.simplewidgetfactory')

def SchemaDisplayWidgetFactory(field, *args, **kw):
    return CustomWidgetFactory((lambda *kv, **kw: zope.component.getMultiAdapter((field, args[(-1)]), IDisplayWidget)), *args, **kw)(field, args[(-1)])


def AddFormWidgetFactory(field, *args, **kw):
    return CustomWidgetFactory((lambda *kv, **kw: zope.component.getMultiAdapter((field, args[(-1)]), IInputWidget)), *args, **kw)(field, args[(-1)])


def EditFormWidgetFactory(field, *args, **kw):
    if field.readonly:
        iface = IDisplayWidget
    else:
        iface = IInputWidget
    return CustomWidgetFactory((lambda *kv, **kw: zope.component.getMultiAdapter((field, args[(-1)]), iface)), *args, **kw)(field, args[(-1)])