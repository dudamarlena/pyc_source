# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/upgrades/to02.py
# Compiled at: 2013-10-15 10:29:21
from Products.CMFCore.utils import getToolByName
from plone.dexterity.interfaces import IDexterityContent
from plone.uuid.handlers import addAttributeUUID
from plone.uuid.interfaces import IUUID
from zope.component import getUtility, queryUtility
from zope.component import getAllUtilitiesRegisteredFor
from zope.intid.interfaces import IIntIds
from plone.multilingual.canonical import Canonical
from plone.multilingual.interfaces import IMultilingualStorage
from Products.Five.browser import BrowserView
import logging

def upgrade(context):
    logger = logging.getLogger('plone.multilingual')
    logger.info('Adding missing UUIDs to the already existing dexterity content types')
    catalog = getToolByName(context, 'portal_catalog')
    query = {'object_provides': IDexterityContent.__identifier__}
    results = catalog.unrestrictedSearchResults(query)
    for b in results:
        ob = b.getObject()
        if IUUID(ob, None) is None:
            addAttributeUUID(ob, None)
            ob.reindexObject(idxs=['UID'])

    logger.info('Added %s missing UUIDs' % len(results))
    intids = queryUtility(IIntIds)
    if not intids:
        intids = getAllUtilitiesRegisteredFor(IIntIds)[0]
    oldstorage = getToolByName(context, 'canonical_storage')
    for canonicalintid in oldstorage.canonicals:
        canonicaluuid = IUUID(intids.getObject(canonicalintid))
        translations = oldstorage.canonicals[canonicalintid].languages
        upgradedcanonical = Canonical()
        for lang in translations.keys():
            langintid = translations[lang]
            langobj = intids.getObject(langintid)
            languuid = IUUID(langobj)
            upgradedcanonical.add_item(lang, languuid)

        storage = getUtility(IMultilingualStorage)
        storage.add_canonical(canonicaluuid, upgradedcanonical)
        logger.info('%s' % upgradedcanonical.languages)

    return


class upgradeView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        upgrade(self.context)
        return 'plone.multilingual utility upgraded successfully'