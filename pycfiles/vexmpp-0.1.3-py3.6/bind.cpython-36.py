# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/features/bind.py
# Compiled at: 2017-01-31 22:58:59
# Size of source mod 2**32: 782 bytes
from ..protocols import resourcebind, sessionbind

async def handle(stream, feature_elem, timeout=None):
    jid = await resourcebind.bind(stream, (stream.creds.jid.resource), timeout=timeout)
    if jid.resource != stream.creds.jid.resource:
        stream.creds.jid = jid
    if feature_elem.getparent().xpath('child::sess:session', namespaces={'sess': sessionbind.NS_URI}):
        await sessionbind.newsession(stream, timeout=timeout)