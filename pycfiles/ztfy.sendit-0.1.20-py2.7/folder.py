# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/user/folder.py
# Compiled at: 2013-04-22 09:25:17
from zope.annotation.interfaces import IAnnotations
from ztfy.sendit.app.interfaces import ISenditApplication
from ztfy.sendit.user.interfaces import ISenditApplicationUsers
from zope.component import adapter
from zope.container.folder import Folder
from zope.interface import implementer, implements
from zope.location import locate
from zope.publisher.interfaces import NotFound
from zope.security.interfaces import IPrincipal
from ztfy.sendit.user import User
from ztfy.utils.request import queryRequest

class UsersFolder(Folder):
    """Users folder class"""
    implements(ISenditApplicationUsers)

    def getUserFolder(self, principal=None):
        if principal is None:
            request = queryRequest()
            if request is not None:
                principal = request.principal
        if principal is None:
            raise NotFound(self, principal)
        if IPrincipal.providedBy(principal):
            principal = principal.id
        return self.get(principal)

    def addUserFolder(self, principal=None):
        if principal is None:
            request = queryRequest()
            if request is not None:
                principal = request.principal
        if principal is None:
            raise NotFound(self, principal)
        if IPrincipal.providedBy(principal):
            principal = principal.id
        user = self.get(principal)
        if user is None:
            user = self[principal] = User()
            user.owner = principal
        return user


SENDIT_APPLICATION_USERS_KEY = 'ztfy.sendit.users'

@adapter(ISenditApplication)
@implementer(ISenditApplicationUsers)
def SenditApplicationUsersFactory(context):
    annotations = IAnnotations(context)
    container = annotations.get(SENDIT_APPLICATION_USERS_KEY)
    if container is None:
        container = annotations[SENDIT_APPLICATION_USERS_KEY] = UsersFolder()
        locate(container, context, '++users++')
    return container