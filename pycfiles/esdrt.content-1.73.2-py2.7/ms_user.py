# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/utilities/ms_user.py
# Compiled at: 2019-05-21 05:08:43
from zope.interface import Interface
from zope.interface import implementer
import plone.api as api

class IUserIsMS(Interface):
    """ Returns True if the user has
        the MSAuthority or MSExpert roles.
    """
    pass


@implementer(IUserIsMS)
class UserIsMS(object):

    def __call__(self, context, user=None):
        user = user or api.user.get_current()
        roles = api.user.get_roles(user=user, obj=context)
        return 'MSAuthority' in roles or 'MSExpert' in roles