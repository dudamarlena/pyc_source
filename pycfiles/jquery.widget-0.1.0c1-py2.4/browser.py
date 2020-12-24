# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jquery/widget/resteditor/browser.py
# Compiled at: 2007-05-24 08:27:53
"""
$Id: layer.py 197 2007-04-13 05:03:32Z rineichen $
"""
__docformat__ = 'reStructuredText'
import zope.interface, zope.component
from zope.app.form.browser.widget import renderElement
from zope.app.form.browser import TextAreaWidget
from zope.viewlet.viewlet import CSSViewlet
from zope.viewlet.viewlet import JavaScriptViewlet
from z3c.form import widget
from z3c.form.browser import textarea
from jquery.widget.resteditor import interfaces
JQueryRestEditorCSS = CSSViewlet('jquery.resteditor.css')
JQueryRestEditorJavaScript = JavaScriptViewlet('jquery.resteditor.js')

class RESTEditorWidget(textarea.TextAreaWidget):
    """Textarea widget implementation."""
    __module__ = __name__
    zope.interface.implementsOnly(interfaces.IRESTEditorWidget)
    css = 'restEditorWidget'
    value = ''
    readonly = None
    accesskey = None


def RESTEditorFieldWidget(field, request):
    """IFieldWidget factory for RESTEditorWidget."""
    return widget.FieldWidget(field, RESTEditorWidget(request))