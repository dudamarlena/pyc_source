# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/lbn/zenoss/__init__.py
# Compiled at: 2013-02-02 11:32:20
import logging
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from packutils import zentinel
logger = logging.getLogger('lbn.zenoss')

class ZenPack(ZenPackBase):
    """ Zenoss eggy thing - placeholder to shim if ever required """
    pass


def initialize(context):
    """
    function to hack zope instance upon startup
    """
    zport = zentinel(context)
    if zport:
        mgr = zport.dmd.ZenPackManager
        broken = filter(lambda x: not hasattr(x, 'isBroken') or x.isBroken(), mgr.packs())
        if broken:
            ids = map(lambda x: mgr.getBrokenPackName(x), broken)
            logger.info('removing: %s' % (', ').join(ids))
            for id in ids:
                try:
                    mgr.packs._delObject(id)
                except Exception, e:
                    log.error(str(e), exc_info=True)


import monkeypatches