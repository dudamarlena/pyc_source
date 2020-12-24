# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/generations/evolve2.py
# Compiled at: 2013-11-19 06:30:30
import logging
logger = logging.getLogger('ztfy.thesaurus')
from transaction.interfaces import ITransactionManager
from zope.component.interfaces import ISite
from zope.intid.interfaces import IIntIds
from ztfy.thesaurus.interfaces.term import IThesaurusTerm
from ztfy.thesaurus.interfaces.thesaurus import IThesaurus
from zope.app.publication.zopepublication import ZopePublication
from zope.component import getUtility, getUtilitiesFor
from zope.location import locate
from zope.site import hooks
from ztfy.utils.catalog import indexObject
from ztfy.utils.catalog.index import TextIndexNG

def evolve(context):
    """Create stemm_label index in each thesaurus"""
    root_folder = context.connection.root().get(ZopePublication.root_name, None)
    for site in root_folder.values():
        if ISite(site, None) is not None:
            hooks.setSite(site)
            intids = getUtility(IIntIds)
            for name, thesaurus in getUtilitiesFor(IThesaurus):
                catalog = thesaurus.catalog
                if 'stemm_label' not in catalog:
                    logger.info("Adding stemmed index in '%s' inner catalog..." % name)
                    index = TextIndexNG('label', IThesaurusTerm, field_callable=False, languages=thesaurus.language, splitter='txng.splitters.default', storage='txng.storages.term_frequencies', dedicated_storage=False, use_stopwords=True, use_normalizer=True, use_stemmer=True, ranking=True)
                    locate(index, catalog, 'stemm_label')
                    catalog['stemm_label'] = index
                    logger.info("Indexing terms in '%s' inner catalog..." % name)
                    for index, term in enumerate(thesaurus.terms.itervalues()):
                        indexObject(term, catalog, 'stemm_label', intids=intids)
                        if not index % 100:
                            ITransactionManager(catalog).savepoint()

    return