# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmonitor/demo.py
# Compiled at: 2019-10-16 08:57:11
# Size of source mod 2**32: 365 bytes
import asyncio, time

async def foo():
    await asyncio.sleep(2)
    print('done')
    return 50


async def main():
    task = asyncio.create_task(foo())
    print('看看会不会提前出现...')
    await asyncio.wait({task})


asyncio.run(main())