# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/model/utils.py
# Compiled at: 2015-04-14 09:00:05
# Size of source mod 2**32: 2607 bytes
"""Misc database helper functions:

 * :class:`transaction`
 * :func:`now_truncated`
 * :func:`get_current_user_id`
"""
import sys
from datetime import datetime
from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import current_user
__all__ = ('transaction', 'now_truncated', 'get_current_user_id')
db = SQLAlchemy()

def lookup_model(tablename):
    return current_app.dry_models_by_tablename[tablename]


def names_from_module(module):
    """Generates all names in module that don't start with an '_'.
    """
    for name in dir(module):
        if not name.startswith('_'):
            yield getattr(module, name)
            continue


class transaction:
    __doc__ = 'Ensures that the transaction is terminated at the end of code block.\n\n    Does a `commit` on normal exit of the code block, and `rollback` if an\n    exception is thrown out of the code block.\n\n    This is simply a `context manager`_ to be used in the with statement.\n\n    .. _context manager: https://docs.python.org/3/library/stdtypes.html#context-manager-types\n    '

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            commit_exc = False
            if exc_type is None:
                try:
                    db.session.commit()
                    return
                except Exception as e:
                    exc_type, exc_val, exc_tb = sys.exc_info()
                    assert exc_val is e
                    commit_exc = True

            db.session.rollback()
            if commit_exc:
                raise exc_val
        finally:
            db.session.close()


def now_truncated():
    """Return utcnow_, truncating the microseconds.

    Postgresql rounds microseconds while python truncates.  So they may
    not match, which screws up Last-Modified checks.

    .. _utcnow: https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
    """
    return datetime.utcnow().replace(microsecond=0)


def get_current_user_id():
    """Returns the current_user_ id, if a user is logged in.

    Else returns None.

    .. _current_user: https://flask-login.readthedocs.org/en/latest/#flask.ext.login.current_user
    """
    if current_user.is_authenticated():
        return current_user.id