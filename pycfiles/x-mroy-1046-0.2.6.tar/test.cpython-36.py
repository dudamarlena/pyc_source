# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dr/Documents/code/Python/Projects/ControllProxy/seed/mrpackage/test.py
# Compiled at: 2018-06-24 23:47:33
# Size of source mod 2**32: 1433 bytes
import os, socket, asyncio, time, async_timeout
from seed.mrpackage.config import SEED_HOME, DB_PATH, Host, Cache
from seed.mrpackage.udp import open_remote_endpoint
from seed.mrpackage.libs import loger
from asynctools.servers import Connection
log = loger()

async def check_up(ip, loop, msg='-v'):
    try:
        handler = await open_remote_endpoint(ip, 60077)
    except Exception as e:
        return (
         ip, False, e)

    try:
        re = handler.send(msg.encode('utf8'))
        recevier = handler.receive()
        res = await asyncio.wait_for(recevier, timeout=10)
    except asyncio.TimeoutError as e:
        return (
         ip, False, e)

    log.info('[check ok] :' + ip + ' : ' + time.asctime())
    return (ip, True, 'good')


async def _run(loop, ips, msg='-v'):
    tasks = [check_up(ip, loop, msg=msg) for ip in ips]
    return await (asyncio.gather)(*tasks)


class Test:

    def __init__(self):
        ca = Cache(DB_PATH)
        self.ips = [h.host for h in ca.query(Host)]
        del ca

    def check_hosts(self, msg='hello'):
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
        ips = self.ips
        res = loop.run_until_complete(_run(loop, ips, msg=msg))
        loop.close()
        return res


def test(host, port, tp='udp', callback=print):
    c = Connection(host, port, tp='udp')
    c.write(b'-v')
    c.read(callback=callback)