# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/ldap/search.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import ldap_paged_search
from coils.core.logic import ActionCommand
from dsml1_writer import DSML1Writer
try:
    import ldap
except:

    class SearchAction(object):
        pass


else:

    class SearchAction(ActionCommand):
        __domain__ = 'action'
        __operation__ = 'ldap-search'
        __aliases__ = ['ldapSearch', 'ldapSearchAction']
        __debugOn__ = None

        def __init__(self):
            ActionCommand.__init__(self)
            if SearchAction.__debugOn__ is None:
                sd = ServerDefaultsManager()
                SearchAction.__debugOn__ = sd.bool_for_default('LDAPDebugEnabled')
            return

        @property
        def debugOn(self):
            return SearchAction.__debugOn__

        def do_action(self):
            dsa = LDAPConnectionFactory.Connect(self._dsa)
            if dsa is None:
                raise CoilsException(('Unable to acquire connection to DSA "{0}"').format(self._dsa))
            if self.debugOn:
                self.log.debug('LDAP SEARCH: Got connection to DSA')
            if len(self._xattrs) == 0:
                self.xattrs = None
            try:
                results = ldap_paged_search(connection=dsa, logger=self.log, search_filter=self._xfilter, search_base=self._xroot, attributes=self._xattrs, search_scope=self._xscope)
            except ldap.NO_SUCH_OBJECT, e:
                self.log.exception(e)
                self.log.info('LDAP NO_SUCH_OBJECT exception, generating empty message')
            except ldap.INSUFFICIENT_ACCESS, e:
                self.log.exception(e)
                self.log.info('LDAP INSUFFICIENT_ACCESS exception, generating empty message')
            except ldap.SERVER_DOWN, e:
                self.log.exception(e)
                self.log.warn('Unable to contact LDAP server!')
                raise e
            except Exception, e:
                self.log.error('Exception in action ldapSearch')
                self.log.exception(e)
                raise e
            else:
                if self.debugOn:
                    self.log.debug('LDAP SEARCH: Formatting results to DSML.')
                writer = DSML1Writer()
                writer.write(results, self.wfile)

            dsa.unbind()
            return

        def parse_action_parameters(self):
            self._dsa = self.action_parameters.get('dsaName', None)
            self._xfilter = self.action_parameters.get('filterText', None)
            self._xroot = self.action_parameters.get('searchRoot', None)
            self._xscope = self.action_parameters.get('searchScope', 'SUBTREE').upper()
            self._xlimit = int(self.action_parameters.get('searchLimit', 150))
            self._xattrs = []
            for xattr in self.action_parameters.get('attributes', '').split(','):
                self._xattrs.append(str(xattr))

            if self._dsa is None:
                raise CoilsException('No DSA defined for ldapSearch')
            if self._xfilter is None:
                raise CoilsException('No filter defined for ldapSearch')
            else:
                self._xfilter = self.decode_text(self._xfilter)
                self._xfilter = self.process_label_substitutions(self._xfilter)
            if self._xroot is None:
                raise CoilsException('No root defined for ldapSearch')
            else:
                self._xroot = self.decode_text(self._xroot)
            if self._xscope == 'SUBTREE':
                self._xscope = ldap.SCOPE_SUBTREE
            else:
                self._xscope = ldap.SCOPE_SUBTREE
            if self.debugOn:
                self.log.debug(('LDAP SEARCH FILTER:{0}').format(self._xfilter))
                self.log.debug(('LDAP SEARCH BASE:{0}').format(self._xroot))
                self.log.debug(('LDAP SEARCH LIMIT:{0}').format(self._xlimit))
            return

        def do_epilogue(self):
            pass