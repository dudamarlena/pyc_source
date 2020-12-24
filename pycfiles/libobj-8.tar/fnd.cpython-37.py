# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bart/libobj/mods/fnd.py
# Compiled at: 2020-03-03 07:58:36
# Size of source mod 2**32: 599 bytes
import lo, os, time

def find(event):
    if not event.args:
        wd = os.path.join(lo.workdir, 'store', '')
        lo.cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split('.')[(-1)].lower() for x in fns})
        if fns:
            event.reply('|'.join(fns))
    else:
        return
        len(event.args) > 1 or event.reply('find <type> <match>')
        return
    match = event.args[0]
    nr = -1
    db = lo.dbs.Db()
    for o in db.find_value(match, event.args[1]):
        nr += 1
        event.display(o, str(nr))