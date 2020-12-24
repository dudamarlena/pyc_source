# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/protocols/stream_mgmt.py
# Compiled at: 2017-01-31 22:58:59
# Size of source mod 2**32: 1059 bytes
from ..stream import Mixin
from ..utils import xpathFilter
from .. import getLogger
log = getLogger(__name__)
NS_URI = 'urn:xmpp:sm:3'

class Opts:
    resume = False
    sm_id = None
    resume_location = None
    max_resume_time = None


class Mixin(Mixin):
    __doc__ = 'XXX: this is a very rudimentary XEP-0198 Mixin. Currently all it does\n    is count stanza in and out.'

    def __init__(self, opts=None):
        self._opts = opts or Opts()
        self._in_count = 0
        self._out_count = 0
        super().__init__([('stream_mgmt_opts', self._opts)])

    @xpathFilter(['/iq', '/presence', '/message',
     (
      '/ns:a', {'ns': NS_URI}), ('/ns:r', {'ns': NS_URI})])
    async def onStanza(self, stream, stanza):
        self._in_count += 1
        log.debug('Stanza IN count: {:d}'.format(self._in_count))

    @xpathFilter(['/iq', '/presence', '/message'])
    def onSend(self, stream, stanza):
        self._out_count += 1
        log.debug('Stanza OUT count: {:d}'.format(self._out_count))