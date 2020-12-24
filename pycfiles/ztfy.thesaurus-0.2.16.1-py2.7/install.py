# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/generations/install.py
# Compiled at: 2013-10-07 08:56:05
import logging
logger = logging.getLogger('ztfy.thesaurus')
from transaction.interfaces import ITransactionManager
from zope.component.interfaces import ISite
from zope.intid.interfaces import IIntIds
from ztfy.thesaurus.interfaces.term import IThesaurusTerm
from ztfy.thesaurus.interfaces.thesaurus import IThesaurus
from zc.catalog.catalogindex import ValueIndex
from zope.app.publication.zopepublication import ZopePublication
from zope.component import getUtility, getUtilitiesFor
from zope.location import locate
from zope.site import hooks
from ztfy.utils.catalog import indexObject

def evolve(context):
    """Create base_label index in each thesaurus"""
    logger.info('Checking index in ZTFY.thesaurus inner catalog...')
    root_folder = context.connection.root().get(ZopePublication.root_name, None)
    for site in root_folder.values():
        if ISite(site, None) is not None:
            hooks.setSite(site)
            for _name, thesaurus in getUtilitiesFor(IThesaurus):
                catalog = thesaurus.catalog
                if 'base_label' not in catalog:
                    index = ValueIndex('base_label', IThesaurusTerm, field_callable=False)
                    locate(index, catalog, 'base_label')
                    catalog['base_label'] = index
                intids = getUtility(IIntIds)
                for index, term in enumerate(thesaurus.terms.itervalues()):
                    indexObject(term, catalog, 'base_label', intids=intids)
                    if not index % 100:
                        ITransactionManager(catalog).savepoint()

    return