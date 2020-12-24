# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/src/cdbcli/build/lib/cdbcli/completer.py
# Compiled at: 2016-07-15 00:01:39
import functools
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from .grammar import grammar
from .commands import COMMANDS, get_all_dbs, is_view

def _fetch_db_names(environment, couch_server):
    try:
        return get_all_dbs(environment, couch_server)
    except RuntimeError:
        return []


def _fetch_doc_ids(environment, couch_server):
    if environment.current_db is None:
        return []
    else:
        return list(environment.current_db)


def _fetch_view_ids(environment, couch_server):
    if environment.current_db is None:
        return []
    else:
        return filter(is_view, list(environment.current_db))


def get_completer(environment, couch_server):
    return GrammarCompleter(grammar, {'command': WordCompleter(COMMANDS.keys()), 
       'database_name': WordCompleter(functools.partial(_fetch_db_names, environment, couch_server)), 
       'doc_id': WordCompleter(functools.partial(_fetch_doc_ids, environment, couch_server)), 
       'view_id': WordCompleter(functools.partial(_fetch_view_ids, environment, couch_server))})