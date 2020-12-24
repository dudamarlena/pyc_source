# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/ldap/service.py
# Compiled at: 2007-12-02 16:26:58
"""
This service manages ldap objects using schemas
"""
from salamoia.nacl.backend import BackendService, BackendMixin
from salamoia.h2o.logioni import Ione
from salamoia.h2o.exception import ConnectionError, FetchError
from connection import Connection
from salamoia.h2o.searchparser import SearchParser
from salamoia.nacl.ldap.search import ILdapSearch, TypeSpec
from salamoia.nacl.ldap.schema import LDAPSchema
from salamoia.h2o.schema import ISchema
from salamoia.nacl.ldap.fetchpattern import LDAPFetchPatternService
from salamoia.nacl.auth import IAuthentication, AuthToken
from salamoia.h2o.auth import Principal, IAuthenticatedPrincipal
from salamoia.h2o.config import Config
from salamoia.h2o.protocols import multiAdapt, contextualAdapt, adapt
import ldap
__all__ = [
 'Service']

class LDAPBackendService(BackendService):
    __module__ = __name__

    def __init__(self):
        super(LDAPBackendService, self).__init__()
        self.searchparser = SearchParser()

    def schemaClass(self):
        return LDAPSchema

    def checkCredentials(self, principal, uri=None):
        """
        Check the credentials trying to connect to the ldap directory
        binding as the user.    
        """
        if Config.defaultConfig().getboolean('security', 'disableAuthentication', 'no'):
            Ione.warning('Authentication disabled in config file!')
            return True
        Connection.defaultConnection()
        schema = ISchema(self)
        schema.service = self
        ldapUser = multiAdapt((self, principal), IAuthentication).id
        if not adapt(principal, IAuthenticatedPrincipal, False):
            Ione.warning('Checking credentials ... takes time')
            Ione.log('ldap user:', ldapUser, msgid='ldapuser')
            try:
                conn = Connection(ldapUser, principal.password)
            except ConnectionError:
                Ione.log('ConnectionError, checkCredentials failed for user: %s, host %s', ldapUser, Connection.host)
                return False

        try:
            groups = self.search("type = group and member='%s'" % ldapUser)
            principal.groups.extend(groups)
        except:
            Ione.error('cannot retreive groups')

        self.authTokens.add(AuthToken(principal, ldapUser))
        return True

    def baseFetch(self, id):
        """
        Returns an object matching the given id.

        This kind of search is fast and it does not involve
        search specification objects. It simply searchs for every object
        based at 'id' with scope SCOPE_BASE, thus returning only the
        base DN 'id'.

        After that an object is created from the returning tuples,
        using it's objectclasses to match for a python class,
        and the object's method 'fill' to actually initialize it
        with the data returned from the search.
        """
        c = Connection.defaultConnection()
        res = c.search('objectclass=*', base=id, scope=ldap.SCOPE_BASE)
        if not res:
            raise FetchError, 'Cannot find object'
        type = TypeSpec.fromObjectClass(res[0][1]['objectClass'], self)
        if not type:
            raise FetchError, 'Cannot map object (%s:%s)' % (res[0][0], res[0][1]['objectClass'])
        typeClass = type.toClass()
        u = typeClass(service=self)
        u.fill(res[0])
        u.type = type
        return u

    def search(self, searchSpec):
        """
        Returns a list of object id matching a filter constructed
        from the searchSpec.

        The OwnerSpec specification is used to set the base of the search,
        if it is found inside the spec.
        Otherwise it does a full search.

        TODO: the search could omit all unused attributes from the search...
        """
        if isinstance(searchSpec, basestring):
            searchSpec = self._parsesearch(searchSpec)
        searchSpec = contextualAdapt(searchSpec, ILdapSearch, ISchema(self))
        searchSpec.setServiceContext(self)
        Ione.log('Searching:', searchSpec.filter(), searchSpec.base(), searchSpec.scope())
        c = Connection.defaultConnection()
        try:
            res = c.search(searchSpec.filter(), attributes=['objectclass'], base=searchSpec.base(), scope=searchSpec.scope())
        except ldap.NO_SUCH_OBJECT:
            Ione.log('No such object in %s, %s ', c.host, c.suffix)
            raise

        searchResult = [ x[0] for x in res ]
        if searchSpec.needTrimming():
            objects = self.fetch(searchResult)
            trimmed = searchSpec.trim(objects)
            return [ x.id for x in trimmed ]
        return searchResult

    def _parsesearch(self, expr):
        Ione.log('parsing:', expr)
        return self.searchparser(expr)

    def backendInfo(self, *actions):

        def info(action):
            if action == 'username':
                return self._currentPrincipal.username
            if action == 'userid':
                return self.authTokens.byName(self._currentPrincipal.username).id
            elif action == 'suffix':
                return Config.defaultConfig().get('ldap', 'suffix')
            elif action == 'serviceName':
                return self.serviceName
            elif action == 'authMethod':
                return self._currentPrincipal.authInfo['authMethod']
            elif action == 'groups':
                return self.authTokens.byName(self._currentPrincipal.username).principal.groups
            elif action == 'listActions':
                return [
                 'username', 'userid', 'suffix', 'serviceName', 'authMethod', 'groups', 'listActions']

        res = [ info(a) for a in actions ]
        if len(res) == 1:
            return res[0]
        return res

    def test(self, arg, arg2=None):
        Ione.log('called, arg: %s arg2: (%s)', arg, arg2)

        class Test(object):
            __module__ = __name__

        t = Test()
        t.x = [10, None, arg]
        return


class LDAPBackendModularService(LDAPFetchPatternService, BackendMixin, LDAPBackendService):
    __module__ = __name__


Service = LDAPBackendModularService
from salamoia.tests import *
runDocTests()