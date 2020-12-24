# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/__init__.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 1167 bytes
"""
Main package for asyncqlio - a Python 3.5+ async ORM built on top of asyncio.

.. currentmodule:: asyncqlio

.. autosummary::
    :toctree:

    db
    orm
    backends

    exc
    meta
"""
__author__ = 'Laura Dickinson'
__copyright__ = 'Copyright (C) 2017 Laura Dickinson'
__licence__ = 'MIT'
__status__ = 'Development'
from pkg_resources import DistributionNotFound, get_distribution
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass

from asyncqlio.backends.base import BaseConnector, BaseDialect, BaseResultSet, BaseTransaction
from asyncqlio.db import DatabaseInterface
from asyncqlio.exc import *
from asyncqlio.orm.inspection import get_pk, get_row_history, get_row_session
from asyncqlio.orm.schema.column import Column
from asyncqlio.orm.schema.relationship import ForeignKey, Relationship
from asyncqlio.orm.schema.table import Table, table_base
from asyncqlio.orm.schema.types import BigInt, Boolean, ColumnType, Integer, SmallInt, String, Text, Timestamp
from asyncqlio.orm.session import Session