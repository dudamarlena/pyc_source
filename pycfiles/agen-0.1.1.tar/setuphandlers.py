# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/tracker/setuphandlers.py
# Compiled at: 2011-09-23 03:45:44
import logging
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-ageliaco.tracker:default'

def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        logger = logging.getLogger('ageliaco.tracker')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')
    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    wanted = (('deadline', 'DateIndex'), )
    indexables = []
    for (name, meta_type) in wanted:
        if name not in indexes:
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
    if context.readDataFile('ageliaco.tracker-default.txt') is None:
        return
    else:
        logger = context.getLogger('ageliaco.tracker')
        site = context.getSite()
        add_catalog_indexes(site, logger)
        return