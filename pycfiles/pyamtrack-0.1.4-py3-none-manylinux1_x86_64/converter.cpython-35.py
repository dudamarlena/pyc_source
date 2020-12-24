# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/converter.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 16623 bytes
__doc__ = 'PyAMS_form.converter module\n\nThis module provides all default schema fields converters.\n'
import datetime, decimal
from cgi import FieldStorage
import six
from zope.i18n.format import DateTimeParseError, NumberParseError
from zope.interface import alsoProvides, implementer
try:
    from zope.publisher.browser import FileUpload
except ImportError:
    FileUpload = None

from zope.schema import ValidationError
from zope.schema.interfaces import IBool, IBytes, ICollection, IDate, IDatetime, IDecimal, IDict, IField, IFloat, IFromUnicode, IInt, ISequence, ITime, ITimedelta
from pyams_form.interfaces import IDataConverter
from pyams_form.interfaces.form import IFormAware
from pyams_form.interfaces.widget import IFieldWidget, IMultiWidget, ISequenceWidget, ISingleCheckBoxWidget, ITextLinesWidget, IWidget, IFileWidget
from pyams_form.util import to_bytes, to_unicode
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import NOT_CHANGED
__docformat__ = 'restructuredtext'
from pyams_form import _

@implementer(IDataConverter)
class BaseDataConverter:
    """BaseDataConverter"""
    _strip_value = True

    def __init__(self, field, widget):
        self.field = field
        self.widget = widget

    def _get_converter(self, field):
        registry = self.widget.request.registry
        widget = registry.getMultiAdapter((field, self.widget.request), IFieldWidget)
        if IFormAware.providedBy(self.widget):
            widget.form = self.widget.form
            alsoProvides(widget, IFormAware)
        converter = registry.getMultiAdapter((field, widget), IDataConverter)
        return converter

    def to_widget_value(self, value):
        """See interfaces.IDataConverter"""
        if value == self.field.missing_value:
            return ''
        return to_unicode(value)

    def to_field_value(self, value):
        """See interfaces.IDataConverter"""
        if self._strip_value and isinstance(value, six.string_types):
            value = value.strip()
        if value == '':
            return self.field.missing_value
        return self.field.fromUnicode(value)

    def __repr__(self):
        return '<%s converts from %s to %s>' % (
         self.__class__.__name__,
         self.field.__class__.__name__,
         self.widget.__class__.__name__)


@adapter_config(required=(IField, IWidget), provides=IDataConverter)
class FieldDataConverter(BaseDataConverter):
    """FieldDataConverter"""

    def __init__(self, field, widget):
        super(FieldDataConverter, self).__init__(field, widget)
        if not IFromUnicode.providedBy(field):
            field_name = ''
            if field.__name__:
                field_name = '``%s`` ' % field.__name__
            raise TypeError('Field %s of type ``%s`` must provide ``IFromUnicode``.' % (
             field_name, type(field).__name__))


@adapter_config(required=IFieldWidget, provides=IDataConverter)
def FieldWidgetDataConverter(widget):
    """Provide a data converter based on a field widget."""
    return widget.request.registry.queryMultiAdapter((widget.field, widget), IDataConverter)


class FormatterValidationError(ValidationError):
    """FormatterValidationError"""
    message = None

    def __init__(self, message, value):
        ValidationError.__init__(self, message, value)
        self.message = message

    def doc(self):
        return self.message


class NumberDataConverter(BaseDataConverter):
    """NumberDataConverter"""
    type = None
    error_message = None

    def __init__(self, field, widget):
        super(NumberDataConverter, self).__init__(field, widget)
        locale = self.widget.request.locale
        self.formatter = locale.numbers.getFormatter('decimal')
        self.formatter.type = self.type

    def to_widget_value(self, value):
        """See interfaces.IDataConverter"""
        if value == self.field.missing_value:
            return ''
        return self.formatter.format(value)

    def to_field_value(self, value):
        """See interfaces.IDataConverter"""
        if value == '':
            return self.field.missing_value
            try:
                return self.formatter.parse(value)
            except NumberParseError:
                raise FormatterValidationError(self.error_message, value)


@adapter_config(required=(IInt, IWidget), provides=IDataConverter)
class IntegerDataConverter(NumberDataConverter):
    """IntegerDataConverter"""
    type = int
    error_message = _('The entered value is not a valid integer literal.')


@adapter_config(required=(IFloat, IWidget), provides=IDataConverter)
class FloatDataConverter(NumberDataConverter):
    """FloatDataConverter"""
    type = float
    error_message = _('The entered value is not a valid decimal literal.')


@adapter_config(required=(IDecimal, IWidget), provides=IDataConverter)
class DecimalDataConverter(NumberDataConverter):
    """DecimalDataConverter"""
    type = decimal.Decimal
    error_message = _('The entered value is not a valid decimal literal.')


class CalendarDataConverter(BaseDataConverter):
    """CalendarDataConverter"""
    type = None
    length = 'short'

    def __init__(self, field, widget):
        super(CalendarDataConverter, self).__init__(field, widget)
        locale = self.widget.request.locale
        self.formatter = locale.dates.getFormatter(self.type, self.length)

    def to_widget_value(self, value):
        """See interfaces.IDataConverter"""
        if value is self.field.missing_value:
            return ''
        return self.formatter.format(value)

    def to_field_value(self, value):
        """See interfaces.IDataConverter"""
        if value == '':
            return self.field.missing_value
            try:
                return self.formatter.parse(value)
            except DateTimeParseError as err:
                raise FormatterValidationError(err.args[0], value)


@adapter_config(required=(IDate, IWidget), provides=IDataConverter)
class DateDataConverter(CalendarDataConverter):
    """DateDataConverter"""
    type = 'date'


@adapter_config(required=(ITime, IWidget), provides=IDataConverter)
class TimeDataConverter(CalendarDataConverter):
    """TimeDataConverter"""
    type = 'time'


@adapter_config(required=(IDatetime, IWidget), provides=IDataConverter)
class DatetimeDataConverter(CalendarDataConverter):
    """DatetimeDataConverter"""
    type = 'dateTime'


@adapter_config(required=(ITimedelta, IWidget), provides=IDataConverter)
class TimedeltaDataConverter(FieldDataConverter):
    """TimedeltaDataConverter"""

    def __init__(self, field, widget):
        self.field = field
        self.widget = widget

    def to_field_value(self, value):
        """See interfaces.IDataConverter"""
        if value == '':
            return self.field.missing_value
            try:
                days_string, crap, time_string = value.split(' ')
            except ValueError:
                time_string = value
                days = 0
            else:
                days = int(days_string)
            seconds = [int(part) * 60 ** (2 - n) for n, part in enumerate(time_string.split(':'))]
            return datetime.timedelta(days, sum(seconds))


@adapter_config(required=(IBytes, IFileWidget), provides=IDataConverter)
class FileUploadDataConverter(BaseDataConverter):
    """FileUploadDataConverter"""

    def to_widget_value(self, value):
        """See interfaces.IDataConverter"""
        pass

    def to_field_value(self, value):
        """See interfaces.IDataConverter"""
        if value is None or value == '':
            return NOT_CHANGED
        if isinstance(value, (FieldStorage, FileUpload)):
            self.widget.headers = value.headers
            self.widget.filename = value.filename
            try:
                if isinstance(value, FieldStorage):
                    seek = value.fp.seek
                    read = value.fp.read
                else:
                    seek = value.seek
                    read = value.read
            except AttributeError as e:
                raise ValueError(_('Bytes data are not a file object'), e)
            else:
                seek(0)
            data = read()
            if data or getattr(value, 'filename', ''):
                return data
            else:
                return self.field.missing_value
        else:
            return to_bytes(value)


@adapter_config(required=(IField, ISequenceWidget), provides=IDataConverter)
class SequenceDataConverter(BaseDataConverter):
    """SequenceDataConverter"""

    def to_widget_value(self, value):
        """Convert from Python bool to HTML representation."""
        if value is self.field.missing_value:
            return []
        terms = self.widget.update_terms()
        try:
            return [terms.getTerm(value).token]
        except LookupError:
            return []

    def to_field_value(self, value):
        """See interfaces.IDataConverter"""
        widget = self.widget
        if len(value) == 0 or value[0] == widget.no_value_token:
            return self.field.missing_value
        widget.update_terms()
        return widget.terms.getValue(value[0])


@adapter_config(required=(ICollection, ISequenceWidget), provides=IDataConverter)
class CollectionSequenceDataConverter(BaseDataConverter):
    """CollectionSequenceDataConverter"""

    def to_widget_value(self, value):
        """Convert from Python bool to HTML representation."""
        if value is self.field.missing_value:
            return []
        widget = self.widget
        if widget.terms is None:
            widget.update_terms()
        values = []
        for entry in value:
            try:
                values.append(widget.terms.getTerm(entry).token)
            except LookupError:
                pass

        return values

    def to_field_value(self, value):
        """See interfaces.IDataConverter"""
        widget = self.widget
        if widget.terms is None:
            widget.update_terms()
        collection_type = self.field._type
        if isinstance(collection_type, tuple):
            collection_type = collection_type[(-1)]
        return collection_type([widget.terms.getValue(token) for token in value])


@adapter_config(required=(ISequence, ITextLinesWidget), provides=IDataConverter)
class TextLinesConverter(BaseDataConverter):
    """TextLinesConverter"""

    def to_widget_value(self, value):
        """Convert from text lines to HTML representation."""
        if value is self.field.missing_value:
            return ''
        return '\n'.join(to_unicode(v) for v in value)

    def to_field_value(self, value):
        """See interfaces.IDataConverter"""
        collection_type = self.field._type
        if isinstance(collection_type, tuple):
            collection_type = collection_type[(-1)]
        if len(value) == 0:
            return self.field.missing_value
        value_type = self.field.value_type._type
        if isinstance(value_type, tuple):
            value_type = value_type[0]
        value = value.replace('\r\n', '\n')
        items = []
        for val in value.split('\n'):
            try:
                items.append(value_type(val))
            except ValueError as err:
                raise FormatterValidationError(str(err), val)

        return collection_type(items)


@adapter_config(required=(ISequence, IMultiWidget), provides=IDataConverter)
class MultiConverter(BaseDataConverter):
    """MultiConverter"""

    def to_widget_value(self, value):
        """Just dispatch it."""
        if value is self.field.missing_value:
            return []
        converter = self._get_converter(self.field.value_type)
        return [converter.to_widget_value(v) for v in value]

    def to_field_value(self, value):
        """Just dispatch it."""
        if len(value) == 0:
            return self.field.missing_value
        converter = self._get_converter(self.field.value_type)
        values = [converter.to_field_value(v) for v in value]
        collection_type = self.field._type
        return collection_type(values)


@adapter_config(required=(IDict, IMultiWidget), provides=IDataConverter)
class DictMultiConverter(BaseDataConverter):
    """DictMultiConverter"""

    def to_widget_value(self, value):
        """Just dispatch it."""
        if value is self.field.missing_value:
            return []
        key_converter = self._get_converter(self.field.key_type)
        converter = self._get_converter(self.field.value_type)
        return [(key_converter.to_widget_value(k), converter.to_widget_value(v)) for k, v in value.items()]

    def to_field_value(self, value):
        """Just dispatch it."""
        if len(value) == 0:
            return self.field.missing_value
        key_converter = self._get_converter(self.field.key_type)
        converter = self._get_converter(self.field.value_type)
        return {key_converter.to_field_value(k):converter.to_field_value(v) for k, v in value}


@adapter_config(required=(IBool, ISingleCheckBoxWidget), provides=IDataConverter)
class BoolSingleCheckboxDataConverter(BaseDataConverter):
    """BoolSingleCheckboxDataConverter"""

    def to_widget_value(self, value):
        """Convert from Python bool to HTML representation."""
        if value:
            return ['selected']
        return []

    def to_field_value(self, value):
        """See interfaces.IDataConverter"""
        if value and value[0] == 'selected':
            return True
        return False