# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/model/translate_errors.py
# Compiled at: 2015-04-13 09:33:08
# Size of source mod 2**32: 4313 bytes
"""Translates Postgresql database errors back to "user speak".
"""
import re
from flask import current_app
from .utils import lookup_model
_get_name_re = re.compile('"([^"]*)"[^"]*$')

def translate_error(exc_val):
    """Returns a sequence of (column, message).
    """
    print('translate_error: args', exc_val.args)
    print('translate_error: connection_invalidated', exc_val.connection_invalidated)
    print('translate_error: detail', exc_val.detail)
    print('translate_error: statement', exc_val.statement)
    print('translate_error: params', exc_val.params)
    pgexc = exc_val.orig
    pgcode = pgexc.pgcode
    pgerror = pgexc.pgerror
    lines = pgerror.split('\n')
    m = _get_name_re.search(lines[0])
    if m:
        name = m.group(1)
    else:
        name = None
    if pgcode == '23502':
        assert name
        _get_table_key(exc_val)
        return (
         (
          name, 'Required field.'),)
    if pgcode == '23505':
        _get_table_key(exc_val)
        if name in current_app.dry_unique_constraints:
            return current_app.dry_unique_constraints[name]
    if pgcode == '23503':
        _get_table_key(exc_val)
        if name in current_app.dry_foreign_key_constraints:
            return (
             current_app.dry_foreign_key_constraints[name],)
    cause = pgexc.__cause__
    d = dict(pgcode=pgcode, pgerror=pgerror, name=name, cause=str(cause), pgexc={k:repr(getattr(pgexc, k)) for k in dir(pgexc) if not k.startswith('_')})
    if cause:
        d['cause_exc'] = {k:repr(getattr(cause, k)) for k in dir(cause) if not k.startswith('_')}
    return (('unknown', d),)


_table_name_re = re.compile('(?: *update +(\\w+) | *insert +into +(\\w+) | *delete +from +(\\w+) )', re.I)

def _get_table_key(exc_val):
    """Returns command, tablename, key.

    Command is one of: 'insert', 'update' or 'delete'.

    If key can not be determined (such as for an autoincrement insert row),
    None if returned.

    If nothing can be determined, returns None, None, None.
    """
    match = _table_name_re.match(exc_val.statement)
    if not match:
        return (None, None, None)
    if match.group(1):
        command = 'update'
        table = match.group(1)
    else:
        if match.group(2):
            command = 'insert'
            table = match.group(2)
        else:
            assert match.group(3)
            command = 'delete'
            table = match.group(3)
        model = lookup_model(table)
        key_column = model._dry_key_column()
        params = exc_val.params
        if key_column in params:
            print('found', key_column)
            key = params[key_column]
        else:
            tbl_key = '{}_{}'.format(table, key_column)
            if tbl_key in params:
                print('found', tbl_key)
                key = params[tbl_key]
            else:
                print('key not found')
                key = None
    print('command', command, 'table', table, 'key_column', key_column, 'key', key)
    return (command, table, key)