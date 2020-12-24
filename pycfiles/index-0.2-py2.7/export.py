# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\export.py
# Compiled at: 2013-09-27 04:08:30
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, os, importlib, logging
from .lib.settings import Settings
from .lib.data_funcs import get_list
from .lib.db import initDb, initlinks, foreign_keys, foreign_keys_c
from .reg import set_object
from .reg.result import reg_error, reg_exception

def Proceed(sources, options={}, tree_widget=None, status=None):
    ROOT = set_object(b'Root', tree_widget, brief=options)
    if hasattr(ROOT, b'tree_item'):
        ROOT.tree_item.setSelected(True)
    handler = options.get(b'handler', b'proceed_default')
    try:
        current = __package__ + b'.' + handler
        handler_module = importlib.import_module(current)
        models_module = importlib.import_module(b'.models', current)
    except Exception as e:
        reg_exception(ROOT, e)
        return

    if not hasattr(handler_module, b'proceed'):
        reg_error(ROOT, (b"No 'proceed' function in handler '{0}'").format(handler))
        return
    dbconfig = options.get(b'db', {})
    try:
        session = initDb(dbconfig, base=models_module.Base)
        initlinks(models_module.Base)
        set_object(b'session', tree_widget, brief=session)
    except Exception as e:
        reg_exception(ROOT, e)
        return

    if isinstance(status, dict):
        status[b'dirs'] = 0
        status[b'files'] = 0
    sources = get_list(sources)
    for source in sources:
        handler_module.proceed(source, options, session, ROOT, status)

    if isinstance(status, dict) and b'break' in status:
        status.pop(b'break')
    try:
        session.commit()
    except Exception as e:
        reg_exception(ROOT, e)


def main(files=None, method=None):
    if files:
        if method:
            s = Settings()
            profiles = s.get_group(b'profiles')
            if profiles.contains(method, dict):
                options = profiles.get_group(method).get_dict()
            else:
                text = (b"Required method not exists: '{0}'!").format(method)
                logging.warning(text)
                return
        else:
            options = {}
        Proceed(files, options)
    else:
        logging.warning(b'Files not specified!')