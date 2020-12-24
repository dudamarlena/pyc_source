# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ETL\transform.py
# Compiled at: 2020-01-14 18:43:38
# Size of source mod 2**32: 294 bytes


class Transform:

    def __init__(self, transformation_function, *args, **kwargs):
        self.transformation_function = transformation_function
        self.args = args
        self.kwargs = kwargs

    def __call__(self, df):
        return self.transformation_function(df, *self.args, **self.kwargs)