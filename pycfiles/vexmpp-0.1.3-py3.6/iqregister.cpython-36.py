# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/protocols/iqregister.py
# Compiled at: 2017-01-31 22:58:59
# Size of source mod 2**32: 175 bytes
NS_URI = 'jabber:iq:register'

async def getForm(stream):
    iq = await stream.sendAndWaitIq(NS_URI, type='get', raise_on_error=True)
    return iq