# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/error.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 4433 bytes
__doc__ = 'PyAMS_form.error module\n\nThis module provides snippets to display error messages.\n'
from zope.component import adapter
from zope.interface import Invalid, implementer
from zope.schema import ValidationError
from pyams_form.interfaces import IValue
from pyams_form.interfaces.error import IErrorViewSnippet, IMultipleErrors
from pyams_form.util import get_specification
from pyams_form.value import ComputedValueCreator, StaticValueCreator
from pyams_template.template import get_view_template
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'
from pyams_form import _
ErrorViewMessage = StaticValueCreator(discriminators=('error', 'request', 'widget',
                                                      'field', 'form', 'content'))
ComputedErrorViewMessage = ComputedValueCreator(discriminators=('error', 'request',
                                                                'widget', 'field',
                                                                'form', 'content'))

def ErrorViewDiscriminators(error_view, error=None, request=None, widget=None, field=None, form=None, content=None):
    """Error view discriminators"""
    adapter(get_specification(error), get_specification(request), get_specification(widget), get_specification(field), get_specification(form), get_specification(content))(error_view)


@adapter_config(required=(ValidationError, None, None, None, None, None), provides=IErrorViewSnippet)
@implementer(IErrorViewSnippet)
class ErrorViewSnippet:
    """ErrorViewSnippet"""
    message = None

    def __init__(self, error, request, widget, field, form, content):
        self.error = self.context = error
        self.request = request
        self.widget = widget
        self.field = field
        self.form = form
        self.content = content

    def create_message(self):
        """Get error message"""
        return self.error.doc()

    def update(self):
        """Update snippet content"""
        registry = self.request.registry
        value = registry.queryMultiAdapter((self.context, self.request, self.widget,
         self.field, self.form, self.content), IValue, name='message')
        if value is not None:
            self.message = value.get()
        else:
            self.message = self.create_message()

    render = get_view_template()

    def __repr__(self):
        return '<%s for %s>' % (self.__class__.__name__, self.error.__class__.__name__)


@adapter_config(required=(ValueError, None, None, None, None, None), provides=IErrorViewSnippet)
class ValueErrorViewSnippet(ErrorViewSnippet):
    """ValueErrorViewSnippet"""
    default_message = _('The system could not process the given value.')

    def create_message(self):
        return self.default_message


@adapter_config(required=(Invalid, None, None, None, None, None), provides=IErrorViewSnippet)
class InvalidErrorViewSnippet(ErrorViewSnippet):
    """InvalidErrorViewSnippet"""

    def create_message(self):
        return self.error.args[0]


@implementer(IMultipleErrors)
class MultipleErrors(Exception):
    """MultipleErrors"""

    def __init__(self, errors):
        self.errors = errors


@adapter_config(required=(IMultipleErrors, None, None, None, None, None), provides=IErrorViewSnippet)
class MultipleErrorViewSnippet(ErrorViewSnippet):
    """MultipleErrorViewSnippet"""

    def update(self):
        """Snippet update"""
        pass

    def render(self):
        """Render multiple errors"""
        return ''.join([view.render() for view in self.error.errors])