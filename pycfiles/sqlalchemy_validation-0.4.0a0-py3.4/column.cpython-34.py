# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlalchemy_validation/column.py
# Compiled at: 2015-12-31 01:46:45
# Size of source mod 2**32: 1579 bytes
"""
"""
import sqlalchemy
from .validate_column import ColumnValidator

class Column(sqlalchemy.Column):
    __doc__ = '\n    Attributes:\n      size: A tuple or None.\n      regexp: A re.RegexObject or None.\n      length: A tuple or None.\n      format: A str or None.\n      validator: A ColumnValidator instance.\n    '

    def __init__(self, *args, **kwargs):
        """This constructor receive additional keyword arguments
        to define additional validations.

        *args
          These arguments is passed to the sqlalchemy.Column contructor.

        **kwargs
          size: Define the size validation.
            tuple (min, max)
          length: Define the length validation.
            tuple (min, max)
            This param only works on string columns.
          reqexp: Define the RegExp validation.
            re.RegexObject
          format: Define the format validation.
            ENUM("email")
        """
        self.size = kwargs.pop('size', None)
        self.regexp = kwargs.pop('regexp', None)
        self.length = kwargs.pop('length', None)
        self.format = kwargs.pop('format', None)
        if 'autoincrement' not in kwargs:
            kwargs['autoincrement'] = False
        super(Column, self).__init__(*args, **kwargs)
        type_length = getattr(self.type, 'length', None)
        if type_length:
            if self.length is None:
                self.length = (
                 None, type_length)
        else:
            if self.length[1] is None:
                self.length = (
                 self.length[0], type_length)
            self.validator = ColumnValidator(self)