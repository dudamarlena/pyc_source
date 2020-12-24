# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sldap3\operation\unbind.py
# Compiled at: 2015-04-22 17:42:46
"""
"""
import logging
from .. import NATIVE_ASYNCIO
if NATIVE_ASYNCIO:
    import asyncio
else:
    import trollius as asyncio
    from trollius import From, Return

@asyncio.coroutine
def do_unbind_operation(dua, message_id):
    logging.debug('do UNBIND operation for DUA %s', dua.identity)
    dua.user = None
    return