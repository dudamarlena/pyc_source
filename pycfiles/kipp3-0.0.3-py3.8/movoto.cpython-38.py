# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp/models/movoto.py
# Compiled at: 2019-11-08 04:26:21
# Size of source mod 2**32: 5583 bytes
"""
----------------
Movoto Databases
----------------

"""
from __future__ import unicode_literals
from collections import namedtuple
from past.builtins import basestring
from kipp.libs.aio import run_until_complete, Future
from .base import BaseDB, as_coroutine
from .exceptions import DBValidateError, DuplicateIndexError, RecordNotFound

class RuntimeStats:
    __doc__ = 'Create/Get/Update/Delete runtime status into movotodb\n\n    Usage:\n    ::\n        from kipp.models import MovotoDB\n\n        movotodb = MovotoDB()\n\n        movotodb.create_runtime_stats(name, stats=None)\n        movotodb.update_runtime_stats(name, stats)\n        movotodb.delete_runtime_stats(name)\n        movotodb.get_runtime_stats(name)\n        is_runtime_stats_exists(name)\n\n    Asynchronous Usage:\n    ::\n        from kipp.models import MovotoDB\n\n        movotodb = MovotoDB(is_aio=True)\n\n        yield movotodb.create_runtime_stats(name, stats=None)\n        yield movotodb.update_runtime_stats(name, stats)\n        yield movotodb.delete_runtime_stats(name)\n        yield movotodb.get_runtime_stats(name)\n\n    '
    _sql_to_create_runtime_stats = '\n        insert into runtime_stats (name, stats)\n        values (%s, %s);\n        '
    _sql_to_update_runtime_stats = '\n        update runtime_stats\n        set stats=%s\n        where name=%s;\n        '
    _RuntimeStats = namedtuple('stats', ['created_at', 'updated_at', 'stats'])
    _sql_to_get_runtime_stats = '\n        select created_at, updated_at, stats\n        from runtime_stats\n        where name=%s;\n        '
    _sql_to_delete_runtime_stats = '\n        delete from runtime_stats\n        where name=%s;\n        '

    def validate_stats(self, stats):
        try:
            assert stats, 'stats should not empty'
            assert isinstance(stats, basestring), 'stats should be ``str``'
            assert len(stats) <= 200, 'the length of stats should shorter than 200'
        except AssertionError as err:
            try:
                raise DBValidateError(*err.args)
            finally:
                err = None
                del err

    def validate_name(self, name):
        try:
            assert name, 'name should not empty'
            assert isinstance(name, basestring), 'name should be ``str``'
            assert len(name) <= 50, 'the length of name should shorter than 50'
        except AssertionError as err:
            try:
                raise DBValidateError(*err.args)
            finally:
                err = None
                del err

    @as_coroutine
    def create_runtime_stats(self, name, stats=None):
        """
        Args:
            name (str): new name
            stats (str, default=None): new stats

        Raises:
            DuplicateIndexError: if exists in db
            DBValidateError: if name/stats invalidate
        """
        self.validate_name(name)
        if stats:
            self.validate_stats(stats)
        try:
            r = self.conn.executeBySql(self._sql_to_create_runtime_stats, name, stats)
        except self.get_mysqldb_exception('IntegrityError') as err:
            try:
                if len(err.args) >= 2 and str(err.args[1]).startswith('Duplicate entry '):
                    raise DuplicateIndexError('Duplicate name in ``runtime_stats`` for {}'.format(name))
                else:
                    raise
            finally:
                err = None
                del err

        else:
            return r

    @as_coroutine
    def update_runtime_stats(self, name, stats, upsert=False):
        """
        Args:
            upsert (bool, default=False): create if not exists

        Raises:
            DBValidateError: if name/stats invalidate

        Returns:
            int: how many lines influenced
        """
        self.validate_name(name)
        self.validate_stats(stats)
        r = self.conn.executeBySql(self._sql_to_update_runtime_stats, stats, name)
        if not int(r):
            if upsert:
                r = self.create_runtime_stats(name, stats)
                if isinstance(r, Future):
                    run_until_complete(r)
                    return r.result()
        return r

    @as_coroutine
    def get_runtime_stats(self, name, **kwargs):
        """Load runtime stats by name

        Args:
            name (str): name of the stats
            default (optional): do not raises RecordNotFound

        Raises:
            RecordNotFound: if not found and no default is specified
            DBValidateError: if name invalidate

        Returns:
            namedtuple: ('created_at', 'updated_at', 'stats')
        """
        self.validate_name(name)
        r = self.conn.getOneBySql(self._sql_to_get_runtime_stats, name)
        if not r:
            if 'default' in kwargs:
                return kwargs['default']
            raise RecordNotFound('Can not find stats via name {}'.format(name))
        return (self._RuntimeStats)(*r)

    @as_coroutine
    def delete_runtime_stats(self, name):
        """
        Raises:
            DBValidateError: if name invalidate
        """
        self.validate_name(name)
        return self.conn.executeBySql(self._sql_to_delete_runtime_stats, name)

    @as_coroutine
    def is_runtime_stats_exists(self, name):
        """Check whether name exists in runtime_stats

        Raises:
            DBValidateError: if name invalidate

        Returns:
            bool: is name exists
        """
        f = self.get_runtime_stats(name, default=None)
        if isinstance(f, Future):
            run_until_complete(f)
            return f.result() is not None
        return f is not None


class MovotoDB(BaseDB, RuntimeStats, object):
    __db_name__ = 'movoto'