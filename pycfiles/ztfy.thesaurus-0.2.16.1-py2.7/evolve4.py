# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/generations/evolve4.py
# Compiled at: 2013-11-19 07:06:15
import logging
logger = logging.getLogger('ztfy.thesaurus')
from transaction.interfaces import ITransactionManager
from zope.component.interfaces import ISite
from zope.intid.interfaces import IIntIds
from ztfy.thesaurus.interfaces.thesaurus import IThesaurus
from zope.app.publication.zopepublication import ZopePublication
from zope.component import getUtility, getUtilitiesFor
from zope.site import hooks
from ztfy.utils.catalog import indexObject

def evolve(context):
    """Create stemm_label index in each thesaurus"""
    root_folder = context.connection.root().get(ZopePublication.root_name, None)
    for site in root_folder.values():
        if ISite(site, None) is not None:
            hooks.setSite(site)
            intids = getUtility(IIntIds)
            for name, thesaurus in getUtilitiesFor(IThesaurus):
                logger.info("Checking index splitter in '%s' inner catalog..." % name)
                catalog = thesaurus.catalog
                for index_name in ('label', 'stemm_label'):
                    index = catalog[index_name]
                    if index._index.splitter != 'txng.splitters.default':
                        index.splitter = 'txng.splitters.default'
                        index._index.splitter = 'txng.splitters.default'
                        for count, term in enumerate(thesaurus.terms.itervalues()):
                            indexObject(term, catalog, index_name, intids=intids)
                            if not count % 100:
                                ITransactionManager(catalog).savepoint()

    return