# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wtforms_jsonschema2/exceptions.py
# Compiled at: 2018-04-16 02:30:23
# Size of source mod 2**32: 243 bytes


class UnsupportedFieldException(Exception):
    __doc__ = "\n    Raised when an attempt is made to convert a field that we don't understand.\n    "

    def __init__(self, field_class):
        self.message = 'Field %s is not supported.' % field_class