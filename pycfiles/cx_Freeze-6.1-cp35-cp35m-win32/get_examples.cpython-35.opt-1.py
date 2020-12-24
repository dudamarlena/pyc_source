# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\importlib\get_examples.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 526 bytes
from urllib.request import urlopen
examples = [
 'https://raw.githubusercontent.com/aio-libs/aiohttp/master/examples/server_simple.py',
 'https://raw.githubusercontent.com/aio-libs/aiohttp/master/examples/web_srv.py',
 'https://raw.githubusercontent.com/gevent/gevent/master/examples/wsgiserver.py']
for example in examples:
    fileName = example.split('/')[(-1)]
    with urlopen(example) as (source):
        with open(fileName, 'w+b') as (target):
            target.write(source.read())
            print('Wrote', fileName)