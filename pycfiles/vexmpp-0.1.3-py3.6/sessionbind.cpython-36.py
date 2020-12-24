# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/protocols/sessionbind.py
# Compiled at: 2017-01-31 22:58:59
# Size of source mod 2**32: 343 bytes
from ..stanzas import Iq
NS_URI = 'urn:ietf:params:xml:ns:xmpp-session'

async def newsession(stream, timeout=None):
    iq = Iq(type='set', request=('session', NS_URI))
    iq.setId('sess')
    resp = await stream.sendAndWait(iq, timeout=timeout)
    if resp.error:
        raise NotImplementedError