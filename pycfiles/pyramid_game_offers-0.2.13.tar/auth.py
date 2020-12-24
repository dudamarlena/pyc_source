# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/auth.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'Auth related methods and classes.'
from pyramid.security import Allow, Everyone, ALL_PERMISSIONS

def groupfinder(userid, request):
    """
    Read all user's groups.

    .. note::

        Adds **s:inactive** group to users who has not activated their account, and **s:user** group to those, who did.
        If user has is_admin flag, he gets **s:superadmin** group set

        Might be useful, when you want restrict access to some parts of your application, but still allow log in, and
        access to some other parts.

    :param int userid: user identity
    :param pyramid.request.Request request: request object
    :returns: list of groups
    :rtype: list
    """
    user = request.user
    groups = []
    if user and user.id == userid:
        groups = [ group.name for group in user.groups ]
        if user.is_admin:
            groups.append('s:superadmin')
        if user.is_active:
            groups.append('s:user')
        else:
            groups.append('s:inactive')
        return groups
    return


class BaseACLRootFactoryMixin(object):
    """
    ACL list factory Mixin.

    __acl__ is the attribute which stores the list.

    :return: tuple (Allow|Deny, Group name, Permission)
    :rtype: list

    .. note::

        Can be converted later to database stored (sqlalchemy session is accessible through request.db)
    """
    __acl__ = [
     (
      Allow, Everyone, 'view'),
     (
      Allow, 's:superadmin', ALL_PERMISSIONS),
     (
      Allow, 's:user', ('password_change', 'email_change'))]

    def __init__(self, request):
        """Assing request as instance attribute."""
        self.request = request