# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/security.py
# Compiled at: 2012-06-20 10:07:04
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.authentication.interfaces import IAuthentication
from zope.pluggableauth.interfaces import IPrincipalInfo
from zc.set import Set
from zope.component import getUtility
from zope.deprecation.deprecation import deprecate
from zope.i18n import translate
from zope.interface import implements
from zope.security.proxy import removeSecurityProxy
from ztfy.utils.request import getRequest
from ztfy.utils import _

def unproxied(value):
    """Remove security proxies from given value ; if value is a list or dict, all elements are unproxied"""
    if isinstance(value, (list, PersistentList)):
        result = []
        for v in value:
            result.append(unproxied(v))

    elif isinstance(value, (dict, PersistentDict)):
        result = value.copy()
        for v in value:
            result[v] = unproxied(value[v])

    elif isinstance(value, (set, Set)):
        result = []
        for v in value:
            result.append(unproxied(v))

    else:
        result = removeSecurityProxy(value)
    return result


@deprecate('ztfy.utils.security.MissingPrincipal is deprecated. Use ztfy.security.search.MissingPrincipal class instead.')
class MissingPrincipal(object):
    implements(IPrincipalInfo)

    def __init__(self, id):
        self.id = id
        self.request = getRequest()

    @property
    def title(self):
        return translate(_('< missing principal %s >'), context=self.request) % self.id

    @property
    def description(self):
        return translate(_("This principal can't be found in any authentication utility..."), context=self.request)


@deprecate('ztfy.utils.security.getPrincipal is deprecated. Use ztfy.security.search.getPrincipal function instead.')
def getPrincipal(uid):
    principals = getUtility(IAuthentication)
    try:
        return principals.getPrincipal(uid)
    except:
        return MissingPrincipal(uid)