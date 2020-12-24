# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/pg_encodings.py
# Compiled at: 2017-02-15 04:26:41
# Size of source mod 2**32: 627 bytes
from encodings import normalize_encoding, aliases
from types import MappingProxyType
from psycopg2.extensions import encodings as _PG_ENCODING_MAP
PG_ENCODING_MAP = MappingProxyType(_PG_ENCODING_MAP)
_PYTHON_ENCODING_MAP = {v:k for k, v in PG_ENCODING_MAP.items()}

def get_postgres_encoding(python_encoding: str) -> str:
    """Python to postgres encoding map."""
    encoding = normalize_encoding(python_encoding.lower())
    encoding_ = aliases.aliases[encoding.replace('_', '', 1)].upper()
    pg_encoding = PG_ENCODING_MAP[encoding_.replace('_', '')]
    return pg_encoding