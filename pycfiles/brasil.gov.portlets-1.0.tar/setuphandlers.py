# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/setuphandlers.py
# Compiled at: 2018-10-18 17:35:14
from brasil.gov.portal.config import TINYMCE_JSON_FORMATS
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.utils import safe_unicode
from Products.CMFQuickInstallerTool import interfaces as BBB
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility
from zope.interface import implementer
import json

@implementer(BBB.INonInstallable)
@implementer(INonInstallable)
class NonInstallable(object):

    @staticmethod
    def getNonInstallableProducts():
        """Hide in the add-ons configlet."""
        return [
         'archetypes.querywidget',
         'brasil.gov.portal.upgrades.v10900',
         'brasil.gov.portal.upgrades.v10901',
         'brasil.gov.portal.upgrades.v10902',
         'brasil.gov.portal.upgrades.v10903',
         'brasil.gov.portal.upgrades.v10904',
         'brasil.gov.portal.upgrades.v10905',
         'brasil.gov.tiles.upgrades.v2000',
         'brasil.gov.vcge.at',
         'brasil.gov.vcge.dx',
         'brasil.gov.vcge.upgrades.v2000',
         'collective.googleanalytics',
         'collective.js.cycle2',
         'collective.js.galleria',
         'collective.js.jqueryui',
         'collective.upload',
         'collective.z3cform.datagridfield',
         'collective.z3cform.datetimewidget',
         'ftw.upgrade',
         'plone.app.blocks',
         'plone.app.collection',
         'plone.app.contenttypes',
         'plone.app.dexterity',
         'plone.app.drafts',
         'plone.app.event',
         'plone.app.event.at',
         'plone.app.intid',
         'plone.app.iterate',
         'plone.app.jquery',
         'plone.app.jquerytools',
         'plone.app.querystring',
         'plone.app.relationfield',
         'plone.app.theming',
         'plone.app.tiles',
         'plone.app.versioningbehavior',
         'plone.formwidget.autocomplete',
         'plone.formwidget.contenttree',
         'plone.formwidget.datetime',
         'plone.formwidget.querystring',
         'plone.formwidget.recurrence',
         'plone.resource',
         'plone.session',
         'plonetheme.classic',
         'Products.Doormat',
         'Products.PloneFormGen',
         'raptus.autocompletewidget']

    @staticmethod
    def getNonInstallableProfiles():
        """Hide at site creation."""
        return [
         'archetypes.querywidget:default',
         'brasil.gov.agenda.upgrades.v4100:default',
         'brasil.gov.agenda:default',
         'brasil.gov.barra.upgrades.v1002:default',
         'brasil.gov.barra.upgrades.v1010:default',
         'brasil.gov.barra:default',
         'brasil.gov.portal.upgrades.v10900:default',
         'brasil.gov.portal.upgrades.v10901:default',
         'brasil.gov.portal.upgrades.v10902:default',
         'brasil.gov.portal.upgrades.v10903:default',
         'brasil.gov.portal.upgrades.v10904:default',
         'brasil.gov.portal.upgrades.v10905:default',
         'brasil.gov.portal:default',
         'brasil.gov.portal:initcontent',
         'brasil.gov.portal:uninstall',
         'brasil.gov.tiles.upgrades.v2000:default',
         'brasil.gov.tiles:default',
         'brasil.gov.tiles:uninstall',
         'brasil.gov.vcge.at:default',
         'brasil.gov.vcge.dx:default',
         'brasil.gov.vcge.upgrades.v2000:default',
         'brasil.gov.vcge:default',
         'brasil.gov.vcge:uninstall',
         'collective.cover:default',
         'collective.js.cycle2:default',
         'collective.js.galleria:default',
         'collective.js.jqueryui:default',
         'collective.nitf:default',
         'collective.polls:default',
         'collective.testcaselayer:testing',
         'collective.upload:default',
         'collective.z3cform.datagridfield:default',
         'ftw.upgrade:default',
         'plone.app.blocks:default',
         'plone.app.caching:default',
         'plone.app.contenttypes:default',
         'plone.app.contenttypes:plone-content',
         'plone.app.dexterity:default',
         'plone.app.drafts:default',
         'plone.app.event.at:default',
         'plone.app.event:default',
         'plone.app.iterate:plone.app.iterate',
         'plone.app.jquerytools:default',
         'plone.app.openid:default',
         'plone.app.querystring:default',
         'plone.app.referenceablebehavior:default',
         'plone.app.relationfield:default',
         'plone.app.theming:default',
         'plone.app.tiles:default',
         'plone.app.versioningbehavior:default',
         'plone.formwidget.autocomplete:default',
         'plone.formwidget.autocomplete:uninstall',
         'plone.formwidget.contenttree:default',
         'plone.formwidget.contenttree:uninstall',
         'plone.formwidget.querystring:default',
         'plone.formwidget.recurrence:default',
         'plone.restapi:performance',
         'plone.session:default',
         'Products.CMFPlacefulWorkflow:base',
         'Products.Doormat:default',
         'Products.Doormat:uninstall',
         'Products.PloneFormGen:default',
         'Products.PloneKeywordManager:uninstall',
         'Products.RedirectionTool:default',
         'raptus.autocompletewidget:default',
         'raptus.autocompletewidget:uninstall',
         'sc.embedder:default',
         'sc.microsite:default',
         'sc.social.like:default']


def set_tinymce_formats():
    if getUtility(ITinyMCE).formats is None:
        json_formats = safe_unicode(json.dumps(TINYMCE_JSON_FORMATS), 'utf-8')
        getUtility(ITinyMCE).formats = json_formats
    else:
        dict_formats = json.loads(getUtility(ITinyMCE).formats)
        for key in TINYMCE_JSON_FORMATS:
            if key not in dict_formats:
                dict_formats[key] = TINYMCE_JSON_FORMATS[key]

        json_formats = safe_unicode(json.dumps(dict_formats), 'utf-8')
        getUtility(ITinyMCE).formats = json_formats
    return


def set_social_media_settings():
    """Update configuration of sc.social.like package."""
    name = 'sc.social.like.interfaces.ISocialLikeSettings.enabled_portal_types'
    value = ('Audio', 'collective.cover.content', 'collective.nitf.content', 'collective.polls.poll',
             'Document', 'Event', 'Image', 'sc.embedder')
    api.portal.set_registry_record(name, value)


def add_content_central_menu():
    """Add Content Central menu option to Folder content type."""
    view = 'centrais-de-conteudo'
    folder_fti = api.portal.get_tool('portal_types')['Folder']
    folder_fti.view_methods += (view,)
    assert view in folder_fti.view_methods


def add_results_filter_menu():
    """Add Results Filter menu option to Collection content type."""
    view = 'filtro-de-resultados'
    collection_fti = api.portal.get_tool('portal_types')['Collection']
    collection_fti.view_methods += (view,)
    assert view in collection_fti.view_methods


def update_infographic_workflow():
    """Remove workflow from Infographic content type."""
    wftool = api.portal.get_tool('portal_workflow')
    wftool.setChainForPortalTypes(['Infographic'], '')
    assert wftool.getChainForPortalType('Infographic') == ()


def run_after(context):
    set_tinymce_formats()
    set_social_media_settings()
    add_content_central_menu()
    add_results_filter_menu()
    update_infographic_workflow()