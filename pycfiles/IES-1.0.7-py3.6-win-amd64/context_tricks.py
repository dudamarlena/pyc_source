# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\context_tricks.py
# Compiled at: 2018-01-14 22:14:26
# Size of source mod 2**32: 2165 bytes


@object.__new__
class nop_context(object):
    __doc__ = 'A nop context manager.\n    '

    def __enter__(self):
        pass

    def __exit__(self, *excinfo):
        pass


def _nop(*args, **kwargs):
    pass


class CallbackManager(object):
    __doc__ = "Create a context manager from a pre-execution callback and a\n    post-execution callback.\n\n    Parameters\n    ----------\n    pre : (...) -> any, optional\n        A pre-execution callback. This will be passed ``*args`` and\n        ``**kwargs``.\n    post : (...) -> any, optional\n        A post-execution callback. This will be passed ``*args`` and\n        ``**kwargs``.\n\n    Notes\n    -----\n    The enter value of this context manager will be the result of calling\n    ``pre(*args, **kwargs)``\n\n    Examples\n    --------\n    >>> def pre(where):\n    ...     print('entering %s block' % where)\n    >>> def post(where):\n    ...     print('exiting %s block' % where)\n    >>> manager = CallbackManager(pre, post)\n    >>> with manager('example'):\n    ...    print('inside example block')\n    entering example block\n    inside example block\n    exiting example block\n\n    These are reusable with different args:\n    >>> with manager('another'):\n    ...     print('inside another block')\n    entering another block\n    inside another block\n    exiting another block\n    "

    def __init__(self, pre=None, post=None):
        self.pre = pre if pre is not None else _nop
        self.post = post if post is not None else _nop

    def __call__(self, *args, **kwargs):
        return _ManagedCallbackContext(self.pre, self.post, args, kwargs)

    def __enter__(self):
        return self.pre()

    def __exit__(self, *excinfo):
        self.post()


class _ManagedCallbackContext(object):

    def __init__(self, pre, post, args, kwargs):
        self._pre = pre
        self._post = post
        self._args = args
        self._kwargs = kwargs

    def __enter__(self):
        return (self._pre)(*self._args, **self._kwargs)

    def __exit__(self, *excinfo):
        (self._post)(*self._args, **self._kwargs)