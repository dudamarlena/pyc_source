# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jquery/jsonform/browser.py
# Compiled at: 2007-05-24 08:27:17
"""
$Id: layer.py 197 2007-04-13 05:03:32Z rineichen $
"""
import zope.interface, zope.component
from zope.viewlet import viewlet
from z3c.form.interfaces import IValue
from z3c.form.interfaces import IErrorViewSnippet
from z3c.form.error import ErrorViewSnippet
from z3c.form.i18n import MessageFactory as _
from zif.jsonserver.interfaces import IJSONRPCRequest
JSONFormValidateJavaScriptViewlet = viewlet.JavaScriptViewlet('jsonform.validate.js')
JSONFormValidateCSSViewlet = viewlet.CSSViewlet('jsonform.validate.css')

class JSONErrorViewSnippet(object):
    """Error view snippet."""
    __module__ = __name__
    zope.component.adapts(zope.schema.ValidationError, None, IJSONRPCRequest, None, None, None)
    zope.interface.implements(IErrorViewSnippet)

    def __init__(self, error, request, widget, field, form, content):
        self.error = self.context = error
        self.request = request
        self.widget = widget
        self.field = field
        self.form = form
        self.content = content

    def update(self):
        value = zope.component.queryMultiAdapter((self.context, self.request, self.widget, self.field, self.form, self), IValue, name='message')
        if value is not None:
            self.message = value.get()
        else:
            self.message = self.error.doc()
        return

    def render(self):
        return self.message

    def __repr__(self):
        return '<%s for %s>' % (self.__class__.__name__, self.error.__class__.__name__)


class JSONValueErrorViewSnippet(JSONErrorViewSnippet):
    """An error view for ValueError."""
    __module__ = __name__
    zope.component.adapts(ValueError, None, IJSONRPCRequest, None, None, None)
    message = _('The system could not process the given value.')

    def update(self):
        value = zope.component.queryMultiAdapter((self.context, self.request, self.widget, self.field, self.form, self), IValue, name='message')
        if value is not None:
            self.message = value.get()
        return

    def render(self):
        return self.message