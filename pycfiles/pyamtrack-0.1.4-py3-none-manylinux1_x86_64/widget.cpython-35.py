# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/widget.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 24907 bytes
__doc__ = 'PyAMS_form.widget module\n\nBase widget implementation.\n'
from pyramid_chameleon.interfaces import IChameleonTranslate
from zope.interface import Invalid, alsoProvides, implementer, implementer_only
from zope.location import Location
from zope.schema import ValidationError
from zope.schema.fieldproperty import FieldProperty
from zope.schema.interfaces import IMinMaxLen, ITitledTokenizedTerm
from pyams_form.interfaces import IDataConverter, INPUT_MODE, ITerms, IValidator, IValue, IWidgetLayoutTemplate
from pyams_form.interfaces.error import IErrorViewSnippet
from pyams_form.interfaces.form import IContextAware, IFormAware
from pyams_form.interfaces.widget import IAfterWidgetUpdateEvent, IFieldWidget, IMultiWidget, ISequenceWidget, IWidget, IWidgetEvent
from pyams_form.template import get_widget_layout, get_widget_template
from pyams_form.util import sorted_none
from pyams_form.value import ComputedValueCreator, StaticValueCreator
from pyams_utils.interfaces.form import IDataManager, NO_VALUE
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'
PLACEHOLDER = object()
StaticWidgetAttribute = StaticValueCreator(discriminators=(
 'context', 'request', 'view', 'field', 'widget'))
ComputedWidgetAttribute = ComputedValueCreator(discriminators=(
 'context', 'request', 'view', 'field', 'widget'))

def apply_value_to_widget(parent, widget, value):
    """Apply given value to widget"""
    if value is not NO_VALUE:
        request = parent.request
        registry = request.registry
        try:
            converter = IDataConverter(widget)
            fvalue = converter.to_field_value(value)
            registry.getMultiAdapter((parent.context, request, parent.form,
             getattr(widget, 'field', None), widget), IValidator).validate(fvalue)
            widget.value = converter.to_widget_value(fvalue)
        except (ValidationError, ValueError) as error:
            view = registry.getMultiAdapter((error, request, widget,
             widget.field, parent.form, parent.context), IErrorViewSnippet)
            view.update()
            widget.error = view
            widget.value = value


@implementer(IWidget)
class Widget(Location):
    """Widget"""
    name = FieldProperty(IWidget['name'])
    label = FieldProperty(IWidget['label'])
    mode = FieldProperty(IWidget['mode'])
    required = FieldProperty(IWidget['required'])
    error = FieldProperty(IWidget['error'])
    value = FieldProperty(IWidget['value'])
    ignore_request = FieldProperty(IWidget['ignore_request'])
    ignore_required_on_validation = FieldProperty(IWidget['ignore_required_on_validation'])
    set_errors = FieldProperty(IWidget['set_errors'])
    show_default = FieldProperty(IWidget['show_default'])
    layout = get_widget_layout()
    template = get_widget_template()
    context = None
    ignore_context = False
    form = None
    field = None
    _adapter_value_attributes = ('label', 'name', 'required', 'title')

    def __init__(self, request):
        self.request = request

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        value = NO_VALUE
        look_for_default = False
        registry = self.request.registry
        if not self.ignore_request:
            self.set_errors = False
            widget_value = self.extract()
            if widget_value is not NO_VALUE:
                self.value = widget_value
                value = PLACEHOLDER
        if IFieldWidget.providedBy(self) and value is NO_VALUE and value is not PLACEHOLDER:
            if IContextAware.providedBy(self) and not self.ignore_context:
                value = registry.getMultiAdapter((self.context, self.field), IDataManager).query()
            field = self.field.bind(self.context)
            if value is field.missing_value or value is NO_VALUE:
                default_value = field.default
                if default_value is not None and self.show_default:
                    value = field.default
                    look_for_default = True
        if (value is NO_VALUE or look_for_default) and self.show_default:
            adapter = registry.queryMultiAdapter((self.context, self.request, self.form,
             self.field, self), IValue, name='default')
            if adapter:
                value = adapter.get()
        if value not in (NO_VALUE, PLACEHOLDER):
            converter = IDataConverter(self)
            self.value = converter.to_widget_value(value)
        for attr_name in self._adapter_value_attributes:
            if hasattr(self, attr_name):
                value = registry.queryMultiAdapter((self.context, self.request, self.form,
                 self.field, self), IValue, name=attr_name)
                if value is not None:
                    setattr(self, attr_name, value.get())

    def extract(self, default=NO_VALUE):
        """See z3c.form.interfaces.IWidget."""
        return self.request.params.get(self.name, default)

    render = get_widget_template()

    def json_data(self):
        """Get widget data in JSON format"""
        return {'mode': self.mode, 
         'error': self.error.message if self.error else '', 
         'value': self.value, 
         'required': self.required, 
         'name': self.name, 
         'id': getattr(self, 'id', ''), 
         'type': 'text', 
         'label': self.label or ''}

    def __call__(self, **kwargs):
        """Get and return layout template which is calling widget/render"""
        layout = self.layout
        if layout is None:
            registry = self.request.registry
            layout = registry.getMultiAdapter((self.context, self.request, self.form,
             self.field, self), IWidgetLayoutTemplate, name=self.mode)
        cdict = {'context': self.context, 
         'request': self.request, 
         'view': self, 
         'translate': query_utility(IChameleonTranslate)}
        cdict.update(kwargs)
        return layout(**cdict)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)


@implementer(ISequenceWidget)
class SequenceWidget(Widget):
    """SequenceWidget"""
    value = ()
    terms = None
    no_value_token = '--NOVALUE--'

    @property
    def display_value(self):
        """Widget display value"""
        value = []
        for token in self.value:
            if token == self.no_value_token:
                pass
            else:
                try:
                    term = self.terms.getTermByToken(token)
                except LookupError:
                    continue

                if ITitledTokenizedTerm.providedBy(term):
                    translate = self.request.localizer.translate
                    value.append(translate(term.title))
                else:
                    value.append(term.value)

        return value

    def update_terms(self):
        """Get terms from widget context"""
        if self.terms is None:
            registry = self.request.registry
            self.terms = registry.getMultiAdapter((self.context, self.request, self.form,
             self.field, self), ITerms)
        return self.terms

    def update(self):
        """See pyams_form.interfaces.widget.IWidget."""
        self.update_terms()
        super(SequenceWidget, self).update()

    def extract(self, default=NO_VALUE):
        """See pyams_form.interfaces.widget.IWidget."""
        params = self.request.params
        if self.name not in params and self.name + '-empty-marker' in params:
            return ()
        value = params.get(self.name, default)
        if value != default:
            if not isinstance(value, (tuple, list)):
                value = (value,)
            if not isinstance(value, tuple):
                value = tuple(value)
            for token in value:
                if token == self.no_value_token:
                    pass
                else:
                    try:
                        self.terms.getTermByToken(token)
                    except LookupError:
                        return default

        return value

    def json_data(self):
        data = super(SequenceWidget, self).json_data()
        data['type'] = 'sequence'
        return data


@implementer(IMultiWidget)
class MultiWidget(Widget):
    """MultiWidget"""
    allow_adding = True
    allow_removing = True
    widgets = None
    key_widgets = None
    _value = None
    _widgets_updated = False
    _mode = FieldProperty(IWidget['mode'])

    def __init__(self, request):
        super(MultiWidget, self).__init__(request)
        self.widgets = []
        self.key_widgets = []
        self._value = []

    @property
    def is_dict(self):
        """Check field key type"""
        return getattr(self.field, 'key_type', None) is not None

    @property
    def counter_name(self):
        """Counter name getter"""
        return '%s.count' % self.name

    @property
    def counter_marker(self):
        """Counter HTML marker getter"""
        return '<input type="hidden" name="%s" value="%d" />' % (
         self.counter_name, len(self.widgets))

    @property
    def mode(self):
        """This gets the subwidgets mode."""
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Subwidgets mode setter"""
        self._mode = mode
        for w in self.widgets:
            w.mode = mode

        for w in self.key_widgets:
            if w is not None:
                w.mode = mode

    def get_widget(self, idx, prefix=None, type_field='value_type'):
        """Setup widget based on index id with or without value."""
        value_type = getattr(self.field, type_field)
        registry = self.request.registry
        widget = registry.getMultiAdapter((value_type, self.request), IFieldWidget)
        self.set_name(widget, idx, prefix)
        widget.mode = self.mode
        if IFormAware.providedBy(self):
            widget.form = self.form
            alsoProvides(widget, IFormAware)
        widget.update()
        return widget

    def set_name(self, widget, idx, prefix=None):
        """Set widget name based on index position"""
        names = lambda id: [str(n) for n in [id] + [prefix, idx] if n is not None]
        widget.name = '.'.join([str(self.name)] + names(None))
        widget.id = '-'.join([str(self.id)] + names(None))

    def append_adding_widget(self):
        """Simply append a new empty widget with correct (counter) name."""
        idx = len(self.widgets)
        widget = self.get_widget(idx)
        self.widgets.append(widget)
        if self.is_dict:
            widget = self.get_widget(idx, 'key', 'key_type')
            self.key_widgets.append(widget)
        else:
            self.key_widgets.append(None)

    def remove_widgets(self, names):
        """
        :param names: list of widget.name to remove from the value
        :return: None
        """
        zipped = list(zip(self.key_widgets, self.widgets))
        self.key_widgets = [k for k, v in zipped if v.name not in names]
        self.widgets = [v for k, v in zipped if v.name not in names]
        if self.is_dict:
            self.value = [(k.value, v.value) for k, v in zip(self.key_widgets, self.widgets)]
        else:
            self.value = [widget.value for widget in self.widgets]

    def apply_value(self, widget, value=NO_VALUE):
        """Validate and apply value to given widget.

        This method gets called on any multi widget value change and is
        responsible for validating the given value and setup an error message.

        This is internal apply value and validation process is needed because
        nothing outside this multi widget does know something about our
        internal sub widgets.
        """
        apply_value_to_widget(self, widget, value)

    def update_widgets(self):
        """Setup internal widgets based on the value_type for each value item.
        """
        old_len = len(self.widgets)
        if IMinMaxLen.providedBy(self.field) and self.mode == INPUT_MODE and self.allow_adding and old_len < self.field.min_length:
            old_len = self.field.min_length
        self.widgets = []
        self.key_widgets = []
        keys = set()
        idx = 0
        if self.value:
            if self.is_dict:
                try:
                    items = sorted_none(self.value)
                except:
                    items = self.value

            else:
                items = zip([None] * len(self.value), self.value)
            for key, v in items:
                widget = self.get_widget(idx)
                self.apply_value(widget, v)
                self.widgets.append(widget)
                if self.is_dict:
                    hash_key = key if not isinstance(key, list) else tuple(key)
                    widget = self.get_widget(idx, 'key', 'key_type')
                    self.apply_value(widget, key)
                    if hash_key in keys and widget.error is None:
                        error = Invalid('Duplicate key')
                        registry = self.request.registry
                        view = registry.getMultiAdapter((error, self.request, widget,
                         widget.field, self.form, self.context), IErrorViewSnippet)
                        view.update()
                        widget.error = view
                    self.key_widgets.append(widget)
                    keys.add(hash_key)
                else:
                    self.key_widgets.append(None)
                idx += 1

        missing = old_len - len(self.widgets)
        if missing > 0:
            for _i in range(missing):
                widget = self.get_widget(idx)
                self.widgets.append(widget)
                if self.is_dict:
                    widget = self.get_widget(idx, 'key', 'key_type')
                    self.key_widgets.append(widget)
                else:
                    self.key_widgets.append(None)
                idx += 1

        self._widgets_updated = True

    def update_allow_add_remove(self):
        """Update the allow_adding/allow_removing attributes
        basing on field constraints and current number of widgets
        """
        if not IMinMaxLen.providedBy(self.field):
            return
        max_length = self.field.max_length
        min_length = self.field.min_length
        num_items = len(self.widgets)
        self.allow_adding = bool(not max_length or num_items < max_length)
        self.allow_removing = bool(num_items and num_items > min_length)

    @property
    def value(self):
        """This invokes updateWidgets on any value change e.g. update/extract."""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.update_widgets()

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(MultiWidget, self).update()
        if not self._widgets_updated:
            self.update_widgets()

    def extract(self, default=NO_VALUE):
        params = self.request.params
        if params.get(self.counter_name) is None:
            return NO_VALUE
        counter = int(params.get(self.counter_name, 0))
        values = []
        append = values.append
        for idx in range(counter):
            widget = self.get_widget(idx)
            if self.is_dict:
                key_widget = self.get_widget(idx, 'key', 'key_type')
                append((key_widget.value, widget.value))
            else:
                append(widget.value)

        return values

    def json_data(self):
        data = super(MultiWidget, self).json_data()
        data['widgets'] = [widget.json_data() for widget in self.widgets]
        data['type'] = 'multi'
        return data


def FieldWidget(field, widget):
    """Set the field for the widget."""
    widget.field = field
    if not IFieldWidget.providedBy(widget):
        alsoProvides(widget, IFieldWidget)
    widget.name = field.__name__
    widget.id = field.__name__.replace('.', '-')
    widget.label = field.title
    widget.required = field.required
    return widget


@implementer(IWidgetEvent)
class WidgetEvent:
    """WidgetEvent"""

    def __init__(self, widget):
        self.widget = widget

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.widget)


@implementer_only(IAfterWidgetUpdateEvent)
class AfterWidgetUpdateEvent(WidgetEvent):
    """AfterWidgetUpdateEvent"""
    pass


class WidgetSelector:
    """WidgetSelector"""

    def __init__(self, ifaces, config):
        if not isinstance(ifaces, (list, tuple)):
            ifaces = (
             ifaces,)
        self.interfaces = ifaces

    def text(self):
        """Widget's selector text"""
        return 'widget_selector = %s' % str(self.interfaces)

    phash = text

    def __call__(self, event):
        for intf in self.interfaces:
            try:
                if intf.providedBy(event.widget):
                    return True
            except (AttributeError, TypeError):
                if isinstance(event.widget, intf):
                    return True

        return False