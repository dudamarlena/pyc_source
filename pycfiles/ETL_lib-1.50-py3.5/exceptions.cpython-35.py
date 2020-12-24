# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ETL\exceptions.py
# Compiled at: 2020-01-14 18:43:38
# Size of source mod 2**32: 665 bytes


class NoTablesDefinedException(Exception):
    __doc__ = 'Exception raised when trying to use a function without a sufficiently detailed\n  set of params.\n\n  The function is necessitating a Config instance with a set of params itself\n  containing detailed informations about tables.\n\n  '

    def __init__(self, func):
        message = 'Instanciate config with a set of params with more details in order to use {}.{}\nOr you may want to use lower level functions from json_utils or delta_utils modules instead.'.format(func.__module__, func.__name__)
        self.message = message

    def __str__(self):
        return self.message