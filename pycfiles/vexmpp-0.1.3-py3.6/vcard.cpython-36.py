# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/protocols/vcard.py
# Compiled at: 2017-02-05 18:38:49
# Size of source mod 2**32: 708 bytes
from ..stanzas import Iq
NS_URI = 'vcard-temp'

async def get(stream, to, timeout=None):
    iq = await stream.sendAndWaitIq(NS_URI, to=to, child_name='vCard', raise_on_error=True,
      id_prefix='vcard_get',
      timeout=timeout)
    return iq


async def set(stream, to, vcard_xml, timeout=None):
    iq = Iq(to=to, type='set', id_prefix='vcard_set')
    iq.append(vcard_xml)
    iq = await stream.sendAndWait(iq, raise_on_error=True, timeout=timeout)
    return iq