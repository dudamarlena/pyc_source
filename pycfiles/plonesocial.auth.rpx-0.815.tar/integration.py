# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.activitystream/plonesocial/activitystream/integration.py
# Compiled at: 2013-07-08 09:20:06
from zope.component import queryUtility
try:
    from plonesocial.microblog.interfaces import IMicroblogTool
    from plonesocial.microblog.utils import get_microblog_context
    HAVE_PLONESOCIAL_MICROBLOG = True
except ImportError:
    HAVE_PLONESOCIAL_MICROBLOG = False

try:
    from plonesocial.network.interfaces import INetworkTool
    HAVE_PLONESOCIAL_NETWORK = True
except ImportError:
    HAVE_PLONESOCIAL_NETWORK = False

class PlonesocialIntegration(object):
    """Provide runtime utility lookup that does not throw
    ImportErrors if some components are not installed."""

    @property
    def microblog(self):
        if HAVE_PLONESOCIAL_MICROBLOG:
            return queryUtility(IMicroblogTool)
        else:
            return
            return

    @property
    def network(self):
        if HAVE_PLONESOCIAL_NETWORK:
            return queryUtility(INetworkTool)
        else:
            return
            return

    def context(self, context):
        if HAVE_PLONESOCIAL_MICROBLOG:
            return get_microblog_context(context)
        else:
            return
            return


PLONESOCIAL = PlonesocialIntegration()