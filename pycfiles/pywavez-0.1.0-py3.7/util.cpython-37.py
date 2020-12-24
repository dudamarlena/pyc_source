# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pywavez/util.py
# Compiled at: 2018-12-12 04:17:54
# Size of source mod 2**32: 982 bytes
import asyncio, inspect, logging, re

async def waitForOne(*aws, timeout=None):
    _, pending = await asyncio.wait(aws,
      timeout=timeout, return_when=(asyncio.FIRST_COMPLETED))
    for f in pending:
        f.cancel()


__rex_to_camel_case = re.compile('_.')

def toCamelCase(x):
    return __rex_to_camel_case.sub(lambda m: m.group(0)[1].upper(), x.strip('_').lower())


def callSoon(func, *args, **kwargs):

    async def makeCall():
        ret = func(*args, **kwargs)
        if inspect.isawaitable(ret):
            await ret

    asyncio.get_event_loop().call_soon(lambda : spawnTask(makeCall()))


def spawnTask(coro):
    task = asyncio.create_task(coro)
    task.add_done_callback(logException)
    return task


def logException(task):
    if not task.cancelled():
        ex = task.exception()
        if ex is not None:
            if type(ex) is not KeyboardInterrupt:
                logging.error(repr(ex))
                task.print_stack()