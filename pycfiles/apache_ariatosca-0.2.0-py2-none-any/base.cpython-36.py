# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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