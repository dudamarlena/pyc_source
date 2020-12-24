# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asfpy/ldap.py
# Compiled at: 2020-03-10 11:06:56
# Size of source mod 2**32: 17290 bytes
""" ASF LDAP Account Manager """
import sys
assert sys.version_info >= (3, 2)
import ldap, ldap.modlist, ldif, re, crypt, random, string
LDAP_SANDBOX = 'ldaps://ldap-sandbox.apache.org:636'
LDAP_MASTER = 'ldaps://ldap-master.apache.org:636'
LDAP_SUFFIX = 'dc=apache,dc=org'
LDAP_PEOPLE_BASE = 'ou=people,dc=apache,dc=org'
LDAP_GROUPS_BASE = 'ou=groups,dc=apache,dc=org'
LDAP_APLDAP_BASE = 'cn=apldap,ou=groups,ou=services,dc=apache,dc=org'
LDAP_CHAIRS_BASE = 'cn=pmc-chairs,ou=groups,ou=services,dc=apache,dc=org'
LDAP_PMCS_BASE = 'ou=project,ou=groups,dc=apache,dc=org'
LDAP_DN = 'uid=%s,ou=people,dc=apache,dc=org'
LDAP_VALID_UID_RE = re.compile('^[a-z0-9][a-z0-9_-]+$')

def bytify(ldiff):
    """ Convert all values in a dict to byte-string """
    for k, v in ldiff.items():
        if type(v) is list:
            n = 0
            for xv in v:
                if type(v[n]) is str:
                    v[n] = xv.encode('utf-8')
                n += 1

        else:
            if type(v) is str:
                v = [
                 v.encode('utf-8')]
        ldiff[k] = v
    else:
        return ldiff


def stringify(ldiff):
    """ Convert all values in a dict to string """
    for k, v in ldiff.items():
        if type(v) is list:
            if len(v) == 1:
                v = v[0]
        elif type(v) is list:
            n = 0
            for xv in v:
                if type(v[n]) is bytes:
                    v[n] = xv.decode('utf-8')
                n += 1

        else:
            if type(v) is bytes:
                v = v.decode('utf-8')
        ldiff[k] = v
    else:
        return ldiff


class ConnectionException(Exception):
    __doc__ = ' Simple exception with a message and an optional origin exception (WIP) '

    def __init__(self, message, origin=None):
        super().__init__(message)
        self.origin = origin


class ValidatorException(Exception):
    __doc__ = ' Simple validator exception with a message and an optional triggering attribute '

    def __init__(self, message, attrib=None):
        super().__init__(message)
        self.attribute = attrib


class committer:
    __doc__ = ' Committer class, allows for munging data '

    def __init__(self, manager, res):
        self.manager = manager
        self.dn = res[0][0]
        self.dn_enc = self.dn.encode('ascii')
        self.attributes = stringify(res[0][1])
        self.uid = self.attributes['uid']

    def add_project(self, project):
        """ Add person to project (as committer) """
        dn = 'cn=%s,%s' % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_ADD, 'member', self.dn_enc)])

    def add_pmc(self, project):
        """ Add person to project (as PMC member) """
        dn = 'cn=%s,%s' % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_ADD, 'owner', self.dn_enc)])

    def add_basic_group(self, group):
        """ Add person to basic posixGroup entry """
        dn = 'cn=%s,%s' % (group, LDAP_GROUPS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_ADD, 'memberUid', self.uid.encode('ascii'))])

    def remove_project(self, project):
        """ Remove person from project (as committer) """
        dn = 'cn=%s,%s' % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_DELETE, 'member', self.dn_enc)])

    def remove_pmc(self, project):
        """ Remove person from PMC """
        dn = 'cn=%s,%s' % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_DELETE, 'owner', self.dn_enc)])

    def remove_basic_group(self, group):
        """ Remove person from basic posixGroup entry """
        dn = 'cn=%s,%s' % (group, LDAP_GROUPS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_DELETE, 'memberUid', self.uid.encode('ascii'))])

    def rename(self, newuid):
        """ Rename an account, fixing in all projects """
        xuid = newuid
        if type(newuid) is str:
            newuid = newuid.encode('ascii')
        else:
            xuid = newuid.decode('ascii')
        if not LDAP_VALID_UID_RE.match(xuid):
            raise ValidatorException('Invalid UID, must match ^[a-z0-9][a-z0-9_-]+$')
        if self.manager.load_account(xuid):
            raise ConnectionException('An account with this uid already exists')
        res = self.manager.lc.search_s(LDAP_SUFFIX, ldap.SCOPE_SUBTREE, 'cn=%s' % xuid)
        if res:
            raise ValidatorException('availid clashes with project name %s!' % res[0][0], 'uid')
        uidnumber = self.manager.nextUid()
        changeset = []
        o_email = self.attributes['asf-committer-email'].encode('ascii')
        n_email = b'%s@apache.org' % newuid
        o_homedir = self.attributes['homeDirectory'].encode('ascii')
        n_homedir = b'/home/%s' % newuid
        changeset.append((ldap.MOD_DELETE, 'asf-committer-email', o_email))
        changeset.append((ldap.MOD_ADD, 'asf-committer-email', n_email))
        changeset.append((ldap.MOD_DELETE, 'homeDirectory', o_homedir))
        changeset.append((ldap.MOD_ADD, 'homeDirectory', n_homedir))
        ouidn = self.attributes['uidNumber'].encode('ascii')
        nuidn = b'%u' % uidnumber
        print('Changing uidNumber/gidNumber to %s...' % uidnumber)
        changeset.append((ldap.MOD_DELETE, 'gidNumber', ouidn))
        changeset.append((ldap.MOD_ADD, 'gidNumber', nuidn))
        changeset.append((ldap.MOD_DELETE, 'uidNumber', ouidn))
        changeset.append((ldap.MOD_ADD, 'uidNumber', nuidn))
        self.manager.lc.modify_s(self.dn, changeset)
        odn = self.dn_enc.decode('ascii')
        newdn = LDAP_DN % xuid
        newdn_enc = newdn.encode('ascii')
        print('Changing %s to %s' % (odn, newdn))
        self.manager.lc.modrdn_s(odn, 'uid=%s' % xuid)
        for role in ('member', 'owner'):
            res = self.manager.lc.search_s(LDAP_SUFFIX, ldap.SCOPE_SUBTREE, '%s=%s' % (role, self.dn_enc.decode('ascii')))

        for entry in res:
            cn = entry[0]
            myhash = entry[1]
            if self.dn_enc in myhash[role]:
                print('Modifying (long) %s attribute in %s ...' % (role, cn))
                self.manager.lc.modify_s(cn, [(ldap.MOD_DELETE, role, self.dn_enc)])
                self.manager.lc.modify_s(cn, [(ldap.MOD_ADD, role, newdn_enc)])
        else:
            ouid = self.uid.encode('ascii')
            for role in ('memberUid', ):
                res = self.manager.lc.search_s(LDAP_SUFFIX, ldap.SCOPE_SUBTREE, '(&(objectClass=posixGroup)(%s=%s))' % (role, self.uid))
                for entry in res:
                    cn = entry[0]
                    myhash = entry[1]
                    if ouid in myhash[role]:
                        print('Modifying (short) %s attribute in %s ...' % (role, cn))
                        self.manager.lc.modify_s(cn, [(ldap.MOD_DELETE, role, ouid)])
                        self.manager.lc.modify_s(cn, [(ldap.MOD_ADD, role, newuid)])
                else:
                    self.uid = xuid
                    self.dn_enc = newdn_enc


class manager:
    __doc__ = ' Top LDAP Manager class for whomever is using the script '

    def __init__(self, user, password, host=LDAP_SANDBOX):
        if not re.match('^[-_a-z0-9]+$', user):
            raise ConnectionException('Invalid characters in User ID. Must be alphanumerical or dashes only.')
        lc = ldap.initialize(host)
        lc.set_option(ldap.OPT_REFERRALS, 0)
        lc.set_option(ldap.OPT_TIMEOUT, 5)
        try:
            lc.simple_bind_s(LDAP_DN % user, password)
        except ldap.INVALID_CREDENTIALS:
            raise ConnectionException('Invalid username or password supplied!')
        except ldap.TIMEOUT:
            raise ConnectionException('The backend authentication server timed out, please retry later.')
        except:
            raise ConnectionException('An unknown error occurred, please retry later.')
        else:
            self.uid = user
            self.dn = LDAP_DN % user
            self.lc = lc
        try:
            res = lc.search_s(LDAP_DN % user, ldap.SCOPE_BASE)
            if not len(res) == 1:
                raise AssertionError
            else:
                assert len(res[0]) == 2
                fn = res[0][1].get('cn')
                raise type(fn) is list and len(fn) == 1 or AssertionError
            self.fullname = str(fn[0], 'utf-8')
            self.email = '%s@apache.org' % user
        except ldap.TIMEOUT:
            raise ConnectionException('The backend authentication server timed out, please retry later.')
        except AssertionError:
            raise ConnectionException('Common backend assertions failed, LDAP corruption?')

        try:
            res = lc.search_s(LDAP_APLDAP_BASE, ldap.SCOPE_BASE)
            if not len(res) == 1:
                raise AssertionError
            else:
                assert len(res[0]) == 2
                members = res[0][1].get('member')
                raise type(members) is list and len(members) > 0 or AssertionError
            self.isAdmin = bytes(LDAP_DN % user, 'utf-8') in members
        except ldap.TIMEOUT:
            raise ConnectionException('The backend authentication server timed out, please retry later.')
        except AssertionError:
            raise ConnectionException('Common backend assertions failed, LDAP corruption?')

    def load_account(self, uid):
        if type(uid) is bytes:
            uid = uid.decode('ascii')
        res = self.lc.search_s(LDAP_PEOPLE_BASE, ldap.SCOPE_SUBTREE, 'uid=%s' % uid)
        if res:
            return committer(self, res)

    def nextUid--- This code section failed: ---

 L. 278         0  SETUP_FINALLY       166  'to 166'

 L. 279         2  LOAD_FAST                'self'
                4  LOAD_ATTR                lc
                6  LOAD_METHOD              search_s
                8  LOAD_GLOBAL              LDAP_PEOPLE_BASE
               10  LOAD_GLOBAL              ldap
               12  LOAD_ATTR                SCOPE_SUBTREE
               14  LOAD_STR                 'uidNumber=*'
               16  LOAD_STR                 'uidNumber'
               18  BUILD_LIST_1          1 
               20  CALL_METHOD_4         4  ''
               22  STORE_FAST               'res'

 L. 280        24  BUILD_MAP_0           0 
               26  STORE_FAST               'umap'

 L. 281        28  LOAD_FAST                'res'
               30  GET_ITER         
               32  FOR_ITER             70  'to 70'
               34  STORE_FAST               'x'

 L. 282        36  LOAD_FAST                'x'
               38  LOAD_CONST               0
               40  BINARY_SUBSCR    
               42  LOAD_FAST                'umap'
               44  LOAD_FAST                'x'
               46  LOAD_CONST               1
               48  BINARY_SUBSCR    
               50  LOAD_METHOD              get
               52  LOAD_STR                 'uidNumber'
               54  CALL_METHOD_1         1  ''
               56  LOAD_CONST               0
               58  BINARY_SUBSCR    
               60  LOAD_METHOD              decode
               62  LOAD_STR                 'ascii'
               64  CALL_METHOD_1         1  ''
               66  STORE_SUBSCR     
               68  JUMP_BACK            32  'to 32'

 L. 283        70  LOAD_LISTCOMP            '<code_object <listcomp>>'
               72  LOAD_STR                 'manager.nextUid.<locals>.<listcomp>'
               74  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               76  LOAD_FAST                'res'
               78  GET_ITER         
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'uids'

 L. 284        84  LOAD_GLOBAL              type
               86  LOAD_FAST                'uids'
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_GLOBAL              list
               92  COMPARE_OP               is
               94  POP_JUMP_IF_FALSE   108  'to 108'
               96  LOAD_GLOBAL              len
               98  LOAD_FAST                'uids'
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_CONST               0
              104  COMPARE_OP               >
              106  POP_JUMP_IF_TRUE    112  'to 112'
            108_0  COME_FROM            94  '94'
              108  LOAD_ASSERT              AssertionError
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM           106  '106'

 L. 285       112  LOAD_GLOBAL              sorted
              114  LOAD_FAST                'uids'
              116  CALL_FUNCTION_1       1  ''
              118  STORE_FAST               'uids'

 L. 286       120  LOAD_GLOBAL              print
              122  LOAD_STR                 'Highest current uidNumber: %s (%s)'
              124  LOAD_FAST                'uids'
              126  LOAD_CONST               -1
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'umap'
              132  LOAD_GLOBAL              str
              134  LOAD_FAST                'uids'
              136  LOAD_CONST               -1
              138  BINARY_SUBSCR    
              140  CALL_FUNCTION_1       1  ''
              142  BINARY_SUBSCR    
              144  BUILD_TUPLE_2         2 
              146  BINARY_MODULO    
              148  CALL_FUNCTION_1       1  ''
              150  POP_TOP          

 L. 287       152  LOAD_FAST                'uids'
              154  LOAD_CONST               -1
              156  BINARY_SUBSCR    
              158  LOAD_CONST               1
              160  BINARY_ADD       
              162  POP_BLOCK        
              164  RETURN_VALUE     
            166_0  COME_FROM_FINALLY     0  '0'

 L. 288       166  DUP_TOP          
              168  LOAD_GLOBAL              ldap
              170  LOAD_ATTR                TIMEOUT
              172  COMPARE_OP               exception-match
              174  POP_JUMP_IF_FALSE   194  'to 194'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L. 289       182  LOAD_GLOBAL              ConnectionException
              184  LOAD_STR                 'The backend authentication server timed out, please retry later.'
              186  CALL_FUNCTION_1       1  ''
              188  RAISE_VARARGS_1       1  'exception instance'
              190  POP_EXCEPT       
              192  JUMP_FORWARD        222  'to 222'
            194_0  COME_FROM           174  '174'

 L. 290       194  DUP_TOP          
              196  LOAD_GLOBAL              AssertionError
              198  COMPARE_OP               exception-match
              200  POP_JUMP_IF_FALSE   220  'to 220'
              202  POP_TOP          
              204  POP_TOP          
              206  POP_TOP          

 L. 291       208  LOAD_GLOBAL              ConnectionException
              210  LOAD_STR                 'Common backend assertions failed, LDAP corruption?'
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
              216  POP_EXCEPT       
              218  JUMP_FORWARD        222  'to 222'
            220_0  COME_FROM           200  '200'
              220  END_FINALLY      
            222_0  COME_FROM           218  '218'
            222_1  COME_FROM           192  '192'

Parse error at or near `POP_TOP' instruction at offset 178

    def create_account(self, uid, email, fullname, forcePass=None, requireTwo=True):
        """ Attempts to create a committer account in LDAP """
        if not self.isAdmin:
            raise ConnectionException('You do not have sufficient access to create accounts')
        else:
            if not LDAP_VALID_UID_RE.match(uid):
                raise ValidatorException('Invalid UID, must match ^[a-z0-9][a-z0-9_-]+$')
            if self.load_account(uid):
                raise ConnectionException('An account with this uid already exists')
            res = self.lc.search_s(LDAP_SUFFIX, ldap.SCOPE_SUBTREE, 'cn=%s' % uid)
            if res:
                raise ValidatorException('availid clashes with project name %s!' % res[0][0], 'uid')
            uidnumber = self.nextUid()
            names = fullname.split(' ')
            if len(names) < 2 and requireTwo:
                raise ValidatorException('Full name needs at least two parts!', 'fullname')
        givenName = names[0]
        surName = names[(-1)]
        for n in names:
            if not n.strip():
                raise ValidatorException('Found part of name with too much spacing!', 'fullname')
            if not re.match('^\\S+@\\S+?\\.\\S+$', email):
                raise ValidatorException('Invalid email address supplied!', 'email')
            password = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(16)))
            if forcePass:
                password = forcePass
            password_crypted = crypt.crypt(password, crypt.mksalt(method=(crypt.METHOD_MD5)))
            ldiff = {'objectClass':[
              'person', 'top', 'posixAccount', 'organizationalPerson', 'inetOrgPerson', 'asf-committer', 'hostObject', 'ldapPublicKey'], 
             'loginShell':'/bin/bash', 
             'asf-sascore':'10', 
             'givenName':givenName, 
             'sn':surName, 
             'mail':email, 
             'gidNumber':str(uidnumber), 
             'uidNumber':str(uidnumber), 
             'asf-committer-email':'%s@apache.org' % uid, 
             'cn':fullname, 
             'homeDirectory':'/home/%s' % uid, 
             'userPassword':'{CRYPT}' + password_crypted}
            bytify(ldiff)
            dn = LDAP_DN % uid
            am = ldap.modlist.addModlist(ldiff)
            self.lc.add_s(dn, am)
            return self.load_account(uid)


class client:
    __doc__ = ' Top LDAP read-only client '

    def __init__(self, user, password, host=LDAP_SANDBOX):
        lc = ldap.initialize(host)
        lc.set_option(ldap.OPT_REFERRALS, 0)
        lc.set_option(ldap.OPT_TIMEOUT, 5)
        try:
            lc.simple_bind_s(user, password)
        except ldap.INVALID_CREDENTIALS:
            raise ConnectionException('Invalid username or password supplied!')
        except ldap.TIMEOUT:
            raise ConnectionException('The backend authentication server timed out, please retry later.')
        except Exception:
            raise ConnectionException('An unknown error occurred, please retry later.')
        else:
            self.uid = user
            self.dn = LDAP_DN % user
            self.lc = lc

    def load_account(self, uid):
        if type(uid) is bytes:
            uid = uid.decode('ascii')
        res = self.lc.search_s(LDAP_PEOPLE_BASE, ldap.SCOPE_SUBTREE, 'uid=%s' % uid)
        if res:
            return committer(self, res)

    def list_groups(self, base=LDAP_PMCS_BASE):
        groups = []
        res = self.lc.search_s(base, ldap.SCOPE_ONELEVEL, 'cn=*')
        for entry in res:
            cn = entry[1]['cn'][0].decode('utf-8')
            groups.append(cn)
        else:
            return sorted(groups)

    def list_members(self, group, role='member'):
        members = []
        if ',' not in group:
            group = 'cn=%s,%s' % (group, LDAP_PMCS_BASE)
        res = self.lc.search_s(group, (ldap.SCOPE_SUBTREE), attrlist=[role])
        for entry in res[0][1][role]:
            members.append(entry.decode('utf-8'))
        else:
            return sorted(members)


class LDIFWriter_Sane(ldif.LDIFWriter):
    __doc__ = ' LDIFWriter with b64 detection fixed '

    def _needs_base64_encoding(self, attr_type, attr_value):
        """
        returns 1 if attr_value has to be base-64 encoded because
        of special chars or because attr_type is in self._base64_attrs
        """
        if attr_type.lower() == 'dn':
            return False
        SAFE_STRING_PATTERN = '(^[\\x22-\\x7Fa-zA-Z ]+$)'
        if type(attr_value) is bytes:
            attr_value = attr_value.decode('utf-8')
        return attr_type.lower() in self._base64_attrs or re.match(SAFE_STRING_PATTERN, attr_value) is None