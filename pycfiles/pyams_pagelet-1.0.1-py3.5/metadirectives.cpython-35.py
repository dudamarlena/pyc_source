# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_pagelet/metadirectives.py
# Compiled at: 2020-02-20 08:01:50
# Size of source mod 2**32: 1747 bytes
"""PyAMS_paget.metadirectives module

This module provides interface of ZCML directives.
"""
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.schema import TextLine
__docformat__ = 'restructuredtext'

class IPageletDirective(Interface):
    __doc__ = 'Pagelet ZCML directive interface'
    name = TextLine(title='The name of the view', description='Shows up in URLs/paths. For example "foo" or "foo.html"', required=True)
    context = GlobalObject(title='The interface or class this view is for', required=False)
    layer = GlobalObject(title='The request interface or class this pagelet is for', description='Defaults to pyramid.interfaces.IRequest', required=False)
    view = GlobalObject(title='View class', description='The view function or class', required=True)
    permission = TextLine(title='Permission', description='The permission needed to use the view', required=False)


IPageletDirective.setTaggedValue('keyword_arguments', True)