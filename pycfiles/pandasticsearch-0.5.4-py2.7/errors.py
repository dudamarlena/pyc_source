# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pandasticsearch/errors.py
# Compiled at: 2018-09-25 01:28:44


class PandasticSearchException(RuntimeError):

    def __init__(self, msg):
        super(PandasticSearchException, self).__init__(msg)


class NoSuchDependencyException(PandasticSearchException):
    pass


class ServerDefinedException(PandasticSearchException):
    pass


class ParseResultException(PandasticSearchException):
    pass


class DataFrameException(PandasticSearchException):
    pass