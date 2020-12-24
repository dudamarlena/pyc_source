# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/serge/Documents/inf/p4.2.4/rd/src/ageliaco.rd2/ageliaco/rd2/setuphandlers.py
# Compiled at: 2013-02-28 07:49:18
import logging
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-ageliaco.rd2:default'

def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        logger = logging.getLogger('ageliaco.rd2')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')
    catalog = getToolByName(context, 'portal_catalog')
    indexes = catalog.indexes()
    wanted = (
     ('start', 'DateIndex'),
     ('end', 'DateIndex'),
     ('firstname', 'FieldIndex'),
     ('lastname', 'FieldIndex'),
     ('email', 'FieldIndex'),
     ('address', 'FieldIndex'),
     ('school', 'FieldIndex'),
     ('supervisor', 'KeywordIndex'),
     ('authors', 'KeywordIndex'),
     ('cycles', 'KeywordIndex'),
     ('sponsorasked', 'FieldIndex'),
     ('sponsorSEM', 'FieldIndex'),
     ('sponsorRD', 'FieldIndex'),
     ('sponsorSchool', 'FieldIndex'),
     ('SearchableText', 'ZCTextIndex'))
    indexables = []
    for name, meta_type in wanted:
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
    if context.readDataFile('ageliaco.rd2-default.txt') is None:
        return
    else:
        logger = context.getLogger('ageliaco.rd2')
        site = context.getSite()
        add_catalog_indexes(site, logger)
        return