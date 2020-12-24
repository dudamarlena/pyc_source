# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/pandas_translator.py
# Compiled at: 2020-03-31 04:55:26
# Size of source mod 2**32: 1630 bytes
from typing import List
from toucan_connectors.condition_translator import ConditionTranslator

class PandasConditionTranslator(ConditionTranslator):
    __doc__ = '\n    Utility class to convert a condition object into pandas.query format\n\n    This is a default way to apply a data filter in connectors, after data has\n    been requested and received.\n    '

    @classmethod
    def get_column_ref(cls, column: str) -> str:
        """To refer column names (even with spaces or operators), we surround them in backticks"""
        return f"`{column}`"

    @classmethod
    def get_value_str_ref(cls, value: str) -> str:
        return f"'{value}'"

    @classmethod
    def join_clauses(cls, clauses: List[str], logical_operator: str) -> str:
        return '(' + f" {logical_operator} ".join(clauses) + ')'

    @classmethod
    def EQUAL(cls, column, value) -> str:
        return f"{column} == {value}"

    @classmethod
    def NOT_EQUAL(cls, column, value) -> str:
        return f"{column} != {value}"

    @classmethod
    def LOWER_THAN(cls, column, value) -> str:
        return f"{column} < {value}"

    @classmethod
    def LOWER_THAN_EQUAL(cls, column, value) -> str:
        return f"{column} <= {value}"

    @classmethod
    def GREATER_THAN(cls, column, value) -> str:
        return f"{column} > {value}"

    @classmethod
    def GREATER_THAN_EQUAL(cls, column, value) -> str:
        return f"{column} >= {value}"

    @classmethod
    def IN(cls, column, value) -> str:
        return f"{column} in {value}"

    @classmethod
    def NOT_IN(cls, column, value) -> str:
        return f"{column} not in {value}"