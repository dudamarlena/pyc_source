# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/schema.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 6211 bytes
__doc__ = 'PyAMS_utils.schema module\n\nThis module is used to define custom schema fields\n'
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
    """IPersistentListField"""
    pass


@implementer(IPersistentListField)
class PersistentListField(List):
    """PersistentListField"""
    _type = PersistentListType


class IPersistentDictField(IDict):
    """IPersistentDictField"""
    pass


@implementer(IPersistentDictField)
class PersistentDictField(Dict):
    """PersistentDictField"""
    _type = PersistentMapping


class IEncodedPasswordField(IPassword):
    """IEncodedPasswordField"""
    pass


@implementer(IEncodedPasswordField)
class EncodedPasswordField(Password):
    """EncodedPasswordField"""
    _type = None

    def fromUnicode(self, str):
        return str

    def constraint(self, value):
        return True


class IHTMLField(IText):
    """IHTMLField"""
    pass


@implementer(IHTMLField)
class HTMLField(Text):
    """HTMLField"""
    pass


class IJSONDictField(IDict):
    """IJSONDictField"""
    pass


class IJSONDictFieldsGetter(Interface):
    """IJSONDictFieldsGetter"""

    def get_fields(self, data):
        """Returns an iterator made of tuples

        Each tuple may ocntain field name, field label and field value
        """
        pass


@implementer(IJSONDictField)
class JSONDictField(Dict):
    """JSONDictField"""

    def __init__(self, key_type=None, value_type=None, **kw):
        super(JSONDictField, self).__init__(key_type=TextLine(), value_type=TextLine(), **kw)


class IColorField(ITextLine):
    """IColorField"""
    pass


@implementer(IColorField)
class ColorField(TextLine):
    """ColorField"""

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
    """IDottedDecimalField"""
    pass


@implementer(IDottedDecimalField)
class DottedDecimalField(Decimal):
    """DottedDecimalField"""
    pass


class IDatesRangeField(ITuple):
    """IDatesRangeField"""
    pass


@implementer(IDatesRangeField)
class DatesRangeField(Tuple):
    """DatesRangeField"""

    def __init__(self, value_type=None, unique=False, **kw):
        super(DatesRangeField, self).__init__(value_type=None, unique=False, min_length=2, max_length=2, **kw)


class ITextLineListField(IList):
    """ITextLineListField"""
    pass


@implementer(ITextLineListField)
class TextLineListField(List):
    """TextLineListField"""

    def __init__(self, value_type=None, unique=False, **kw):
        super(TextLineListField, self).__init__(value_type=TextLine(), unique=True, **kw)


class IMailAddressField(ITextLine):
    """IMailAddressField"""
    pass


EMAIL_REGEX = re.compile('^[^ @]+@[^ @]+\\.[^ @]+$')

class InvalidEmail(ValidationError):
    """InvalidEmail"""
    __doc__ = _("Email address must be entered as « name@domain.name », without '<' and '>' characters")


@implementer(IMailAddressField)
class MailAddressField(TextLine):
    """MailAddressField"""

    def _validate(self, value):
        super(MailAddressField, self)._validate(value)
        if not EMAIL_REGEX.match(value):
            raise InvalidEmail(value)


class ITimezoneField(IChoice):
    """ITimezoneField"""
    pass


@implementer(ITimezoneField)
class TimezoneField(Choice):
    """TimezoneField"""

    def __init__(self, **kw):
        if 'vocabulary' in kw:
            kw.pop('vocabulary')
        if 'default' not in kw:
            kw['default'] = 'GMT'
        super(TimezoneField, self).__init__(vocabulary=TIMEZONES_VOCABULARY_NAME, **kw)


class IEncodingField(IChoice):
    """IEncodingField"""
    pass


@implementer(IEncodingField)
class EncodingField(Choice):
    """EncodingField"""

    def __init__(self, vocabulary=ENCODINGS_VOCABULARY_NAME, **kw):
        if 'values' in kw:
            del kw['values']
        if 'source' in kw:
            del kw['source']
        kw['vocabulary'] = vocabulary
        super(EncodingField, self).__init__(**kw)