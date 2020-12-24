# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/ldap/update_users_from_ldap.py
# Compiled at: 2012-10-12 07:02:39
import json
from coils.core import CoilsException, PropertyManager
from coils.foundation import ldap_paged_search, LDAPConnectionFactory
from coils.core.logic import ActionCommand
try:
    import ldap
except:

    class UpdateUsersFromLDAP(object):
        pass


else:

    class UpdateUsersFromLDAP(ActionCommand):
        __domain__ = 'action'
        __operation__ = 'update-users-from-ldap'
        __aliases__ = ['updateUsersFromLDAP', 'updateUsersFromLDAPAction']

        def __init__(self):
            ActionCommand.__init__(self)

        @property
        def result_mimetype(self):
            return 'text/plain'

        def do_action(self):
            if not self._ctx.is_admin:
                raise CoilsException(('Insufficient privilages to invoke {0}').format(self.__operation__))
            dsa = LDAPConnectionFactory.Connect(self._dsa)
            results = ldap_paged_search(connection=dsa, logger=self.log, search_filter=self._xfilter, search_base=self._xroot, attributes=[ str(x) for x in self._xmap.keys() ], search_scope=self._xscope)
            self.wfile.write(('LDAP Filter:{0}\n').format(self._xfilter))
            self.wfile.write(('LDAP Base:{0}\n').format(self._xroot))
            self.wfile.write(('LDAP Attributes:{0}\n').format([ str(x) for x in self._xmap.keys() ]))
            self.wfile.write('\n')
            self.wfile.write(('Search found {0} results\n').format(len(results)))
            self.wfile.write('\n')
            count = 0
            for user in results:
                self.log.info(user)
                count += 1
                ldap_dn = user[0]
                attributes = {}
                for (key, value) in user[1].items():
                    if value:
                        attributes[unicode(key).lower()] = value[0]
                    else:
                        value = None

                self.wfile.write('\n')
                self.wfile.write(('LDAP DN:{0}\n').format(ldap_dn))
                uid = attributes[self._xuid]
                if uid is None:
                    self.wfile.write(('No UID attribute found for "{0}"\n').format(ldap_dn))
                    self.wfile.write('\n')
                    continue
                if self._strip:
                    uid = uid.split(self._strip)[0]
                account = self._ctx.run_command('account::get', login=uid)
                is_new = False
                if not account:
                    if self._create == 'YES':
                        account = self._ctx.run_command('contact::new', values={'login': uid, 'is_account': 1, 
                           'ldap_url': ldap_dn, 
                           'source_url': ldap_dn})
                        self.wfile.write(('Creating new account for UID "{0}"').format(uid))
                        is_new = True
                    else:
                        self.wfile.write(('No account object foundfor UID "{0}"').format(uid))
                        self.wfile.write('\n')
                        continue
                for (source, target) in self._xmap.items():
                    value = None
                    if source.lower() in attributes:
                        value = attributes[source.lower()]
                    if not value:
                        continue
                    target = target.split('.')
                    if len(target) == 1:
                        setattr(account, target[0], value)
                        self.wfile.write((' set contact value "{0}" to "{1}"\n').format(target[0], value))
                    elif target[0] == 'cv':
                        cv = account.get_company_value(target[1])
                        if cv:
                            cv.set_value(value)
                            self.wfile.write((' set company value "{0}" to "{1}"\n').format(cv.name, value))
                    elif target[0] == 'property':
                        (namespace, name) = PropertyManager.Parse_Property_Name(('.').join(target[1:]))
                        self._ctx.property_manager.set_property(account, namespace, name, value)
                        self.wfile.write((' assigned value "{0}" to property "{{{1}}}{2}"\n').format(value, namespace, name))
                    elif target[0] == 'telephone':
                        telephone = account.telephones.get(target[1], None)
                        if telephone:
                            setattr(telephone, target[2], value)
                            self.wfile.write((' set telephone type "{0}" attribute "{1}" to "{2}"\n').format(target[1], target[2], value))
                    elif target[0] == 'address':
                        address = account.addresses.get(target[1], None)
                        if address:
                            setattr(address, target[2], value)
                            self.wfile.write((' set address type "{0}" attribute "{1}" to "{2}"\n').format(target[1], target[2], value))

            self.wfile.write('\n')
            return

        def parse_action_parameters(self):
            self._dsa = self.action_parameters.get('dsaName', None)
            self._xfilter = self.action_parameters.get('filterText', None)
            self._xuid = self.action_parameters.get('uidAttribute', 'uid')
            self._xmap = self.action_parameters.get('attributeMap', None)
            self._xroot = self.action_parameters.get('searchRoot', None)
            self._xscope = self.action_parameters.get('searchScope', 'SUBTREE').upper()
            self._create = self.action_parameters.get('createAccounts', 'YES').upper()
            self._strip = self.action_parameters.get('stripLogins', None)
            if not self._dsa:
                raise CoilsException('No dsaNAME parameter specified for updateUsersFromLDAPAction')
            if not self._xfilter:
                raise CoilsException('No filterText [LDAP Search Filter] parameter specified for updateUsersFromLDAPAction')
            if not self._xmap:
                raise CoilsException('No attributeMap parameter specified for updateUsersFromLDAPAction')
            try:
                self._xmap = json.loads(self._xmap)
            except:
                raise CoilsException('updateUsersFromLDAPAction unable to parse attributeMap parameter')

            if not isinstance(self._xmap, dict):
                raise CoilsException('updateUsersFromLDAPAction attributeMap parameter is not a dictionary value.')
            if not self._xroot:
                raise CoilsException('No searchRoot parameter specified for updateUsersFromLDAPAction')
            if self._xscope == 'ONELEVEL':
                self._xscope = ldap.SCOPE_ONELEVEL
            else:
                self._xscope = ldap.SCOPE_SUBTREE
            return