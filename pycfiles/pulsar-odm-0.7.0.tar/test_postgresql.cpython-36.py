# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/tests/test_postgresql.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 780 bytes
from tests import base

@base.green
class PostgreSqlTests(base.TestCase, base.MapperMixin):

    @classmethod
    def url(cls):
        if '+green' in cls.cfg.postgresql:
            return cls.cfg.postgresql + '?pool_size=7&pool_timeout=15'
        else:
            return cls.cfg.postgresql

    def test_pool(self):
        from odm.dialects.postgresql import PGDGreen, GreenletPool
        engine = self.mapper.get_engine()
        if isinstance(engine.dialect, PGDGreen):
            self.assertIsInstance(engine.pool, GreenletPool)
            self.assertEqual(engine.pool.max_size(), 7)
            self.assertEqual(engine.pool.timeout(), 15)

    def test_dialect(self):
        dialect = self.mapper.dialect('task')
        self.assertEqual(dialect.name, 'postgresql')