# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/setuphandlers.py
# Compiled at: 2019-02-15 13:51:23
import logging
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import SORT_METHOD_FOLDER_ORDER
from emrt.necd.content.constants import LDAP_SECTOREXP
from emrt.necd.content.constants import LDAP_SECRETARIAT
from emrt.necd.content.constants import LDAP_LEADREVIEW
from emrt.necd.content.constants import ROLE_SE
from emrt.necd.content.constants import ROLE_LR
LOGGER = logging.getLogger('emrt.necd.content.setuphandlers')
VOCABULARIES = [
 {'id': 'eea_member_states', 'title': 'EEA Member States', 
    'filename': 'eea_member_states.csv'},
 {'id': 'ghg_source_category', 'title': 'NFR category group', 
    'filename': 'ghg_source_category.csv'},
 {'id': 'ghg_source_sectors', 'title': 'NFR Sector', 
    'filename': 'ghg_source_sectors.csv'},
 {'id': 'fuel', 'title': 'Fuel', 
    'filename': 'fuel.csv'},
 {'id': 'pollutants', 'title': 'Pollutants', 
    'filename': 'pollutants.csv'},
 {'id': 'scenario_type', 'title': 'Scenario Type', 
    'filename': 'scenario_type.csv'},
 {'id': 'highlight', 'title': 'Highligt', 
    'filename': 'highlight.csv'},
 {'id': 'highlight_projection', 'title': 'Highlight Projection', 
    'filename': 'highlight_projection.csv'},
 {'id': 'parameter', 'title': 'Parameter', 
    'filename': 'parameter.csv'},
 {'id': 'conclusion_reasons', 'title': 'Conclusion Reasons', 
    'filename': 'conclusion_reasons.csv'}]
LDAP_ROLE_MAPPING = {LDAP_SECTOREXP: ROLE_SE, 
   LDAP_LEADREVIEW: ROLE_LR, 
   LDAP_SECRETARIAT: 'Manager'}
LDAP_PLUGIN_ID = 'ldap-plugin'
MEMCACHED_ID = 'memcached'

def create_vocabulary(context, vocabname, vocabtitle, importfilename=None, profile=None):
    _ = context.invokeFactory(id=vocabname, title=vocabtitle, type_name='SimpleVocabulary')
    vocabulary = context.getVocabularyByName(vocabname)
    vocabulary.setSortMethod(SORT_METHOD_FOLDER_ORDER)
    wtool = getToolByName(context, 'portal_workflow')
    wtool.doActionFor(vocabulary, 'publish')
    from logging import getLogger
    log = getLogger('create_vocabulary')
    log.info('Created %s vocabulary' % vocabname)
    if importfilename is not None:
        data = profile.readDataFile(importfilename, subdir='necdvocabularies')
        vocabulary.importCSV(data)
    for term in vocabulary.values():
        wtool.doActionFor(term, 'publish')

    log.info('done')
    return


def prepareVocabularies(context, profile):
    """ initial population of vocabularies """
    atvm = getToolByName(context, 'portal_vocabularies')
    for vocabulary in VOCABULARIES:
        vocab = atvm.getVocabularyByName(vocabulary.get('id'))
        if vocab is None:
            create_vocabulary(atvm, vocabulary.get('id'), vocabulary.get('title'), vocabulary.get('filename', None), profile)

    return


def enable_atd_spellchecker(portal):
    tinymce = getToolByName(portal, 'portal_tinymce')
    tinymce.libraries_spellchecker_choice = 'AtD'
    tinymce.libraries_atd_service_url = 'service.afterthedeadline.com'


def setup_memcached(portal, memcached_id):
    if memcached_id not in portal.keys():
        try:
            _ = portal.manage_addProduct['MemcachedManager'].manage_addMemcachedManager(memcached_id)
        except Exception as err:
            LOGGER.exception(err)
        else:
            cache = portal[memcached_id]
            cache._settings['servers'] = ('127.0.0.1:11211', )
            cache._p_changed = True


def get_portal_acl(portal):
    return portal['acl_users']


def get_ldap_plugin(acl, ldap_id):
    return acl[ldap_id]


def map_ldap_roles(context):
    """Map LDAP roles to Plone roles"""
    if context.readDataFile('emrt.necd.content_various.txt') is None:
        return
    else:
        portal_acl = get_portal_acl(getSite())
        ldap_plugin = get_ldap_plugin(portal_acl, LDAP_PLUGIN_ID)
        ldap_acl = ldap_plugin._getLDAPUserFolder()
        for ldap_group, plone_role in LDAP_ROLE_MAPPING.items():
            ldap_acl.manage_addGroupMapping(ldap_group, plone_role)

        return


def setup_ldap(portal, ldap_id, memcached_id):
    acl = get_portal_acl(portal)
    ldap_plugin = get_ldap_plugin(acl, ldap_id)
    ldap_acl = ldap_plugin._getLDAPUserFolder()
    for ldap_group, plone_role in LDAP_ROLE_MAPPING.items():
        ldap_acl.manage_addGroupMapping(ldap_group, plone_role)

    ldap_plugin.ZCacheable_setManagerId(manager_id=memcached_id)
    enabled_interfaces = ('IUserEnumerationPlugin', 'IGroupsPlugin', 'IGroupEnumerationPlugin',
                          'IRoleEnumerationPlugin', 'IAuthenticationPlugin', 'IPropertiesPlugin',
                          'IRolesPlugin', 'IGroupIntrospection')
    ldap_plugin.manage_activateInterfaces(enabled_interfaces)
    plugins = acl['plugins']
    active_plugins = plugins.getAllPlugins('IPropertiesPlugin')['active']
    interface = plugins._getInterfaceFromName('IPropertiesPlugin')
    for _ in range(len(active_plugins) - 1):
        plugins.movePluginsUp(interface, [ldap_id])


def post_install(context):
    portal = getSite()
    setup_memcached(portal, MEMCACHED_ID)
    setup_ldap(portal, LDAP_PLUGIN_ID, MEMCACHED_ID)


def setupVarious(context):
    """ various import steps for emrt.necd.content """
    if context.readDataFile('emrt.necd.content_various.txt') is None:
        return
    else:
        portal = context.getSite()
        prepareVocabularies(portal, context)
        enable_atd_spellchecker(portal)
        return


def reimport_vocabularies(context):
    if context.readDataFile('emrt.necd.content_various.txt') is None:
        return
    else:
        portal = context.getSite()
        prepareVocabularies(portal, context)
        return


def update_workflow_rolemap(context):
    if context.readDataFile('emrt.necd.content_various.txt') is None:
        return
    else:
        site = context.getSite()
        portal_workflow = getToolByName(site, 'portal_workflow')
        portal_workflow.updateRoleMappings()
        return