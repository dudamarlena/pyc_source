# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/scope_level.py
# Compiled at: 2020-05-13 11:17:34
# Size of source mod 2**32: 509 bytes
from typing import Union
from datalogue.errors import DtlError, _enum_parse_error
from datalogue.dtl_utils import SerializableStringEnum

class Scope(SerializableStringEnum):
    User = 'User'
    Group = 'Group'
    Organization = 'Organization'

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error('share target', s))

    @staticmethod
    def from_string(string: str) -> Union[(DtlError, 'Scope')]:
        return SerializableStringEnum.from_str(Scope)(string)