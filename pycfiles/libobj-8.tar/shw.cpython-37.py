# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bart/libobj/mods/shw.py
# Compiled at: 2020-03-03 07:58:36
# Size of source mod 2**32: 1768 bytes
import lo, os, threading, time

def cfg(event):
    if not lo.workdir:
        raise AssertionError
    else:
        if not event.args:
            files = [x.split('.')[(-2)].lower() for x in os.listdir(os.path.join(lo.workdir, 'store')) if x.endswith('Cfg')]
            if files:
                event.reply('|'.join(['main'] + list(set(files))))
            else:
                event.reply('no configuration files yet.')
            return
        target = event.args[0]
        if target == 'main':
            event.reply(lo.cfg)
            return
        cn = 'lo.%s.Cfg' % target
        db = lo.Db()
        l = db.last(cn)
        l or event.reply('no %s found.' % cn)
        return
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        event.reply(l.get(event.args[1]))
        return
    setter = {event.args[1]: event.args[2]}
    l.edit(setter)
    l.save()
    event.reply('ok')


def ps(event):
    psformat = '%-8s %-50s'
    result = []
    for thr in sorted((threading.enumerate()), key=(lambda x: x.getName())):
        if str(thr).startswith('<_'):
            continue
        else:
            d = vars(thr)
            o = lo.Object()
            o.update(d)
            if o.get('sleep', None):
                up = o.sleep - int(time.time() - o.state.latest)
            else:
                up = int(time.time() - lo.starttime)
        result.append((up, thr.getName(), o))

    nr = -1
    for up, thrname, o in sorted(result, key=(lambda x: x[0])):
        nr += 1
        res = '%s %s' % (nr, psformat % (lo.tms.elapsed(up), thrname[:60]))
        if res.strip():
            event.reply(res)


def up(event):
    event.reply(lo.tms.elapsed(time.time() - lo.starttime))


def v(event):
    event.reply('%s %s' % (lo.cfg.name.upper(), lo.__version__))