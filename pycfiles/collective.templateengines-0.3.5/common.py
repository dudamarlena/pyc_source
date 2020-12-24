# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/thet-data/data/dev/htu/bda.htu.buildout/src/collective.teaser/collective/teaser/browser/common.py
# Compiled at: 2013-10-09 03:55:20
import random
from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from plone.app.portlets.portlets import base

class Assignment(base.Assignment):
    """Ignore me, I'm a portlet upgrade helper to avoid portlet breaks because
    of persistant failures."""


def _teaserlist(context, data):
    """XXX: cache on request.
    """
    context = aq_inner(context)
    cat = getToolByName(context, 'portal_catalog')
    query = {}
    query['Type'] = 'Teaser'
    query['importance'] = data.importance_levels
    if data.keywords_filter:
        query['Subject'] = data.keywords_filter
    portal = getToolByName(context, 'portal_url').getPortalObject()
    ppath = portal.getPhysicalPath()
    query['path'] = {'query': ('/').join(ppath)}
    if data.search_base:
        query['path'] = {'query': '%s%s' % (('/').join(ppath), data.search_base)}
    query['effectiveRange'] = DateTime()
    brains = cat(**query)
    teasers = []
    [ teasers.extend(int(teaser.importance) * [teaser]) for teaser in brains ]
    return teasers


def get_teasers(context, data, request):
    teasers = _teaserlist(context, data)
    if not teasers:
        return
    else:
        taken_teasers = getattr(request, 'teasers', [])
        choosen_teasers = []
        for cnt in range(data.num_teasers):
            teasers = [ _ for _ in teasers if _.id not in taken_teasers ]
            if not teasers:
                break
            choosen_teaser = random.choice(teasers)
            choosen_teasers.append(choosen_teaser.getObject())
            taken_teasers.append(choosen_teaser.id)

        request['teasers'] = taken_teasers
        show_title = data.show_title
        show_desc = data.show_description
        scale = data.teaser_scale
        teaser_list = []
        for teaser in choosen_teasers:
            img_text_part = not show_desc and teaser.Description() or ''
            img_text = '%s%s' % (teaser.title.encode('utf-8'),
             img_text_part and ' - %s' % img_text_part or '')
            img_text = img_text.decode('utf-8')
            teaser_list.append({'title': show_title and teaser.title or None, 
               'image': getattr(teaser, 'image', False) and teaser.getField('image').tag(teaser, scale=scale, alt=img_text, title=img_text) or None, 
               'description': show_desc and teaser.Description() or None, 
               'url': teaser.getLink_internal() and teaser.getLink_internal().absolute_url() or teaser.link_external or None})

        return teaser_list