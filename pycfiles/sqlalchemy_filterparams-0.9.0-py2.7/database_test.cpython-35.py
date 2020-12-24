# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cbrand/projects/python-sqlalchemy-filterparams/build/lib/sqlalchemy_filterparams_tests/database_test.py
# Compiled at: 2016-02-20 17:15:20
# Size of source mod 2**32: 486 bytes
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filterparams_tests.models import Base

class BaseDatabaseTest(TestCase):
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)