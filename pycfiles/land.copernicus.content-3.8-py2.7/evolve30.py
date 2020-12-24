# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/upgrades/evolve30.py
# Compiled at: 2018-01-23 05:41:50
from functools import partial
import logging
from plone import api
from land.copernicus.content.content.api import LandFileApi
logger = logging.getLogger('land.copernicus.content')
MSG_CHANGED_TITLE = 'Changed title: %s -> %s. %s'
MSG_CHANGED_SHORTNAME = 'Changed ID: %s -> %s. %s'

def extract_props(landfile):
    description = landfile._md['description'].raw
    return dict(title=landfile.title, shortname=landfile.id, description=description, remoteUrl=landfile.remoteUrl, _fileSize=landfile.fileSize, fileCategories=tuple((cat['name'], cat['value']) for cat in landfile.fileCategories if cat['value']))


def _join_categories(categories):
    return (' ').join('(%s)' % val for _, val in categories)


def add_with_fallback(lfa, props):
    """ If the title exists, create a new title
        by appending the file categories.
    """
    if lfa.get(props['title']):
        props['title'] = ('{} {}').format(props['title'], _join_categories(props['fileCategories']))
    return lfa.add(**props)


def _log_prop_change(msg, old_prop, new_prop, url):
    if new_prop != old_prop:
        logger.warn(msg, old_prop, new_prop, url)


log_title_change = partial(_log_prop_change, MSG_CHANGED_TITLE)
log_shortname_change = partial(_log_prop_change, MSG_CHANGED_SHORTNAME)

def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [ b.getObject() for b in catalog(portal_type='LandItem') ]
    for landitem in landitems:
        query = dict(portal_type='LandFile', review_state='published')
        brains = landitem.getFolderContents(contentFilter=query)
        landfiles = [ b.getObject() for b in brains ]
        if landfiles:
            lfa = LandFileApi(landitem.landfiles)
            for landfile in landfiles:
                url = landfile.absolute_url(1)
                obj = landfile.aq_inner.aq_self
                props = extract_props(obj)
                new_landfile = add_with_fallback(lfa, props)
                log_title_change(obj.title, new_landfile.title, url)
                log_shortname_change(obj.id, new_landfile.shortname, url)

            len_orig = len(landfiles)
            len_added = len(landitem.landfiles)
            api.content.delete(objects=landfiles)
            logger.info('Done %s -> %s!', len_orig, len_added)