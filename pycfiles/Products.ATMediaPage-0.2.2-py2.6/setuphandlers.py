# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/ATMediaPage/setuphandlers.py
# Compiled at: 2010-06-03 11:09:25
from logging import getLogger
from plone.browserlayer import utils as layerutils
from Products.ATMediaPage.interfaces import IATMediaPageSpecific
logger = getLogger('Products.ATMediaPage')

def resetLayers(context):
    """Remove custom browserlayer on uninstall."""
    if context.readDataFile('Products.ATMediaPage_uninstall.txt') is None:
        return
    else:
        if IATMediaPageSpecific in layerutils.registered_layers():
            layerutils.unregister_layer(name='Products.ATMediaPage')
            logger.info('Browser layer "Products.ATMediaPage" uninstalled.')
        return