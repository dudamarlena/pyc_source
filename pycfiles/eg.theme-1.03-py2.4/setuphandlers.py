# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eg/theme/setuphandlers.py
# Compiled at: 2010-11-25 09:07:53
import logging
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-eg.theme:default'

def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        logger = logging.getLogger('eg.theme')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')
    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    wanted = (
     ('timefrom', 'FieldIndex'), ('timeuntil', 'FieldIndex'), ('topic', 'ZCTextIndex'), ('area', 'ZCTextIndex'), ('mediacontent', 'ZCTextIndex'))
    indexables = []
    for (name, meta_type) in wanted:
        if name not in indexes:
            if meta_type == 'ZCTextIndex':

                class Empty:
                    __module__ = __name__

                title_extras = Empty()
                title_extras.index_type = 'Okapi BM25 Rank'
                title_extras.lexicon_id = 'plone_lexicon'
                catalog.addIndex(name, meta_type, title_extras)
            else:
                catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info('Added %s for field %s.', meta_type, name)

    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.', (', ').join(indexables))
        catalog.manage_reindexIndex(ids=indexables)
    return


def import_various(context):
    """Import step for configuration that is not handled in xml files.
    """
    if context.readDataFile('eg_theme-default.txt') is None:
        return
    logger = context.getLogger('eg.theme')
    site = context.getSite()
    add_catalog_indexes(site, logger)
    return