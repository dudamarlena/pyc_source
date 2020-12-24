# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/utils.py
# Compiled at: 2013-04-11 17:47:52
"""Helper functions for the view subpackage"""
from HTMLParser import HTMLParser
from PyQt4 import QtCore, QtGui
from datetime import datetime, time, date
import re, logging, operator
from camelot.core.sql import like_op
from sqlalchemy.sql.operators import between_op
from camelot.core.utils import ugettext
from camelot.core.utils import ugettext_lazy as _
logger = logging.getLogger('camelot.view.utils')
_local_date_format = None
_local_datetime_format = None
_local_time_format = None

def local_date_format():
    """Get the local data format and cache it for reuse"""
    global _local_date_format
    if not _local_date_format:
        locale = QtCore.QLocale()
        format_sequence = re.split('y*', unicode(locale.dateFormat(locale.ShortFormat)))
        format_sequence.insert(-1, 'yyyy')
        _local_date_format = unicode(('').join(format_sequence))
    return _local_date_format


def local_datetime_format():
    """Get the local datatime format and cache it for reuse"""
    global _local_datetime_format
    if not _local_datetime_format:
        locale = QtCore.QLocale()
        format_sequence = re.split('y*', unicode(locale.dateTimeFormat(locale.ShortFormat)))
        format_sequence.insert(-1, 'yyyy')
        _local_datetime_format = unicode(('').join(format_sequence))
    return _local_datetime_format


def local_time_format():
    """Get the local time format and cache it for reuse"""
    global _local_time_format
    if not _local_time_format:
        locale = QtCore.QLocale()
        _local_time_format = unicode(locale.timeFormat(locale.ShortFormat))
    return _local_time_format


def default_language(*args):
    """takes arguments, to be able to use this function as a
    default field attribute"""
    locale = QtCore.QLocale()
    return unicode(locale.name())


class ParsingError(Exception):
    pass


def string_from_string(s):
    if not s:
        return None
    else:
        return unicode(s)


def bool_from_string(s):
    if s is None:
        raise ParsingError()
    if s.lower() not in ('false', 'true'):
        raise ParsingError()
    return eval(s.lower().capitalize())


def _insert_string(original, new, pos):
    """Inserts new inside original at pos."""
    return original[:pos] + new + original[pos:]


def date_from_string(s):
    s = s.strip()
    if not s:
        return
    else:
        from PyQt4.QtCore import QDate
        import string
        f = local_date_format()
        dt = QDate.fromString(s, f)
        if not dt.isValid():
            if len(f) == len(s) + 1:
                s = '0' + s
                dt = QDate.fromString(s, f)
        if not dt.isValid():
            separators = ('').join([ c for c in f if c not in string.ascii_letters ])
            if separators:
                alternative_string = ('').join([ c if c in string.digits else separators[0] for c in s ])
                dt = QDate.fromString(alternative_string, f)
        if not dt.isValid():
            only_letters_format = ('').join([ c for c in f if c in string.ascii_letters ])
            only_letters_string = ('').join([ c for c in s if c in string.ascii_letters + string.digits ])
            dt = QDate.fromString(only_letters_string, only_letters_format)
            if not dt.isValid():
                only_letters_format = ('').join([ c for c in only_letters_format if c not in ('y', ) ])
                dt = QDate.fromString(only_letters_string, only_letters_format)
                if not dt.isValid():
                    raise ParsingError()
                else:
                    return date(date.today().year, dt.month(), dt.day())
        return date(dt.year(), dt.month(), dt.day())


def time_from_string(s):
    s = s.strip()
    if not s:
        return None
    else:
        from PyQt4.QtCore import QTime
        f = local_time_format()
        tm = QTime.fromString(s, f)
        if not tm.isValid():
            raise ParsingError()
        return time(tm.hour(), tm.minute(), tm.second())


def datetime_from_string(s):
    s = s.strip()
    if not s:
        return None
    else:
        from PyQt4.QtCore import QDateTime
        f = local_datetime_format()
        dt = QDateTime.fromString(s, f)
        if not dt.isValid():
            raise ParsingError()
        return datetime(dt.date().year(), dt.date().month(), dt.date().day(), dt.time().hour(), dt.time().minute(), dt.time().second())


def code_from_string(s, separator):
    return s.split(separator)


def int_from_string(s):
    value = float_from_string(s)
    if value != None:
        value = int(value)
    return value


def float_from_string(s):
    if s == None:
        return
    else:
        s = s.strip()
        if len(s) == 0:
            return
        locale = QtCore.QLocale()
        f, ok = locale.toDouble(s)
        if not ok:
            raise ParsingError()
        return f


def pyvalue_from_string(pytype, s):
    if pytype is str:
        return str(s)
    if pytype is unicode:
        return unicode(s)
    if pytype is bool:
        return bool_from_string(s)
    if pytype is date:
        return date_from_string(s)
    if pytype is time:
        return date_from_string(s)
    if pytype is datetime:
        return datetime_from_string(s)
    if pytype is float:
        return float_from_string(s)
    if pytype is int:
        return int_from_string(s)


def to_string(value):
    if value == None:
        return ''
    else:
        return unicode(value)


def enumeration_to_string(value):
    return ugettext(unicode(value or '').replace('_', ' ').capitalize())


operator_names = {operator.eq: _('='), 
   operator.ne: _('!='), 
   operator.lt: _('<'), 
   operator.le: _('<='), 
   operator.gt: _('>'), 
   operator.ge: _('>='), 
   like_op: _('like'), 
   between_op: _('between')}

def text_from_richtext(unstripped_text):
    """function that returns a list of lines with escaped data, to be used in 
    templates for example
    :arg unstripped_text: string
    :return: list of strings
    """
    strings = [
     '']
    if not unstripped_text:
        return strings

    class HtmlToTextParser(HTMLParser):

        def handle_endtag(self, tag):
            if tag == 'br':
                strings.append('')

        def handle_data(self, data):
            from xml.sax.saxutils import escape
            data = data.strip()
            if data:
                strings.append(escape(data))

    parser = HtmlToTextParser()
    parser.feed(unstripped_text.strip())
    return strings


def resize_widget_to_screen(widget, fraction=0.75):
    """Resize a widget to fill a certain fraction of the screen
    
    :param widget: the widget to resize
    :param fraction: the fraction of the screen to fill after the resize
    """
    desktop = QtGui.QApplication.desktop()
    available_geometry = desktop.availableGeometry(widget)
    widget.resize(available_geometry.width() * 0.75, available_geometry.height() * 0.75)