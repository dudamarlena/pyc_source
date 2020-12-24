# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/btypes.py
# Compiled at: 2016-10-03 09:39:22
import dateutil.parser as date_parser, sqlalchemy.types as types
from bauble.i18n import _
import bauble.error as error

class EnumError(error.BaubleError):
    """Raised when a bad value is inserted or returned from the Enum type"""
    pass


class Enum(types.TypeDecorator):
    """A database independent Enum type. The value is stored in the
    database as a Unicode string.
    """
    impl = types.Unicode

    def __init__(self, values, empty_to_none=False, strict=True, translations={}, **kwargs):
        """
        : param values: A list of valid values for column.
        :param empty_to_none: Treat the empty string '' as None.  None
        must be in the values list in order to set empty_to_none=True.
        :param strict:
        :param translations: A dictionary of values->translation
        """
        if values is None or len(values) is 0:
            raise EnumError(_('Enum requires a list of values'))
        try:
            [ len(x) for x in values if x is not None ]
        except TypeError:
            raise EnumError(_('Enum requires string values (or None)'))

        if set(type(x) for x in values if x is not None) - set([type(''), type('')]) != set():
            raise EnumError(_('Enum requires string values (or None)'))
        if len(values) != len(set(values)):
            raise EnumError(_('Enum requires the values to be different'))
        self.translations = dict((v, v) for v in values)
        for key, value in translations.iteritems():
            self.translations[key] = value

        if empty_to_none and None not in values:
            raise EnumError(_('You have configured empty_to_none=True but None is not in the values lists'))
        self.values = values[:]
        self.strict = strict
        self.empty_to_none = empty_to_none
        size = max([ len(v) for v in values if v is not None ])
        super(Enum, self).__init__(size, **kwargs)
        return

    def process_bind_param(self, value, dialect):
        """
        Process the value going into the database.
        """
        if self.empty_to_none and value is '':
            value = None
        if value not in self.values:
            raise EnumError(_('"%(value)s" not in Enum.values: %(all_values)s') % dict(value=value, all_values=self.values))
        return value

    def process_result_value(self, value, dialect):
        """
        Process the value returned from the database.
        """
        return value

    def copy(self):
        return Enum(self.values, self.empty_to_none, self.strict)


class DateTime(types.TypeDecorator):
    """
    A DateTime type that allows strings
    """
    impl = types.DateTime
    import re
    _rx_tz = re.compile('[+-]')

    def process_bind_param(self, value, dialect):
        if not isinstance(value, basestring):
            return value
        try:
            DateTime._dayfirst
            DateTime._yearfirst
        except AttributeError:
            import bauble.prefs as prefs
            DateTime._dayfirst = prefs.prefs[prefs.parse_dayfirst_pref]
            DateTime._yearfirst = prefs.prefs[prefs.parse_yearfirst_pref]

        result = date_parser.parse(value, dayfirst=DateTime._dayfirst, yearfirst=DateTime._yearfirst)
        return result

    def process_result_value(self, value, dialect):
        return value

    def copy(self):
        return DateTime()


class Date(types.TypeDecorator):
    """
    A Date type that allows Date strings
    """
    impl = types.Date

    def process_bind_param(self, value, dialect):
        if not isinstance(value, basestring):
            return value
        try:
            Date._dayfirst
            Date._yearfirst
        except AttributeError:
            import bauble.prefs as prefs
            Date._dayfirst = prefs.prefs[prefs.parse_dayfirst_pref]
            Date._yearfirst = prefs.prefs[prefs.parse_yearfirst_pref]

        return date_parser.parse(value, dayfirst=Date._dayfirst, yearfirst=Date._yearfirst).date()

    def process_result_value(self, value, dialect):
        return value

    def copy(self):
        return Date()