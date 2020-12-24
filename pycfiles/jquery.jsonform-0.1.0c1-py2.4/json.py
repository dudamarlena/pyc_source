# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jquery/jsonform/json.py
# Compiled at: 2007-05-24 08:27:17
"""
$Id: views.py 93 2006-07-22 22:57:31Z roger.ineichen $
"""
__docformat__ = 'restructuredtext'
import zope.component, zope.interface
from zope.publisher.interfaces.browser import IBrowserPage
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IValidator
from z3c.form.interfaces import IErrorViewSnippet
from z3c.form import util
from zif.jsonserver.interfaces import IJSONRPCPublisher
from zif.jsonserver.interfaces import IJSONRPCRequest
from zif.jsonserver.jsonrpc import MethodPublisher

class Validator(MethodPublisher):
    __module__ = __name__
    zope.component.adapts(IBrowserPage, IJSONRPCRequest)
    zope.interface.implements(IJSONRPCPublisher)

    def jsonValidate(self, id, value):
        """Validate the value for the witdget with the given DOM field id."""
        res = 'OK'
        data = {}
        errorView = None
        self.context.updateWidgets()
        widget = util.getWidgetById(self.context, id)
        if widget is not None:
            content = self.context.widgets.content
            form = self.context.widgets.form
            try:
                value = IDataConverter(widget).toFieldValue(value)
                validator = zope.component.getMultiAdapter((content, self.request, self.context, getattr(widget, 'field', None), widget), IValidator)
                error = validator.validate(value)
            except (zope.schema.ValidationError, ValueError), error:
                errorView = zope.component.getMultiAdapter((error, self.request, widget, widget.field, form, content), IErrorViewSnippet)
                errorView.update()

        if errorView is not None:
            res = errorView.render()
        return {'id': id, 'result': res}