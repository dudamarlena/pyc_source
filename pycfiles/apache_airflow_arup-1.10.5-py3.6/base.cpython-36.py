# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/base.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1219 bytes
from typing import Any
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
import airflow
SQL_ALCHEMY_SCHEMA = airflow.configuration.get('core', 'SQL_ALCHEMY_SCHEMA')
metadata = None if not SQL_ALCHEMY_SCHEMA or SQL_ALCHEMY_SCHEMA.isspace() else MetaData(schema=SQL_ALCHEMY_SCHEMA)
Base = declarative_base(metadata=metadata)
ID_LEN = 250