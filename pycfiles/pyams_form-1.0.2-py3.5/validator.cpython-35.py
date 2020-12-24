# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/validator.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 8097 bytes
"""PyAMS_form.validator module

Default validation adapters.
"""
import copy
from zope.component import adapter
from zope.interface import Interface, Invalid, alsoProvides, implementer
from zope.interface.interfaces import IInterface, IMethod
from zope.schema.interfaces import IBytes, IField
from pyams_form.interfaces import IData, IManagerValidator, IValidator, IValue
from pyams_form.interfaces.form import IContextAware
from pyams_form.interfaces.widget import IFileWidget
from pyams_form.util import changed_widget, get_specification
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import IDataManager, NOT_CHANGED, NO_VALUE
from pyams_utils.registry import get_current_registry
__docformat__ = 'restructuredtext'

@implementer(IValidator)
class StrictSimpleFieldValidator:
    __doc__ = 'Strict simple field validator\n\n    Validates all incoming values\n    '

    def __init__(self, context, request, view, field, widget):
        self.context = context
        self.request = request
        self.view = view
        self.field = field
        self.widget = widget

    def validate(self, value, force=False):
        """See interfaces.IValidator"""
        context = self.context
        field = self.field
        widget = self.widget
        if field.required and widget and widget.ignore_required_on_validation:
            field = copy.copy(field)
            field.required = False
        if context is not None:
            field = field.bind(context)
        registry = self.request.registry
        if value is NOT_CHANGED:
            if IContextAware.providedBy(widget) and not widget.ignore_context:
                value = registry.getMultiAdapter((context, field), IDataManager).query()
            else:
                value = NO_VALUE
            if value is NO_VALUE:
                value = field.default
                adapter = registry.queryMultiAdapter((
                 context, self.request, self.view, field, widget), IValue, name='default')
                if adapter:
                    value = adapter.get()
        return field.validate(value)

    def __repr__(self):
        return "<%s for %s['%s']>" % (
         self.__class__.__name__,
         self.field.interface.getName(),
         self.field.__name__)


@adapter_config(required=(Interface, Interface, Interface, IField, Interface), provides=IValidator)
class SimpleFieldValidator(StrictSimpleFieldValidator):
    __doc__ = 'Simple Field Validator\n\n    Ignores unchanged values.\n    '

    def validate(self, value, force=False):
        """See interfaces.IValidator"""
        if value is self.field.missing_value:
            return super(SimpleFieldValidator, self).validate(value, force)
        if not force:
            if value is NOT_CHANGED:
                return
            if self.widget and not changed_widget(self.widget, value, field=self.field, context=self.context):
                pass
            return
        return super(SimpleFieldValidator, self).validate(value, force)


@adapter_config(required=(Interface, Interface, Interface, IBytes, IFileWidget), provides=IValidator)
class FileUploadValidator(StrictSimpleFieldValidator):
    __doc__ = 'File upload validator\n    '


def WidgetValidatorDiscriminators(validator, context=None, request=None, view=None, field=None, widget=None):
    """Widget validator discriminators"""
    adapter(get_specification(context), get_specification(request), get_specification(view), get_specification(field), get_specification(widget))(validator)


class NoInputData(Invalid):
    __doc__ = "There was no input data because:\n\n    - It wasn't asked for\n\n    - It wasn't entered by the user\n\n    - It was entered by the user, but the value entered was invalid\n\n    This exception is part of the internal implementation of checkInvariants.\n\n    "


@implementer(IData)
class Data:
    __doc__ = 'Form data proxy implementation'

    def __init__(self, schema, data, context):
        self._Data_data___ = data
        self._Data_schema___ = schema
        alsoProvides(self, schema)
        self.__context__ = context

    def __getattr__(self, name):
        schema = self._Data_schema___
        data = self._Data_data___
        try:
            field = schema[name]
        except KeyError:
            raise AttributeError(name)

        if IMethod.providedBy(field):
            raise RuntimeError('Data value is not a schema field', name)
        value = data.get(name, data)
        if value is data:
            if self.__context__ is None:
                raise NoInputData(name)
            registry = get_current_registry()
            dman = registry.getMultiAdapter((self.__context__, field), IDataManager)
            value = dman.get()
        setattr(self, name, value)
        return value


@adapter_config(required=(Interface, Interface, Interface, IInterface, Interface), provides=IManagerValidator)
class InvariantsValidator:
    __doc__ = 'Simple Field Validator'

    def __init__(self, context, request, view, schema, manager):
        self.context = context
        self.request = request
        self.view = view
        self.schema = schema
        self.manager = manager

    def validate(self, data):
        """See interfaces.IManagerValidator"""
        return self.validate_object(Data(self.schema, data, self.context))

    def validate_object(self, object):
        """validate given object"""
        errors = []
        try:
            self.schema.validateInvariants(object, errors)
        except Invalid:
            pass

        return tuple([error for error in errors if not isinstance(error, NoInputData)])

    def __repr__(self):
        return '<%s for %s>' % (self.__class__.__name__, self.schema.getName())


def WidgetsValidatorDiscriminators(validator, context=None, request=None, view=None, schema=None, manager=None):
    """Widgets validator discriminators"""
    adapter(get_specification(context), get_specification(request), get_specification(view), get_specification(schema), get_specification(manager))(validator)