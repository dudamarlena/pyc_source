# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/asyncbots/util.py
# Compiled at: 2018-01-10 16:38:46
# Size of source mod 2**32: 1690 bytes
"""Module with utility functions"""
import asyncio
from asyncio.futures import CancelledError
from functools import partial
import logging, re, traceback, requests
logger = logging.getLogger(__name__)

def kill_all_tasks():
    """Kill all currently running asyncio tasks."""
    for task in asyncio.Task.all_tasks():
        task.cancel()
        print('Cancelled task')


async def handle_async_exception(coro, *args, **kwargs):
    """Wrapper for coroutines which will catch an exception and kill the entire program rather than hanging."""
    try:
        return await coro(*args, **kwargs)
    except Exception as e:
        try:
            if not isinstance(e, CancelledError):
                logger.error('Exception in %s', coro)
                logger.error(traceback.format_exc())
                kill_all_tasks()
        finally:
            e = None
            del e


_request_funcs = {'GET':requests.get, 
 'POST':requests.post}

async def make_request(url, params, request_type='GET', **kwargs):
    """Coroutine which makes request asychronously rather than blocking."""
    loop = asyncio.get_event_loop()
    func = partial(_request_funcs[request_type], params=params, **kwargs)
    res = (await loop.run_in_executor(None, func, url)).json()
    if res['ok'] is not True:
        logger.warning('Slack returned bad status: %s', res)
    return res


MENTION_RE = re.compile('<@(U[0-9A-Z]{8})>$')

def mention_to_uid(mention):
    """Converts a mention (as formatted by Slack) to a UID. Returns None if the input is not a valid mention."""
    res = MENTION_RE.match(mention)
    if res is None:
        return
    return res.group(1)


def uid_to_mention(uid):
    """Convert a UID to a mention."""
    return '<@{}>'.format(uid)