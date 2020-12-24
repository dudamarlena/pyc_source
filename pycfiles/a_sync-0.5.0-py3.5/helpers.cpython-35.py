# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/a_sync/helpers.py
# Compiled at: 2016-12-23 16:13:40
# Size of source mod 2**32: 2183 bytes
"""Helper functions for the package."""
import asyncio
from concurrent import futures
from typing import Optional
EXECUTOR = None
EXECUTOR_THREAD_COUNT = 20

def get_or_create_event_loop() -> asyncio.AbstractEventLoop:
    """
    Get or create the current event loop.

    Gets the current event loop if it exists, else creates, sets as global,
    and then returns an asyncio event loop.

    Args:
        None

    Returns:
        event_loop - an asyncio event loop
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop


def get_or_create_executor() -> futures.ThreadPoolExecutor:
    """
    Get or create an executor.

    Gets the current executor if one exists, else creates, sets as global,
    and then returns a futures.ThreadPoolExecutor.

    Args:
        None

    Returns:
        executor - a futures.ThreadPoolExecutor
    """
    executor = get_executor()
    if not executor:
        executor = create_executor()
        set_executor(executor)
    return executor


def get_executor() -> Optional[futures.ThreadPoolExecutor]:
    """
    Get the executor.

    Returns the current global executor - either a futures.ThreadPoolExecutor or None, if none has been set.

    Args:
        None

    Returns:
        executor - a futures.ThreadPoolExecutor or None
    """
    global EXECUTOR
    return EXECUTOR


def set_executor(executor: futures.ThreadPoolExecutor) -> None:
    """
    Set an executor to run blocking functions in.

    Args:
        executor - a futures.ThreadPoolExecutor to set as global default.

    Returns:
        None
    """
    global EXECUTOR
    EXECUTOR = executor


def create_executor() -> futures.ThreadPoolExecutor:
    """
    Create an executor to run blocking functions in.

    Args:
        None

    Returns:
        executor - a futures.ThreadPoolExecutor.
    """
    return futures.ThreadPoolExecutor(EXECUTOR_THREAD_COUNT)