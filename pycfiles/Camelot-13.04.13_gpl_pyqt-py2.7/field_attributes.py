# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/field_attributes.py
# Compiled at: 2013-04-11 17:47:52
"""Default field attributes for various sqlalchemy column types"""
import sqlalchemy.types, camelot.types
from camelot.core.sql import like_op
from sqlalchemy.sql.operators import between_op
import datetime, operator
from controls import delegates
from camelot.core import constants
from camelot.view.utils import bool_from_string, date_from_string, time_from_string, datetime_from_string, int_from_string, float_from_string, string_from_string, enumeration_to_string, default_language, code_from_string
_numerical_operators = (
 operator.eq, operator.ne, operator.lt, operator.le, operator.gt, operator.ge, between_op)
_text_operators = (operator.eq, operator.ne, like_op)
order_operators = (
 operator.lt, operator.le, operator.gt, operator.ge, between_op, like_op)
_sqlalchemy_to_python_type_ = {sqlalchemy.types.Boolean: lambda f: {'python_type': bool, 
                              'editable': True, 
                              'nullable': True, 
                              'delegate': delegates.BoolDelegate, 
                              'from_string': bool_from_string, 
                              'operators': (
                                          operator.eq,)}, 
   sqlalchemy.types.Date: lambda f: {'python_type': datetime.date, 
                           'format': constants.camelot_date_format, 
                           'editable': True, 
                           'min': None, 
                           'max': None, 
                           'nullable': True, 
                           'delegate': delegates.DateDelegate, 
                           'from_string': date_from_string, 
                           'operators': _numerical_operators}, 
   sqlalchemy.types.Time: lambda f: {'python_type': datetime.time, 
                           'editable': True, 
                           'nullable': True, 
                           'widget': 'time', 
                           'delegate': delegates.TimeDelegate, 
                           'format': constants.camelot_time_format, 
                           'nullable': True, 
                           'from_string': time_from_string, 
                           'operators': _numerical_operators}, 
   sqlalchemy.types.DateTime: lambda f: {'python_type': datetime.datetime, 
                               'editable': True, 
                               'nullable': True, 
                               'widget': 'time', 
                               'format': constants.camelot_datetime_format, 
                               'nullable': True, 
                               'delegate': delegates.DateTimeDelegate, 
                               'from_string': datetime_from_string, 
                               'operators': _numerical_operators}, 
   sqlalchemy.types.Float: lambda f: {'python_type': float, 
                            'precision': ((isinstance(f.precision, tuple) or f).precision if 1 else f.precision[1]) or 2, 
                            'editable': True, 
                            'minimum': constants.camelot_minfloat, 
                            'maximum': constants.camelot_maxfloat, 
                            'nullable': True, 
                            'delegate': delegates.FloatDelegate, 
                            'from_string': float_from_string, 
                            'operators': _numerical_operators}, 
   sqlalchemy.types.Numeric: lambda f: {'python_type': float, 
                              'precision': f.scale, 
                              'editable': True, 
                              'minimum': constants.camelot_minfloat, 
                              'maximum': constants.camelot_maxfloat, 
                              'nullable': True, 
                              'delegate': delegates.FloatDelegate, 
                              'from_string': float_from_string, 
                              'operators': _numerical_operators, 
                              'decimal': True}, 
   sqlalchemy.types.Integer: lambda f: {'python_type': int, 
                              'editable': True, 
                              'minimum': constants.camelot_minint, 
                              'maximum': constants.camelot_maxint, 
                              'nullable': True, 
                              'delegate': delegates.IntegerDelegate, 
                              'from_string': int_from_string, 
                              'to_string': unicode, 
                              'widget': 'int', 
                              'operators': _numerical_operators}, 
   sqlalchemy.types.String: lambda f: {'python_type': str, 
                             'length': f.length, 
                             'delegate': delegates.PlainTextDelegate, 
                             'editable': True, 
                             'nullable': True, 
                             'widget': 'str', 
                             'from_string': string_from_string, 
                             'operators': _text_operators}, 
   camelot.types.Image: lambda f: {'python_type': str, 
                         'editable': True, 
                         'nullable': True, 
                         'delegate': delegates.ImageDelegate, 
                         'storage': f.storage, 
                         'preview_width': 100, 
                         'preview_height': 100, 
                         'operators': _text_operators}, 
   camelot.types.Code: lambda f: {'python_type': str, 
                        'editable': True, 
                        'delegate': delegates.CodeDelegate, 
                        'nullable': True, 
                        'parts': f.parts, 
                        'separator': f.separator, 
                        'operators': _text_operators, 
                        'from_string': lambda s: code_from_string(s, f.separator)}, 
   camelot.types.IPAddress: lambda f: {'python_type': str, 
                             'editable': True, 
                             'nullable': True, 
                             'parts': f.parts, 
                             'delegate': delegates.CodeDelegate, 
                             'widget': 'code', 
                             'operators': _text_operators}, 
   camelot.types.VirtualAddress: lambda f: {'python_type': str, 
                                  'editable': True, 
                                  'nullable': True, 
                                  'delegate': delegates.VirtualAddressDelegate, 
                                  'operators': _text_operators, 
                                  'from_string': lambda str: None}, 
   camelot.types.RichText: lambda f: {'python_type': str, 
                            'editable': True, 
                            'nullable': True, 
                            'delegate': delegates.RichTextDelegate, 
                            'from_string': string_from_string, 
                            'operators': []}, 
   camelot.types.Color: lambda f: {'delegate': delegates.ColorDelegate, 
                         'python_type': str, 
                         'editable': True, 
                         'nullable': True, 
                         'widget': 'color', 
                         'operators': _text_operators}, 
   camelot.types.Rating: lambda f: {'delegate': delegates.StarDelegate, 
                          'editable': True, 
                          'nullable': True, 
                          'python_type': int, 
                          'widget': 'star', 
                          'from_string': int_from_string, 
                          'operators': _numerical_operators}, 
   camelot.types.Enumeration: lambda f: {'delegate': delegates.ComboBoxDelegate, 
                               'python_type': str, 
                               'choices': [ (v, enumeration_to_string(v)) for v in f.choices ], 'from_string': lambda s: dict((enumeration_to_string(v), v) for v in f.choices)[s], 
                               'minimal_column_width': max(len(enumeration_to_string(v)) for v in f.choices), 
                               'editable': True, 
                               'nullable': True, 
                               'widget': 'combobox', 
                               'operators': _numerical_operators}, 
   camelot.types.Language: lambda f: {'delegate': delegates.LanguageDelegate, 
                            'python_type': str, 
                            'default': default_language, 
                            'from_string': string_from_string, 
                            'editable': True, 
                            'nullable': False, 
                            'widget': 'combobox'}, 
   camelot.types.File: lambda f: {'python_type': str, 
                        'editable': True, 
                        'delegate': delegates.FileDelegate, 
                        'storage': f.storage, 
                        'operators': _text_operators, 
                        'remove_original': False}}

class DummyField(object):

    def __init__(self):
        self.length = 20
        self.parts = ['AAA', '99']
        self.choices = ['planned', 'canceled']
        self.precision = 2
        self.scale = 2
        self.storage = None
        self.separator = '.'
        return


row_separator = '+' + '-' * 50 + '+' + '-' * 100 + '+' + '-' * 70 + '+'
row_format = '| %-48s | %-98s | %-68s |'
doc = 'Field types handled through introspection :\n\n' + row_separator + '\n' + row_format % ('**Field type**',
                                                                                               '**Default delegate**',
                                                                                               '**Default editor**') + '\n' + row_separator + '\n'
field_types = _sqlalchemy_to_python_type_.keys()
field_types.sort(lambda x, y: cmp(x.__name__, y.__name__))
for field_type in field_types:
    field_attributes = _sqlalchemy_to_python_type_[field_type](DummyField())
    delegate = field_attributes['delegate']
    row = row_format % (':class:`' + field_type.__module__ + '.' + field_type.__name__ + '`',
     ':class:`' + delegate.__module__ + '.' + delegate.__name__ + '`',
     '.. image:: /_static/editors/%s_editable.png' % delegate.editor.__name__)
    doc += row + '\n' + row_separator + '\n'

doc += '\n'
__doc__ = doc