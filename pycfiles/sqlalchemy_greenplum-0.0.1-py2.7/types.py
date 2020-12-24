# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sqlalchemy_greenplum\types.py
# Compiled at: 2018-03-20 22:05:17
from sqlalchemy import types as sqltypes
from sqlalchemy.util import compat

class TINYINT(sqltypes.TypeEngine):
    __visit_name__ = 'TINYINT'


class DOUBLE(sqltypes.Float):
    __visit_name__ = 'DOUBLE'


class BOOLEAN(sqltypes.Boolean):

    def get_dbapi_type(self, dbapi):
        return dbapi.NUMBER


class DATE(sqltypes.Date):

    def literal_processor(self, dialect):
        self.bind_processor(dialect)

        def process(value):
            return "to_date('%s')" % value

        return process


class TIME(sqltypes.Time):

    def literal_processor(self, dialect):
        self.bind_processor(dialect)

        def process(value):
            return "to_time('%s')" % value

        return process


class TIMESTAMP(sqltypes.DateTime):

    def literal_processor(self, dialect):
        self.bind_processor(dialect)

        def process(value):
            return "to_timestamp('%s')" % value

        return process


class _LOBMixin(object):

    def result_processor(self, dialect, coltype):
        if not dialect.auto_convert_lobs:
            return None
        else:

            def process(value):
                if isinstance(value, compat.string_types):
                    return value
                else:
                    if compat.py2k and isinstance(value, buffer):
                        return value
                    else:
                        if value is not None:
                            return value.read()
                        return value

                    return

            return process


class HanaText(_LOBMixin, sqltypes.Text):

    def get_dbapi_type(self, dbapi):
        return dbapi.CLOB


class HanaUnicodeText(_LOBMixin, sqltypes.UnicodeText):

    def get_dbapi_type(self, dbapi):
        return dbapi.NCLOB

    def result_processor(self, dialect, coltype):
        lob_processor = _LOBMixin.result_processor(self, dialect, coltype)
        if lob_processor is None:
            return
        else:
            string_processor = sqltypes.UnicodeText.result_processor(self, dialect, coltype)
            if string_processor is None:
                return lob_processor

            def process(value):
                return string_processor(lob_processor(value))

            return process
            return


class HanaBinary(_LOBMixin, sqltypes.LargeBinary):

    def get_dbapi_type(self, dbapi):
        return dbapi.BLOB

    def bind_processor(self, dialect):
        return


class NCLOB(sqltypes.Text):
    __visit_name__ = 'NCLOB'