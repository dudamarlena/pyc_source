# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlalchemy_hawq/point.py
# Compiled at: 2019-10-07 13:43:57
# Size of source mod 2**32: 1939 bytes
"""
Defines Hawq point type for use by Sqlalchemy
"""
import re
from sqlalchemy.types import UserDefinedType

class SQLAlchemyHawqException(Exception):
    __doc__ = '\n    Custom exception name for Hawq-Sqlalchemy package\n    '


class Point(UserDefinedType):
    __doc__ = '\n    Wrapper for a 2-element tuple.\n    The Point type is available in HAWQ db and postgres DBAPI, but not in SQLAlchemy.\n    '

    def get_col_spec(value):
        """
        Returns type name.
        get_col_spec must be overridden when implementing a custom class.
        """
        return 'POINT'

    def bind_processor(self, dialect):
        """
        Returns a method to convert the tuple input to a its SQL string.
        """

        def process(value):
            if value is None:
                return
            try:
                val1, val2 = value
                if val1 is None or val2 is None:
                    if val1 is not None or val2 is not None:
                        raise SQLAlchemyHawqException('Both values must be non-null or no data will be saved for Point({})'.format(value))
                    return
                return str(value)
            except (ValueError, TypeError):
                raise SQLAlchemyHawqException('Unexpected input type for Point ({})'.format(value))

        return process

    def result_processor(self, dialect, coltype):
        """
        Transforms the SQL string into a Python tuple.
        Point((float x),(float y)) -> (float x, float y)
        """

        def process(value):
            if value is None:
                return
            match = re.match('^\\((?P<x>\\d+(\\.\\d+)?),(?P<y>\\d+(\\.\\d+)?)\\)$', value)
            if match:
                return (
                 float(match.group('x')), float(match.group('y')))
            raise SQLAlchemyHawqException('Failed to get Point value from SQL ({})'.format(value))

        return process