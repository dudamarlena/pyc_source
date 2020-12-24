# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/t/work/cihai/cihai/cihai/db.py
# Compiled at: 2019-08-17 05:41:51
# Size of source mod 2**32: 1258 bytes
"""Cihai core functionality."""
from __future__ import absolute_import, print_function, unicode_literals
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

class Database(object):
    __doc__ = '\n    Cihai SQLAlchemy instance\n    '

    def __init__(self, config):
        self.engine = create_engine(config['database']['url'])
        self.metadata = MetaData()
        self.metadata.bind = self.engine
        self.reflect_db()
        self.session = Session(self.engine)

    def reflect_db(self):
        """
        No-op to reflect db info.

        This is available as a method so the database can be reflected
        outside initialization (such bootstrapping unihan during CLI usage).
        """
        self.metadata.reflect(views=True, extend_existing=True)
        self.base = automap_base(metadata=(self.metadata))
        self.base.prepare()

    engine = None
    metadata = None
    session = None
    base = None