# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\serpscrap\find_proxies.py
# Compiled at: 2018-01-04 10:12:25
# Size of source mod 2**32: 785 bytes
import asyncio
from proxybroker import Broker

async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as (f):
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            row = '%s %s:%d\n' % (proto, proxy.host, proxy.port)
            f.write(row)


def main():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=[
     'HTTP'],
      countries=[
     'DE'],
      limit=10), save(proxies, filename='proxies.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


if __name__ == '__main__':
    main()