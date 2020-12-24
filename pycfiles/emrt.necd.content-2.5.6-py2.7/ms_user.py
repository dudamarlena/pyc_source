# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/utilities/ms_user.py
# Compiled at: 2019-02-15 13:51:23
from zope.interface import implementer
from zope.component import getUtility
import plone.api as api
from emrt.necd.content.utilities.interfaces import IUserIsMS
from emrt.necd.content.constants import ROLE_MSA
from emrt.necd.content.constants import ROLE_MSE

@implementer(IUserIsMS)
class UserIsMS(object):

    def __call__(self, context, user=None):
        user = user or api.user.get_current()
        roles = api.user.get_roles(user=user, obj=context)
        return ROLE_MSA in roles or ROLE_MSE in roles


def hide_from_ms(context):
    is_ms = getUtility(IUserIsMS)(context)
    is_manager = 'Manager' in api.user.get_roles()
    return is_manager or not is_ms