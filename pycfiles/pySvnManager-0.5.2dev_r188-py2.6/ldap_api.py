# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/model/ldap_api.py
# Compiled at: 2010-09-03 11:31:17
import ldap, sys, logging
log = logging.getLogger(__name__)

class LDAP(object):

    def __init__(self, config):
        self.config = config
        self.verbose = getattr(self.config, 'ldap_verbose', False)
        self.coding = getattr(self.config, 'ldap_coding', 'utf-8')
        filter = getattr(self.config, 'ldap_filter', '(!(objectClass=gosaUserTemplate))(authorizedService=svn)(ossxpConfirmed=TRUE)') or ''
        if '(uid=%(username)s)' in filter:
            filter = filter.replace('(uid=%(username)s)', '(!(objectClass=gosaUserTemplate))')
        if filter.startswith('(&'):
            filter = filter[2:-1]
        if filter and not filter.startswith('('):
            filter = '(%s)' % filter
        self.filter = filter
        self.attr_uid = getattr(self.config, 'ldap_uid_attribute', 'uid')
        self.attr_givenname = getattr(self.config, 'ldap_givenname_attribute', 'givenName')
        self.attr_sn = getattr(self.config, 'ldap_surname_attribute', 'sn')
        self.attr_cn = getattr(self.config, 'ldap_aliasname_attribute', 'cn')
        self.attr_mail = getattr(self.config, 'ldap_email_attribute', 'mail')
        self.l = self.ldap_bind()

    def ldap_bind(self):
        """ get authentication data from form, authenticate against LDAP (or Active
            Directory), fetch some user infos from LDAP and create a user object
            for that user. The session is kept by the moin_session auth plugin.
        """
        if not self.config or not hasattr(self.config, 'ldap_base'):
            log.warning('LDAP not config yet, must define ldap_base and other ldap settings.')
            return
        else:
            try:
                log.debug('LDAP: Setting misc. options...')
                ldap.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
                ldap.set_option(ldap.OPT_REFERRALS, getattr(self.config, 'ldap_referrals', 0))
                ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, getattr(self.config, 'ldap_timeout', 10))
                starttls = getattr(self.config, 'ldap_start_tls', False)
                if hasattr(ldap, 'TLS_AVAIL') and ldap.TLS_AVAIL:
                    for (option, value) in ((ldap.OPT_X_TLS_CACERTDIR, getattr(self.config, 'ldap_tls_cacertdir', '')),
                     (
                      ldap.OPT_X_TLS_CACERTFILE, getattr(self.config, 'ldap_tls_cacertfile', '')),
                     (
                      ldap.OPT_X_TLS_CERTFILE, getattr(self.config, 'ldap_tls_certfile', '')),
                     (
                      ldap.OPT_X_TLS_KEYFILE, getattr(self.config, 'ldap_tls_keyfile', '')),
                     (
                      ldap.OPT_X_TLS_REQUIRE_CERT, getattr(self.config, 'ldap_tls_require_cert', ldap.OPT_X_TLS_NEVER)),
                     (
                      ldap.OPT_X_TLS, starttls)):
                        if value:
                            ldap.set_option(option, value)

                server = getattr(self.config, 'ldap_uri', 'ldap://localhost')
                if self.verbose:
                    log.debug('LDAP: Trying to initialize %r.' % server)
                l = ldap.initialize(server)
                if self.verbose:
                    log.debug('LDAP: Connected to LDAP server %r.' % server)
                if starttls and server.startswith('ldap:'):
                    if self.verbose:
                        log.debug('LDAP: Trying to start TLS to %r.' % server)
                    try:
                        l.start_tls_s()
                        if self.verbose:
                            log.debug('LDAP: Using TLS to %r.' % server)
                    except (ldap.SERVER_DOWN, ldap.CONNECT_ERROR), err:
                        if self.verbose:
                            log.debug("LDAP: Couldn't establish TLS to %r (err: %s)." % (server, str(err)))
                        raise

                ldap_binddn = getattr(self.config, 'ldap_binddn', '')
                ldap_bindpw = getattr(self.config, 'ldap_bindpw', '')
                l.simple_bind_s(ldap_binddn.encode(self.coding), ldap_bindpw.encode(self.coding))
                if self.verbose:
                    log.debug('LDAP: Bound with binddn %r' % ldap_binddn)
            except ldap.INVALID_CREDENTIALS, err:
                log.debug('LDAP bind failed, invalid bind credentials.')
                return
            except:
                import traceback
                info = sys.exc_info()
                log.debug('LDAP: caught an exception, traceback follows...')
                log.debug(('').join(traceback.format_exception(*info)))
                return

            return l
            return

    def is_bind(self):
        return self.l is not None

    def fetch_user(self, username, attrs=None):
        if not self.is_bind():
            return
        else:
            try:
                filter = '(&(uid=%s)%s)' % (username, self.filter)
                if attrs is None:
                    attrs = [
                     self.attr_uid,
                     self.attr_givenname,
                     self.attr_sn,
                     self.attr_cn,
                     self.attr_mail]
                if self.verbose:
                    log.debug('LDAP: Searching %r' % filter)
                lusers = self.l.search_st(self.config.ldap_base, getattr(self.config, 'ldap_scope', ldap.SCOPE_SUBTREE), filter.encode(self.coding), attrlist=attrs, timeout=getattr(self.config, 'ldap_timeout', 10))
                lusers = [ (dn, ldap_dict) for (dn, ldap_dict) in lusers if dn is not None ]
                if self.verbose:
                    for (dn, ldap_dict) in lusers:
                        log.debug('LDAP: dn:%r' % dn)
                        for (key, val) in ldap_dict.items():
                            log.debug('    %r: %r' % (key, val))

            except ldap.INVALID_CREDENTIALS, err:
                log.debug('LDAP bind failed, invalid bind credentials.')
                return
            except:
                import traceback
                info = sys.exc_info()
                log.debug('LDAP: caught an exception, traceback follows...')
                log.debug(('').join(traceback.format_exception(*info)))
                return

            return lusers
            return

    def test_login(self, username, password):
        if not username or not password or self.l is None:
            return False
        else:
            lusers = self.fetch_user(username)
            result_length = len(lusers)
            if result_length != 1:
                if result_length > 1:
                    log.debug('LDAP: Search found more than one (%d) matches.' % result_length)
                if result_length == 0:
                    if self.verbose:
                        log.debug('LDAP: Search found no matches.')
                return False
            (dn, ldap_dict) = lusers[0]
            if self.verbose:
                log.debug('LDAP: DN found is %r, trying to bind with pw' % dn)
            try:
                self.l.simple_bind_s(dn, password.encode(self.coding))
            except ldap.INVALID_CREDENTIALS, err:
                log.debug('LDAP bind failed, invalid bind credentials.')
                return False
            except:
                import traceback
                info = sys.exc_info()
                log.debug('LDAP: caught an exception, traceback follows...')
                log.debug(('').join(traceback.format_exception(*info)))
                return False

            return True
            return

    def fetch_all_users(self, filter=None, attrs=None):
        if not self.is_bind():
            return
        else:
            try:
                if not filter:
                    filter = '(&(uid=*)%s)' % self.filter
                if attrs is None:
                    attrs = [
                     self.attr_uid,
                     self.attr_givenname,
                     self.attr_sn,
                     self.attr_cn,
                     self.attr_mail]
                if self.verbose:
                    log.debug('LDAP: Searching %r' % filter)
                lusers = self.l.search_st(self.config.ldap_base, getattr(self.config, 'ldap_scope', ldap.SCOPE_SUBTREE), filter.encode(self.coding), attrlist=attrs, timeout=getattr(self.config, 'ldap_timeout', 10))
                lusers = [ (dn, ldap_dict) for (dn, ldap_dict) in lusers if dn is not None ]
                if self.verbose:
                    for (dn, ldap_dict) in lusers:
                        log.debug('LDAP: dn:%r' % dn)
                        for (key, val) in ldap_dict.items():
                            log.debug('    %r: %r' % (key, val))

            except ldap.INVALID_CREDENTIALS, err:
                log.debug('LDAP bind failed, invalid bind credentials.')
                return
            except:
                import traceback
                info = sys.exc_info()
                log.debug('LDAP: caught an exception, traceback follows...')
                log.debug(('').join(traceback.format_exception(*info)))
                return

            return lusers
            return