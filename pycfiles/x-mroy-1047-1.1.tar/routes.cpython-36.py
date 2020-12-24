# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dr/Documents/code/Python/vps-manager/web/routes.py
# Compiled at: 2019-05-31 03:50:24
# Size of source mod 2**32: 2825 bytes
import os, random, json, asyncio
from ashares.remote import AsyncConnection
from enuma_elish.book import Book
import logging

def select_routes(geo=None, number=3, entry=None, out=None, exclude=None, ss_dir='/tmp/ss-random'):
    confs = []
    for f in os.listdir(ss_dir):
        with open(os.path.join(ss_dir, f)) as (fp):
            confs.append(json.load(fp))

    random.shuffle(confs)

    def whereis(conf, exclude=None, include=None, n=3):
        if not geo:
            return 'Unknow'
        else:
            ip = conf.get('server')
            name = geo.city(ip).city.name
            name = name if name else 'Unknow'
            return name.lower()

    code = 0
    if not entry:
        code ^= 1
    if not out:
        code ^= 2
    bak = []
    b = []
    for c in confs:
        city = whereis(c)
        if entry:
            if not isinstance(entry, dict):
                if entry in city:
                    entry = c
        if out:
            if not isinstance(out, dict):
                if out in city:
                    out = c
        if exclude:
            if exclude in city:
                continue
        bak.append(c)

    if not isinstance(entry, dict):
        code ^= 1
        entry = random.choice(bak)
        bak.remove(entry)
    if not isinstance(out, dict):
        code ^= 2
        out = random.choice(bak)
        bak.remove(out)
    if number < 3:
        return [entry, out]
    else:
        for i in range(number - 2):
            o = random.choice(bak)
            bak.remove(o)
            b.append(o)

        return (
         code, [entry] + b + [out])


async def ensure_func(host, ss_dir):
    ip = host.host
    port = int(host.port)
    pwd = host.passwd
    conf_path = os.path.join(ss_dir, ip)
    if not os.path.exists(conf_path):
        a = AsyncConnection(host=ip, name='root', port=port, password=pwd, keyfile=None)
        a.timeout_t = 12
        _, _, t, _ = await a.tcp_ping(port)
        if t < 999:
            res = await a.enuma_elish()
            if len(res) > 1:
                if res[(-1)] == 0:
                    return True
            logging.error(str(res))
        else:
            logging.error('22 port is not connected')
        return False
    else:
        return True


async def _init_routes(db, Obj, ss_dir):
    try:
        hosts = [i for i in db.query(Obj)]
        s = [ensure_func(host, ss_dir) for host in hosts]
        return await (asyncio.gather)(*s)
    except Exception as e:
        raise e


def init_routes(db, Obj, ss_dir):
    loop = asyncio.new_event_loop()
    uset = loop.run_until_complete(_init_routes(db, Obj, ss_dir))


def build_routes(confs):
    for i in range(len(confs)):
        confs[i]['server_port'] = int(confs[i]['server_port'])

    return Book.Links(confs)