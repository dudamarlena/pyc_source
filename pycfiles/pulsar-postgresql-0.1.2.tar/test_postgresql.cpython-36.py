# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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