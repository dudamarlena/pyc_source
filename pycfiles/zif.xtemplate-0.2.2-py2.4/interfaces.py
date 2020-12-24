# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/xtemplate/interfaces.py
# Compiled at: 2007-08-25 13:41:36
from zope.publisher.browser import IBrowserPage
from zope.interface import Attribute

class ILXMLHTMLPage(IBrowserPage):
    """a page generated with LXML eleemnts"""
    __module__ = __name__
    head = Attribute('document head element')
    body = Attribute('document body Element')
    docElement = Attribute('document root Element')