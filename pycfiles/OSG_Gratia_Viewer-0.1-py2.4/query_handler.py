# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gratia/database/query_handler.py
# Compiled at: 2008-01-29 17:13:05
from graphtool.database.query_handler import results_parser

def displayName(*args, **kw):
    dn = args[0]
    parts = dn.split('/')
    display = 'Unknown'
    for part in parts:
        if len(part) == 0:
            continue
        try:
            (attr, val) = part.split('=', 1)
        except:
            continue

        if attr == 'CN':
            display = val

    try:
        parts = display.split()
        dummy = int(parts[(-1)])
        display = display[:-len(parts[(-1)]) - 1]
    except:
        pass

    proper = ''
    for parts in display.split():
        proper += parts[0].upper() + parts[1:].lower() + ' '

    return proper[:-1]


def fake_parser(results, **kw):
    return (
     results, kw)


def table_parser(results, columns='column1, column2', **kw):
    columns = [ i.strip() for i in columns.split(',') ]
    column_len = len(columns)
    retval = []
    for row in results:
        entry = {}
        for i in range(column_len):
            entry[columns[i]] = row[i]

    return (
     retval, kw)


def opportunistic_usage_parser(sql_results, vo='Unknown', globals=globals(), **kw):
    (vo_listing, dummy) = globals['RegistrationQueries'].ownership_query()
    ownership = []
    for (v, site) in vo_listing:
        if vo.lower() == v.lower():
            ownership.append(site)

    def pivot_transform(arg, **kw):
        if arg in ownership:
            return
        return arg

    try:
        kw.pop('pivot_transform')
    except:
        pass

    return results_parser(sql_results, pivot_transform=pivot_transform, globals=globals, vo=vo, **kw)


def opportunistic_usage_parser2(sql_results, vo='Unknown', globals=globals(), **kw):
    (vo_listing, dummy) = globals['RegistrationQueries'].ownership_query()
    ownership = []
    for (v, site) in vo_listing:
        if vo.lower() == v.lower():
            ownership.append(site)

    def pivot_transform(arg, **kw):
        if arg in ownership:
            return 'Owned'
        return 'Opportunistic'

    try:
        kw.pop('pivot_transform')
    except:
        pass

    return results_parser(sql_results, pivot_transform=pivot_transform, globals=globals, vo=vo, **kw)