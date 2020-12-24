# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zaggregator/tests/run_asyncio.py
# Compiled at: 2018-06-07 19:27:20
# Size of source mod 2**32: 385 bytes
import asyncio, sys
delay = 1

def zag_sampler_loop(lc):
    loop, callback = lc
    loop.call_later(delay, callback, lc)
    sys.stdout.write('.')
    sys.stdout.flush()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    callback = zag_sampler_loop
    lc = (loop, callback)
    loop.call_later(delay, callback, lc)
    loop.run_forever()
    loop.close()