# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/errors.py
# Compiled at: 2015-08-17 17:37:49


class FileNotFindError(Exception):

    def __init__(self, file):
        message = ('Static file "{file}" not find').format(file=file)
        super(FileNotFindError, self).__init__(message)