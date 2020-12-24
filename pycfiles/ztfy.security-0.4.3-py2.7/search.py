# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/search.py
# Compiled at: 2013-04-15 04:26:47
__docformat__ = 'restructuredtext'
from zope.authentication.interfaces import IAuthentication, PrincipalLookupError
from zope.pluggableauth.interfaces import IPrincipalInfo
from zope.pluggableauth.plugins.groupfolder import IGroupFolder
from zope.pluggableauth.plugins.principalfolder import IInternalPrincipalContainer
from ztfy.security.interfaces import IAuthenticatorSearchAdapter
from zope.component import adapts, queryUtility
from zope.i18n import translate
from zope.interface import implements
from ztfy.utils.request import getRequest, getRequestData, setRequestData
from ztfy.security import _

class NoPrincipal(object):
    implements(IPrincipalInfo)

    def __init__(self):
        self.id = ''

    title = _('No selected principal')
    description = _('No principal was selected')


class MissingPrincipal(object):
    implements(IPrincipalInfo)

    def __init__(self, uid):
        self.id = uid
        self.request = getRequest()

    @property
    def title(self):
        return translate(_('< missing principal %s >'), context=self.request) % self.id

    @property
    def description(self):
        return translate(_("This principal can't be found in any authentication utility..."), context=self.request)


class PrincipalFolderSearchAdapter(object):
    """Principal folder search adapter"""
    adapts(IInternalPrincipalContainer)
    implements(IAuthenticatorSearchAdapter)

    def __init__(self, context):
        self.context = context

    def search(self, query):
        return self.context.search({'search': query})


class GroupFolderSearchAdapter(object):
    """Principal group search adapter"""
    adapts(IGroupFolder)
    implements(IAuthenticatorSearchAdapter)

    def __init__(self, context):
        self.context = context

    def search(self, query):
        return self.context.search({'search': query})


REQUEST_PRINCIPALS_KEY = 'ztfy.security.principals.cache'

def getPrincipal(uid, auth=None, request=None):
    """Get a principal"""
    if not uid:
        return NoPrincipal()
    else:
        if request is not None:
            cache = getRequestData(REQUEST_PRINCIPALS_KEY, request, None)
            if cache and uid in cache:
                return cache[uid]
        if auth is None:
            auth = queryUtility(IAuthentication)
        if auth is None:
            return NoPrincipal()
        try:
            result = auth.getPrincipal(uid)
        except PrincipalLookupError:
            return MissingPrincipal(uid)

        if request is not None:
            cache = cache or {}
            cache[uid] = result
            setRequestData(REQUEST_PRINCIPALS_KEY, cache, request)
        return result
        return


def findPrincipals(query, names=None):
    """Search for principals"""
    query = query.strip()
    if not query:
        return ()
    else:
        auth = queryUtility(IAuthentication)
        if auth is None:
            return ()
        if isinstance(names, (str, unicode)):
            names = names.split(',')
        result = []
        for name, plugin in auth.getQueriables():
            if not names or name in names:
                search = IAuthenticatorSearchAdapter(plugin.authplugin, None)
                if search is not None:
                    result.extend([ getPrincipal(uid, auth) for uid in search.search(query) ])

        return sorted(result, key=lambda x: x.title)