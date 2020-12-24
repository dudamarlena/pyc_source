# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/kedro_viz/utils.py
# Compiled at: 2020-02-21 04:43:58
# Size of source mod 2**32: 3017 bytes
""" Kedro-Viz helper functions """
import logging
from time import sleep, time
from typing import Any, Callable

class WaitForException(Exception):
    __doc__ = "\n    WaitForException: if func doesn't return expected result within the\n        specified time\n\n    "


def wait_for(func: Callable, expected_result: Any=True, timeout_: int=10, print_error: bool=True, sleep_for: int=1, **kwargs) -> None:
    """
    Run specified function until it returns expected result until timeout.

    Args:
        func (Callable): Specified function
        expected_result (Any): result that is expected. Defaults to None.
        timeout_ (int): Time out in seconds. Defaults to 10.
        print_error (boolean): whether any exceptions raised should be printed.
            Defaults to False.
        sleep_for (int): Execute func every specified number of seconds.
            Defaults to 1.
        **kwargs: Arguments to be passed to func

    Raises:
         WaitForException: if func doesn't return expected result within the
         specified time

    """
    end = time() + timeout_
    while time() <= end:
        try:
            retval = func(**kwargs)
        except Exception as err:
            if print_error:
                logging.error(err)
        else:
            if retval == expected_result:
                return
            sleep(sleep_for)

    raise WaitForException("func: {}, didn't return {} within specified timeout: {}".format(func, expected_result, timeout_))