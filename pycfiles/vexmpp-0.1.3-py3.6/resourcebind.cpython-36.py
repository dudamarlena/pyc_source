# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/protocols/resourcebind.py
# Compiled at: 2017-01-31 22:58:59
# Size of source mod 2**32: 797 bytes
from lxml import etree
from ..jid import Jid
from ..stanzas import Iq
from .. import getLogger
log = getLogger(__name__)
NS_URI = 'urn:ietf:params:xml:ns:xmpp-bind'

async def bind(stream, resource, timeout=None):
    iq = Iq(type='set', request=('bind', NS_URI))
    iq.setId('bind')
    if resource:
        resource_elem = etree.Element('resource')
        resource_elem.text = resource
        iq.request.append(resource_elem)
    resp = await stream.sendAndWait(iq, timeout=timeout)
    if resp.error:
        raise resp.error
    jid = resp.request.findtext('bind:jid', namespaces={'bind': NS_URI})
    if not jid:
        log.error("Resource bind result did not contain a 'jid'")
        return
    else:
        return Jid(jid)