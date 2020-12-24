# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/collective/reflex/setuphandlers.py
# Compiled at: 2019-09-08 10:50:52
import logging
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces import constrains
from plone import api
from zope.interface import implementer
from zope.lifecycleevent import modified
logger = logging.getLogger(__name__)

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
         'collective.reflex:uninstall']


def post_install(context):
    """Post install script"""
    set_up_content(context)


def uninstall(context):
    """Uninstall script"""
    pass


def set_up_content(context):
    """Create and configure some initial content"""
    portal = api.portal.get()
    for item in STRUCTURE:
        _create_content(item, portal)


def _create_content(item_dict, container, force=False):
    old = container.get(item_dict['id'], None)
    if old and not force:
        children = item_dict.pop('children', [])
        for subitem in children:
            _create_content(subitem, old)

        return
    layout = item_dict.pop('layout', None)
    default_page = item_dict.pop('default_page', None)
    allowed_types = item_dict.pop('allowed_types', None)
    local_roles = item_dict.pop('local_roles', [])
    children = item_dict.pop('children', [])
    state = item_dict.pop('state', None)
    new = api.content.create(container=container, safe_id=True, **item_dict)
    logger.info(('Created {0} at {1}').format(new.portal_type, new.absolute_url()))
    if layout is not None:
        new.setLayout(layout)
    if default_page is not None:
        new.setDefaultPage(default_page)
    if allowed_types is not None:
        _constrain(new, allowed_types)
    for local_role in local_roles:
        api.group.grant_roles(groupname=local_role['group'], roles=local_role['roles'], obj=new)

    if state is not None:
        api.content.transition(new, to_state=state)
    modified(new)
    for subitem in children:
        _create_content(subitem, new)

    return


def _constrain(context, allowed_types):
    behavior = constrains.ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)


STRUCTURE = [
 {'id': 'report', 
    'type': 'Folder', 
    'title': 'Report', 
    'description': 'Report', 
    'state': 'private', 
    'layout': '@@collective-search-view', 
    'allowed_types': [
                    'Folder'], 
    'exclude_from_nav': True}]