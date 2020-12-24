# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/collective/prettysociable/migration.py
# Compiled at: 2011-04-17 05:53:23
from zope.component import getUtility
from plone.browserlayer import utils as layerutils
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.prettysociable.interfaces import IPrettySociableSpecific
import logging
logger = logging.getLogger('prettysociable-migration')

def emptyMigrate(self):
    """For dummy upgrade steps."""
    pass


def migrateTo02(context):
    """Remove wrong kupu styles."""
    site = getUtility(IPloneSiteRoot)
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        paragraph_styles = list(kupu.getParagraphStyles())
        wrong_styles = [
         ('prettySociable Link', 'prettySociable|a')]
        to_remove = dict(wrong_styles)
        for style in paragraph_styles:
            css_class = style.split('|')[(-1)]
            if css_class in to_remove:
                paragraph_styles.remove(style)
                logger.info('Removed style "%s" from kupu config.' % style)

        kupu.configure_kupu(parastyles=paragraph_styles)
    return


def migrateTo03(context):
    """Add new custom browserlayer."""
    if IPrettySociableSpecific not in layerutils.registered_layers():
        layerutils.register_layer(IPrettySociableSpecific, name='collective.prettysociable')
        logger.info('Browser layer "collective.prettysociable" installed.')