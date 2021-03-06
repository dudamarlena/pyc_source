# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/multisitepanel/browser/msp_sitemap.py
# Compiled at: 2010-08-20 03:32:40
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_parent, aq_base
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from zope.component import getUtilitiesFor, getMultiAdapter
from plone.app.workflow.interfaces import ISharingPageRole
from plone.memoize.instance import memoize
from plone.app.workflow.browser.sharing import SharingView

class ContextmapQueryBuilder(NavtreeQueryBuilder):
    """Build a folder tree query suitable for a sitemap"""
    __module__ = __name__

    def __init__(self, context):
        NavtreeQueryBuilder.__init__(self, context)
        self.query['path'] = {'query': '/'}


class MultiSitemapView(BrowserView):
    __module__ = __name__
    title = _('Multisite sitemap')
    __call__ = ViewPageTemplateFile('templates/sitemap.pt')

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        try:
            form = self.request.form
            siteid = form.get('siteid', None)
            self.siteApp = self.context.restrictedTraverse('/').get(siteid, None)
        except:
            print 'ERROREE!!!'

        self.sharing = SharingView(self.siteApp, request)
        return

    def createSiteMap(self):
        context = aq_inner(self.context)
        queryBuilder = ContextmapQueryBuilder(context)
        query = queryBuilder()
        portal = context.restrictedTraverse('@@plone_portal_state').portal()
        strategy = SitemapNavtreeStrategy(portal)
        data = buildFolderTree(context, obj=context, query=query, strategy=strategy)
        return data['children']

    @memoize
    def msp_roles(self):
        """Get a list of roles that can be managed for the target plone site.
        
        Returns a list of dicts with keys:
        
            - id
            - title
        """
        portal_membership = getToolByName(self.siteApp, 'portal_membership')
        pairs = []
        for (name, utility) in getUtilitiesFor(ISharingPageRole):
            permission = utility.required_permission
            if permission is None or portal_membership.checkPermission(permission, self.siteApp):
                pairs.append(dict(id=name, title=utility.title))

        pairs.sort(key=lambda x: x['id'])
        return pairs

    def role_settings(self):
        """Get current settings for users and groups for which settings have been made.
        
        Returns a list of dicts with keys:
        
         - id
         - title
         - type (one of 'group' or 'user')
         - roles
         
        'roles' is a dict of settings, with keys of role ids as returned by 
        roles(), and values True if the role is explicitly set, False
        if the role is explicitly disabled and None if the role is inherited.
        """
        existing_settings = self.existing_role_settings()
        current_settings = existing_settings
        requested = self.request.form.get('entries', None)
        if requested is not None:
            knownroles = [ r['id'] for r in self.roles() ]
            settings = {}
            for entry in requested:
                roles = [ r for r in knownroles if entry.get('role_%s' % r, False) ]
                settings[(entry['id'], entry['type'])] = roles

            for entry in current_settings:
                desired_roles = settings.get((entry['id'], entry['type']), None)
                if desired_roles is None:
                    continue
                for role in entry['roles']:
                    if entry['roles'][role] in [True, False]:
                        entry['roles'][role] = role in desired_roles

        current_settings.sort(key=lambda x: x['type'] + str(x['title']))
        return current_settings

    def inherited(self, section):
        """Return True if local roles are inherited here.
        """
        context = self.siteApp.restrictedTraverse(section['path'])
        if context is None:
            context = self.context
        if getattr(aq_base(context), '__ac_local_roles_block__', None):
            return False
        return True

    def existing_role_settings(self):
        """Get current settings for users and groups that have already got
        at least one of the managed local roles.

        Returns a list of dicts as per role_settings()
        """
        context = aq_inner(self.context)
        portal_membership = getToolByName(context, 'portal_membership')
        portal_groups = getToolByName(context, 'portal_groups')
        acl_users = getToolByName(context, 'acl_users')
        info = []
        local_roles = acl_users._getLocalRolesForDisplay(context)
        acquired_roles = self._inherited_roles()
        available_roles = [ r['id'] for r in self.roles() ]
        items = {}
        for (name, roles, rtype, rid) in acquired_roles:
            items[rid] = dict(id=rid, name=name, type=rtype, sitewide=[], acquired=roles, local=[])

        for (name, roles, rtype, rid) in local_roles:
            if items.has_key(rid):
                items[rid]['local'] = roles
            else:
                items[rid] = dict(id=rid, name=name, type=rtype, sitewide=[], acquired=[], local=roles)

        if AUTH_GROUP not in items:
            items[AUTH_GROUP] = dict(id=AUTH_GROUP, name=_('Logged-in users'), type='group', sitewide=[], acquired=[], local=[])
        member = portal_membership.getAuthenticatedMember()
        if member.getId() in items:
            items[member.getId()]['disabled'] = True
        dec_users = [ (a['id'] not in STICKY, a['type'], a['name'], a) for a in items.values() ]
        dec_users.sort()
        for d in dec_users:
            item = d[(-1)]
            name = item['name']
            rid = item['id']
            global_roles = set()
            if item['type'] == 'user':
                member = acl_users.getUserById(rid)
                if member is not None:
                    name = member.getProperty('fullname') or member.getId() or name
                    global_roles = set(member.getRoles())
            elif item['type'] == 'group':
                g = portal_groups.getGroupById(rid)
                name = g.getGroupTitleOrName()
                global_roles = set(g.getRoles())
                if rid == AUTH_GROUP:
                    name = _('Logged-in users')
            info_item = dict(id=item['id'], type=item['type'], title=name, disabled=item.get('disabled', False), roles={})
            have_roles = False
            for r in available_roles:
                if r in global_roles:
                    info_item['roles'][r] = 'global'
                elif r in item['acquired']:
                    info_item['roles'][r] = 'acquired'
                    have_roles = True
                elif r in item['local']:
                    info_item['roles'][r] = True
                    have_roles = True
                else:
                    info_item['roles'][r] = False

            if have_roles or rid in STICKY:
                info.append(info_item)

        return info

    def _inherited_roles(self):
        """Returns a tuple with the acquired local roles."""
        context = aq_inner(self.context)
        if not self.inherited(context):
            return []
        portal = getToolByName(context, 'portal_url').getPortalObject()
        result = []
        cont = True
        if portal != context:
            parent = aq_parent(context)
            while cont:
                if not getattr(parent, 'acl_users', False):
                    break
                userroles = parent.acl_users._getLocalRolesForDisplay(parent)
                for (user, roles, role_type, name) in userroles:
                    found = 0
                    for (user2, roles2, type2, name2) in result:
                        if user2 == user:
                            for role in roles:
                                if role not in roles2:
                                    roles2.append(role)

                            found = 1
                            break

                    if found == 0:
                        result.append([user, list(roles), role_type, name])

                if parent == portal:
                    cont = False
                elif not self.inherited(parent):
                    cont = False
                else:
                    parent = aq_parent(parent)

        for pos in range(len(result) - 1, -1, -1):
            result[pos][1] = tuple(result[pos][1])
            result[pos] = tuple(result[pos])

        return tuple(result)