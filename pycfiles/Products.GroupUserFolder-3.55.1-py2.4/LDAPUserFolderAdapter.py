# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/LDAPUserFolderAdapter.py
# Compiled at: 2008-05-20 04:51:58
"""

"""
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from global_symbols import *
from Products.GroupUserFolder import postonly
MANDATORY_ATTRIBUTES = ('sn', 'cn')

def _doAddUser(self, name, password, roles, domains, **kw):
    """
    Special user adding method for use with LDAPUserFolder.
    This will ensure parameters are correct for LDAP management
    """
    kwargs = {}
    attrs = {}
    if hasattr(self, 'gruf_ldap_required_fields'):
        attrs = self.gruf_ldap_required_fields(login=name)
    for attr in MANDATORY_ATTRIBUTES:
        attrs[attr] = name

    kwargs.update(attrs)
    rdn_attr = self._rdnattr
    kwargs[rdn_attr] = name
    kwargs['user_pw'] = password
    kwargs['confirm_pw'] = password
    kwargs['user_roles'] = self._mangleRoles(name, roles)
    msg = self.manage_addUser(kwargs=kwargs)
    if msg:
        raise RuntimeError, msg


def _doDelUsers(self, names):
    """
    Remove a bunch of users from LDAP.
    We have to call manage_deleteUsers but, before, we need to find their dn.
    """
    dns = []
    for name in names:
        dns.append(self._find_user_dn(name))

    self.manage_deleteUsers(dns)


def _find_user_dn(self, name):
    """
    Convert a name to an LDAP dn
    """
    login_attr = self._login_attr
    v = self.findUser(search_param=login_attr, search_term=name)
    v = filter(lambda x: x[login_attr] == name, v)
    l = len(v)
    if not l:
        raise "Invalid user name: '%s'" % (name,)
    elif l > 1:
        raise "Duplicate user name for '%s'" % (name,)
    return v[0]['dn']


def _mangleRoles(self, name, roles):
    """
    Return role_dns for this user
    """
    if self._local_groups:
        return roles
    role_dns = []
    all_groups = self.getGroups()
    all_roles = self.valid_roles()
    groups = {}
    for g in all_groups:
        groups[g[0]] = g[1]

    for role in roles:
        if role not in all_roles:
            continue
        if role.startswith(GROUP_PREFIX):
            role = role[GROUP_PREFIX_LEN:]
            if role in all_roles:
                continue
        r = groups.get(role, None)
        if not r:
            Log(LOG_WARNING, "LDAP Server doesn't provide a '%s' group (required for user '%s')." % (role, name))
        else:
            role_dns.append(r)

    return role_dns


def _doChangeUser(self, name, password, roles, domains, **kw):
    """
    Update a user
    """
    dn = self._find_user_dn(name)
    if password is not None:
        if password == '':
            raise ValueError, 'Password must not be empty for LDAP users.'
        self.manage_editUserPassword(dn, password)
    self.manage_editUserRoles(dn, self._mangleRoles(name, roles))
    return


def manage_editGroupRoles(self, user_dn, role_dns=[], REQUEST=None):
    """ Edit the roles (groups) of a group """
    from Products.LDAPUserFolder.utils import GROUP_MEMBER_MAP
    try:
        from Products.LDAPUserFolder.LDAPDelegate import ADD, DELETE
    except ImportError:
        ADD = self._delegate.ADD
        DELETE = self._delegate.DELETE

    msg = ''
    all_groups = self.getGroups(attr='dn')
    cur_groups = self.getGroups(dn=user_dn, attr='dn')
    group_dns = []
    for group in role_dns:
        if group.find('=') == -1:
            group_dns.append('cn=%s,%s' % (group, self.groups_base))
        else:
            group_dns.append(group)

    if self._local_groups:
        if len(role_dns) == 0:
            del self._groups_store[user_dn]
        else:
            self._groups_store[user_dn] = role_dns
    for group in all_groups:
        member_attr = GROUP_MEMBER_MAP.get(self.getGroupType(group))
        if group in cur_groups and group not in group_dns:
            action = DELETE
        elif group in group_dns and group not in cur_groups:
            action = ADD
        else:
            action = None
        if action is not None:
            msg = self._delegate.modify(group, action, {member_attr: [user_dn]})

    if msg:
        raise RuntimeError, msg
    return


manage_editGroupRoles = postonly(manage_editGroupRoles)