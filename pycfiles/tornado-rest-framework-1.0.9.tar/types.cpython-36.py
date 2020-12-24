# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/types.py
# Compiled at: 2018-10-19 23:03:13
# Size of source mod 2**32: 489 bytes
import typing
Scope = typing.MutableMapping[(str, typing.Any)]
Message = typing.MutableMapping[(str, typing.Any)]
Receive = typing.Callable[([], typing.Awaitable[Message])]
Send = typing.Callable[([Message], typing.Awaitable[None])]
ASGIInstance = typing.Callable[([Receive, Send], typing.Awaitable[None])]
ASGIApp = typing.Callable[([Scope], ASGIInstance)]
StrDict = typing.Mapping[(str, str)]
StrPairs = typing.Sequence[typing.Tuple[(str, str)]]
BytesPairs = typing.List[typing.Tuple[(bytes, bytes)]]