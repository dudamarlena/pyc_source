# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aioble/dotnet/utils.py
# Compiled at: 2018-12-04 02:10:23
# Size of source mod 2**32: 385 bytes
import asyncio
from collections import Awaitable
from System import Action
from System.Threading.Tasks import Task

async def wrap_dotnet_task(task, loop):
    done = asyncio.Event()
    task.ContinueWith(Action[Task](lambda x: loop.call_soon_threadsafe(done.set)))
    await done.wait()
    if task.IsFaulted:
        raise Exception(task.Exception.ToString())
    return task.Result