# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/schema.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 6211 bytes
"""PyAMS_utils.schema module

This module is used to define custom schema fields
"""
import re, string
from persistent.list import PersistentList as PersistentListType
from persistent.mapping import PersistentMapping
from zope.interface import Interface, implementer
from zope.schema import Choice, Decimal, Dict, List, Password, Text, TextLine, Tuple, ValidationError
from zope.schema.interfaces import IChoice, IDecimal, IDict, IList, IPassword, IText, ITextLine, ITuple
from pyams_utils.interfaces import ENCODINGS_VOCABULARY_NAME, TIMEZONES_VOCABULARY_NAME
__docformat__ = 'restructuredtext'
from pyams_utils import _

class IPersistentListField(IList):
    __doc__ = 'Persistent list field marker interface'


@implementer(IPersistentListField)
class PersistentListField(List):
    __doc__ = 'Persistent list field'
    _type = PersistentListType


class IPersistentDictField(IDict):
    __doc__ = 'Persistent mapping field marker interface'


@implementer(IPersistentDictField)
class PersistentDictField(Dict):
    __doc__ = 'Persistent mapping field'
    _type = PersistentMapping


class IEncodedPasswordField(IPassword):
    __doc__ = 'Encoded password field interface'


@implementer(IEncodedPasswordField)
class EncodedPasswordField(Password):
    __doc__ = 'Encoded password field'
    _type = None

    def fromUnicode(self, str):
        return str

    def constraint(self, value):
        return True


class IHTMLField(IText):
    __doc__ = 'HTML field interface'


@implementer(IHTMLField)
class HTMLField(Text):
    __doc__ = 'HTML field'


class IJSONDictField(IDict):
    __doc__ = 'JSON dict value field interface'


class IJSONDictFieldsGetter(Interface):
    __doc__ = 'Adapter interface used to get JSON value fields list'

    def get_fields(self, data):
        """Returns an iterator made of tuples

        Each tuple may ocntain field name, field label and field value
        """
        pass


@implementer(IJSONDictField)
class JSONDictField(Dict):
    __doc__ = 'JSON dict value field'

    def __init__(self, key_type=None, value_type=None, **kw):
        super(JSONDictField, self).__init__(key_type=TextLine(), value_type=TextLine(), **kw)


class IColorField(ITextLine):
    __doc__ = 'Marker interface for color fields'


@implementer(IColorField)
class ColorField(TextLine):
    __doc__ = 'Color field'

    def __init__(self, *args, **kw):
        super(ColorField, self).__init__(*args, **kw)

    def _validate(self, value):
        if len(value) not in (3, 6):
            raise ValidationError(_('Color length must be 3 or 6 characters'))
        for val in value:
            if val not in string.hexdigits:
                raise ValidationError(_("Color value must contain only valid hexadecimal color codes (numbers or letters between 'A' end 'F')"))

        super(ColorField, self)._validate(value)


class IDottedDecimalField(IDecimal):
    __doc__ = 'Marker interface for dotted decimal fields'


@implementer(IDottedDecimalField)
class DottedDecimalField(Decimal):
    __doc__ = 'Dotted decimal field'


class IDatesRangeField(ITuple):
    __doc__ = 'Marker interface for dates range fields'


@implementer(IDatesRangeField)
class DatesRangeField(Tuple):
    __doc__ = 'Dates range field'

    def __init__(self, value_type=None, unique=False, **kw):
        super(DatesRangeField, self).__init__(value_type=None, unique=False, min_length=2, max_length=2, **kw)


class ITextLineListField(IList):
    __doc__ = 'Marker interface for textline list field'


@implementer(ITextLineListField)
class TextLineListField(List):
    __doc__ = 'TextLine list field'

    def __init__(self, value_type=None, unique=False, **kw):
        super(TextLineListField, self).__init__(value_type=TextLine(), unique=True, **kw)


class IMailAddressField(ITextLine):
    __doc__ = 'Marker interface for mail address field'


EMAIL_REGEX = re.compile('^[^ @]+@[^ @]+\\.[^ @]+$')

class InvalidEmail(ValidationError):
    __doc__ = 'Invalid email validation error'
    __doc__ = _("Email address must be entered as « name@domain.name », without '<' and '>' characters")


@implementer(IMailAddressField)
class MailAddressField(TextLine):
    __doc__ = 'Mail address field'

    def _validate(self, value):
        super(MailAddressField, self)._validate(value)
        if not EMAIL_REGEX.match(value):
            raise InvalidEmail(value)


class ITimezoneField(IChoice):
    __doc__ = 'Marker interface for timezone field'


@implementer(ITimezoneField)
class TimezoneField(Choice):
    __doc__ = 'Timezone choice field'

    def __init__(self, **kw):
        if 'vocabulary' in kw:
            kw.pop('vocabulary')
        if 'default' not in kw:
            kw['default'] = 'GMT'
        super(TimezoneField, self).__init__(vocabulary=TIMEZONES_VOCABULARY_NAME, **kw)


class IEncodingField(IChoice):
    __doc__ = 'Encoding field interface'


@implementer(IEncodingField)
class EncodingField(Choice):
    __doc__ = 'Encoding schema field'

    def __init__(self, vocabulary=ENCODINGS_VOCABULARY_NAME, **kw):
        if 'values' in kw:
            del kw['values']
        if 'source' in kw:
            del kw['source']
        kw['vocabulary'] = vocabulary
        super(EncodingField, self).__init__(**kw)