# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/hplskin/html.py
# Compiled at: 2012-06-26 16:42:30
__docformat__ = 'restructuredtext'
from zope.schema.interfaces import IText
from layer import IHPLLayer
from ztfy.file.browser.widget.interfaces import IHTMLWidgetSettings
from ztfy.skin.interfaces import IBaseForm
from zope.component import adapts
from zope.interface import implements
from ztfy.blog.browser.skin import HTMLWidgetAdapter as BaseHTMLWidgetAdapter

class HTMLWidgetAdapter(BaseHTMLWidgetAdapter):
    """Custom HTML widget settings adapter"""
    adapts(IText, IBaseForm, IHPLLayer)
    implements(IHTMLWidgetSettings)

    @property
    def mce_content_css(self):
        return '/--static--/ztfy.hplskin/css/hpl.css'