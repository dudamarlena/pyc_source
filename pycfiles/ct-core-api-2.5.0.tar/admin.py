# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/db/admin.py
# Compiled at: 2019-08-05 00:35:42
from cantools.db import get_model, get_schema, put_multi
from cantools.util import log

def index(kind, i=0):
    kinds = kind == '*' and list(get_schema().keys()) or [kind]
    puts = []
    for kind in kinds:
        mod = get_model(kind)
        schema = get_schema(kind)
        q = mod.query()
        for prop in ['created', 'modified', 'date']:
            if prop in schema:
                q.order(getattr(mod, prop))
                break

        items = q.fetch()
        log('assigning sequential index properties to %s %s records' % (len(items), kind), important=True)
        for n in range(len(items)):
            item = items[n]
            i += 1
            item.index = i
            if n and not n % 100:
                log('processed %s %s entities' % (n, kind), 1)

        log('processed %s %s entities' % (len(items), kind))
        puts += items

    log('saving %s records' % (len(puts),), important=True)
    put_multi(puts)
    return i