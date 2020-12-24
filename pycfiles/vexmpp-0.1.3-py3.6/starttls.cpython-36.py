# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/features/starttls.py
# Compiled at: 2017-02-05 17:55:26
# Size of source mod 2**32: 823 bytes
from ..errors import XmppError
from ..stanzas import Stanza
NS_URI = 'urn:ietf:params:xml:ns:xmpp-tls'

async def handle(stream, feature_elem, timeout=None):
    nsmap = {'tls': NS_URI}
    stream.send(Stanza('starttls', nsmap={None: NS_URI}))
    resp = await stream.wait([('/tls:proceed', nsmap),
     (
      '/tls:failure', nsmap)],
      timeout=timeout)
    if resp.name == '{%s}proceed' % NS_URI:
        await stream._transport.starttls()
    else:
        raise XmppError('starttls failure: %s' % resp.toXml().decode())
    return True


def isRequired(feature_elem):
    return '{%s}required' % NS_URI in [c.tag for c in feature_elem]