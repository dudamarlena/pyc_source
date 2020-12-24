# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/protocols/iqversion.py
# Compiled at: 2017-02-05 20:13:13
# Size of source mod 2**32: 1522 bytes
import platform
from lxml import etree
from ..__about__ import __project_name__, __version__
from ..stream import Mixin
from ..utils import xpathFilter
from .. import getLogger
log = getLogger(__name__)
NS_URI = 'jabber:iq:version'
GET_XPATH = ("/iq[@type='get']/ns:query", {'ns': NS_URI})

async def get(stream, to, timeout=None):
    iq = await stream.sendAndWaitIq(NS_URI, to=to, raise_on_error=True, id_prefix='version_get',
      timeout=timeout)
    return iq


class IqVersionMixin(Mixin):
    __doc__ = "A stream mixin for handling version IQ 'get' requests."

    def __init__(self, name=__project_name__, version=__version__, show_platform=True):
        super().__init__()
        self._name = str(name)
        self._version = str(version)
        self._show_platform = show_platform

    @xpathFilter(GET_XPATH)
    async def onStanza(self, stream, stanza):
        log.debug('jabber:iq:version received')
        result = stanza.resultResponse()
        elem = etree.Element('name')
        elem.text = self._name
        result.query.append(elem)
        elem = etree.Element('version')
        elem.text = self._version
        result.query.append(elem)
        if self._show_platform:
            elem = etree.Element('os')
            elem.text = '%s, %s, %s' % (platform.system(), platform.release(),
             platform.version())
            result.query.append(elem)
        stream.send(result)