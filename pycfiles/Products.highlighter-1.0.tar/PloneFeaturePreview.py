# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/PloneFeaturePreview.py
# Compiled at: 2008-05-20 04:51:58
__doc__ = "\n                                                                           \n                      GRUF3 Feature-preview stuff.                         \n                                                                           \n This code shouldn't be here but allow people to preview advanced GRUF3    \n features (eg. flexible LDAP searching in 'sharing' tab, ...) in Plone 2,  \n without having to upgrade to Plone 2.1.\n                                                                           \n Methods here are monkey-patched by now but will be provided directly by\n Plone 2.1.\n Please forgive this 'uglyness' but some users really want to have full    \n LDAP support without switching to the latest Plone version ! ;)\n\n\n BY DEFAULT, this thing IS enabled with Plone 2.0.x\n"
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from OFS.SimpleItem import SimpleItem
from OFS.Image import Image
from Globals import InitializeClass, DTMLFile, MessageDialog
from Acquisition import aq_base
from AccessControl.User import nobody
from AccessControl import ClassSecurityInfo
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from interfaces.portal_groups import portal_groups as IGroupsTool
from global_symbols import *

def searchForMembers(self, REQUEST=None, **kw):
    """
    searchForMembers(self, REQUEST=None, **kw) => normal or fast search method.

    The following properties can be provided:
    - name
    - email
    - last_login_time
    - roles

    This is an 'AND' request.

    If name is provided, then a _fast_ search is performed with GRUF's
    searchUsersByName() method. This will improve performance.

    In any other case, a regular (possibly _slow_) search is performed.
    As it uses the listMembers() method, which is itself based on gruf.getUsers(),
    this can return partial results. This may change in the future.
    """
    md = self.portal_memberdata
    mt = self.portal_membership
    if REQUEST:
        dict = REQUEST
    else:
        dict = kw
    name = dict.get('name', None)
    email = dict.get('email', None)
    roles = dict.get('roles', None)
    last_login_time = dict.get('last_login_time', None)
    is_manager = mt.checkPermission('Manage portal', self)
    if name:
        name = name.strip().lower()
    if email:
        email = email.strip().lower()
    md_users = None
    uf_users = None
    if name:
        lst = md.searchMemberDataContents('fullname', name)
        md_users = [ x['username'] for x in lst ]
        acl_users = self.acl_users
        meth = getattr(acl_users, 'searchUsersByName', None)
        if meth:
            uf_users = meth(name)
    Log(LOG_DEBUG, md_users, uf_users)
    members = []
    if md_users is not None and uf_users is not None:
        names_checked = 1
        wrap = mt.wrapUser
        getUser = acl_users.getUser
        for userid in md_users:
            members.append(wrap(getUser(userid)))

        for userid in uf_users:
            if userid in md_users:
                continue
            usr = getUser(userid)
            if usr is not None:
                members.append(wrap(usr))

        if not email and not roles and not last_login_time:
            return members
    else:
        members = self.listMembers()
        names_checked = 0
    res = []
    portal = self.portal_url.getPortalObject()
    for member in members:
        u = member.getUser()
        if not (member.listed or is_manager):
            continue
        if name and not names_checked:
            if u.getUserName().lower().find(name) == -1 and member.getProperty('fullname').lower().find(name) == -1:
                continue
        if email:
            if member.getProperty('email').lower().find(email) == -1:
                continue
        if roles:
            user_roles = member.getRoles()
            found = 0
            for r in roles:
                if r in user_roles:
                    found = 1
                    break

            if not found:
                continue
        if last_login_time:
            if member.last_login_time < last_login_time:
                continue
        res.append(member)

    Log(LOG_DEBUG, res)
    return res


def listAllowedMembers(self):
    """listAllowedMembers => list only members which belong
    to the same groups/roles as the calling user.
    """
    user = self.REQUEST['AUTHENTICATED_USER']
    caller_roles = user.getRoles()
    current_members = self.listMembers()
    allowed_members = []
    for member in current_members:
        for role in caller_roles:
            if role in member.getRoles():
                allowed_members.append(member)
                break

    return allowed_members


def _getPortrait(self, member_id):
    """
    return member_id's portrait if you can.
    If it's not possible, just try to fetch a 'portait' property from the underlying user source,
    then create a portrait from it.
    """
    Log(LOG_DEBUG, 'trying to fetch the portrait for the given member id')
    portrait = self._former_getPortrait(member_id)
    if portrait:
        Log(LOG_DEBUG, 'Returning the old-style portrait:', portrait, 'for', member_id)
        return portrait
    member = self.portal_membership.getMemberById(member_id)
    portrait = member.getUser().getProperty('portrait', None)
    if not portrait:
        Log(LOG_DEBUG, 'No portrait available in the user source for', member_id)
        return
    Log(LOG_DEBUG, 'Converting the portrait', type(portrait))
    portrait = Image(id=member_id, file=portrait, title='')
    membertool = self.portal_memberdata
    membertool._setPortrait(portrait, member_id)
    Log(LOG_DEBUG, 'Returning the real portrait')
    return self._former_getPortrait(member_id)


def setLocalRoles(self, obj, member_ids, member_role, reindex=1):
    """ Set local roles on an item """
    member = self.getAuthenticatedMember()
    gruf = self.acl_users
    my_roles = member.getRolesInContext(obj)
    if 'Manager' in my_roles or member_role in my_roles:
        for member_id in member_ids:
            u = gruf.getUserById(member_id) or gruf.getGroupByName(member_id)
            if not u:
                continue
            member_id = u.getUserId()
            roles = list(obj.get_local_roles_for_userid(userid=member_id))
            if member_role not in roles:
                roles.append(member_role)
                obj.manage_setLocalRoles(member_id, roles)

    if reindex:
        obj.reindexObjectSecurity()


def deleteLocalRoles(self, obj, member_ids, reindex=1):
    """ Delete local roles for members member_ids """
    member = self.getAuthenticatedMember()
    my_roles = member.getRolesInContext(obj)
    gruf = self.acl_users
    member_ids = [ u.getUserId() for u in [ gruf.getUserById(u) or gruf.getGroupByName(u) for u in member_ids ] if u ]
    if 'Manager' in my_roles or 'Owner' in my_roles:
        obj.manage_delLocalRoles(userids=member_ids)
    if reindex:
        obj.reindexObjectSecurity()


if PREVIEW_PLONE21_IN_PLONE20_:
    from Products.CMFCore import MembershipTool as CMFCoreMembershipTool
    CMFCoreMembershipTool.MembershipTool.setLocalRoles = setLocalRoles
    CMFCoreMembershipTool.MembershipTool.deleteLocalRoles = deleteLocalRoles
    from Products.CMFPlone import MemberDataTool
    from Products.CMFPlone import MembershipTool
    MembershipTool.MembershipTool.searchForMembers = searchForMembers
    MembershipTool.MembershipTool.listAllowedMembers = listAllowedMembers
    MemberDataTool.MemberDataTool._former_getPortrait = MemberDataTool.MemberDataTool._getPortrait
    MemberDataTool.MemberDataTool._getPortrait = _getPortrait
    Log(LOG_NOTICE, "Applied GRUF's monkeypatch over Plone 2.0.x. Enjoy!")