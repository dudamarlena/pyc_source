# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/venv24/checkouts/collective.cu3er/collective/cu3er/setuphandlers.py
# Compiled at: 2010-05-22 11:25:59
from logging import getLogger
from plone.browserlayer import utils as layerutils
from collective.cu3er.interfaces import ICU3ERSpecific
log = getLogger('collective.cu3er')

def resetLayers(context):
    """Remove custom browserlayer on uninstall."""
    if context.readDataFile('collective.cu3er_uninstall.txt') is None:
        return
    if ICU3ERSpecific in layerutils.registered_layers():
        layerutils.unregister_layer(name='collective.cu3er')
        log.info('Browser layer "collective.cu3er" uninstalled.')
    return