# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/ldapauthenticator.py
# Compiled at: 2012-10-12 07:02:39
from authenticator import Authenticator
from exception import CoilsException, AuthenticationException
from coils.foundation import Session, Contact, ServerDefaultsManager
try:
    import ldap, ldap.sasl
except:

    class LDAPAuthenticator(Authenticator):

        def __init__(self, context, metadata, options):
            raise Exception('LDAP support not available')


else:
    import ldaphelper

    class LDAPAuthenticator(Authenticator):
        _dsa = None
        _ldap_debug = None

        def __init__(self, context, metadata, options):
            self._verify_options(options)
            Authenticator.__init__(self, context, metadata, options)

        @property
        def ldap_debug_enabled(self):
            if LDAPAuthenticator._ldap_debug is None:
                if ServerDefaultsManager().bool_for_default('LDAPDebugEnabled'):
                    LDAPAuthenticator._ldap_debug = True
                else:
                    LDAPAuthenticator._ldap_debug = False
            return LDAPAuthenticator._ldap_debug

        def _verify_options(self, options):
            pass

        def _bind_and_search(self, options, login):
            dsa = ldap.initialize(options['url'])
            if options['start_tls'] == 'YES':
                if self.ldap_debug_enabled:
                    self.log.debug('Starting TLS')
                dsa.start_tls_s()
            if options['binding'] == 'SIMPLE':
                dsa.simple_bind_s(options['bind_identity'], options['bind_secret'])
                if self.ldap_debug_enabled:
                    self.log.debug('Starting TLS')
            elif options['binding'] == 'DIGEST':
                tokens = ldap.sasl.digest_md5(options['bind_identity'], options['bind_secret'])
                dsa.sasl_interactive_bind_s('', tokens)
                self._search_bind()
            search_filter = options['search_filter']
            if search_filter is None:
                search_filter = ('({0}=%s)').format(options['uid_attribute']) % login
                if self.ldap_debug_enabled:
                    self.log.error(('No LDAP filter configured, defaulting to "{0}"').format(search_filter))
            else:
                search_filter = search_filter % login
            if self.ldap_debug_enabled:
                self.log.debug(('LDAP Container: {0}').format(options['search_container']))
                self.log.debug(('LDAP Filter: {0}').format(search_filter))
                self.log.debug(('LDAP UID Attribute: {0}').format(options['uid_attribute']))
            result = dsa.search_s(options['search_container'], ldap.SCOPE_SUBTREE, search_filter, [
             options['uid_attribute']])
            result = ldaphelper.get_search_results(result)
            if self.ldap_debug_enabled:
                self.log.debug(('Found {0} results.').format(len(result)))
            return result

        def _test_simple_bind(self, options, dn, secret):
            dsa = ldap.initialize(options['url'])
            if options['start_tls'] == 'YES':
                LDAPAuthenticator._dsa.start_tls_s()
            result = False
            try:
                dsa.simple_bind_s(dn, secret)
                result = True
                dsa.unbind()
            except Exception, e:
                self.log.exception(e)

            return result

        def _get_ldap_object(self):
            if self.options['binding'] == 'SIMPLE':
                accounts = self._bind_and_search(self.options, self.login)
                if len(accounts) == 0:
                    raise AuthenticationException('Matching account not returned by DSA')
                elif len(accounts) > 1:
                    raise AuthenticationException('Dupllicate accounts returned by DSA')
                else:
                    dn = accounts[0].get_dn()
                    if self.ldap_debug_enabled:
                        self.log.debug(('Testing authentication bind as {0}').format(dn))
                    if dn is None:
                        self.log.warn('LDAP object with null DN!')
                if self._test_simple_bind(self.options, dn, self.secret):
                    self.log.debug(('LDAP bind with {0}').format(dn))
                    return accounts[0]
                raise AuthenticationException('DSA declined username or password')
            elif self.options['binding'] == 'SASL':
                raise AuthenticationException('SASL bind test not implemented!')
            return

        def authenticate(self):
            if Authenticator.authenticate(self):
                return True
            else:
                ldap_object = self._get_ldap_object()
                if ldap_object is not None:
                    return True
                raise AuthenticationException('Incorrect username or password')
                return

        def provision_login(self):
            """ Authenticators can override this method to support auto-provisioning of
                user accounts.  If the account cannot be auto-provsioned this method
                should return None; if the authenticator does not support provisioning
                just return None. """
            ldap_object = self._get_ldap_object()
            return