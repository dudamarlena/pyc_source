# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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