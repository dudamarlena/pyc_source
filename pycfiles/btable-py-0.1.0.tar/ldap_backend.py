# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/backend/ldap_backend.py
# Compiled at: 2015-10-20 16:27:01
import os, datetime, ldap
from bta.backend import Backend, VirtualTable, SpecialTable
import bta.tools.expr, bta.tools.decoding, bta.datatable, bta.sd, logging
log = logging.getLogger('bta.backend.ldap')

@Backend.register('ldap')
class LDAPBackend(Backend):

    def __init__(self, options, connection=None):
        Backend.__init__(self, options, connection)
        self.cnx = ldap.initialize(self.connection)
        self.user = os.getenv('BTA_LDAP_USER')
        self.passwd = os.getenv('BTA_LDAP_PASS')
        self.cnx.simple_bind_s(self.user, self.passwd)

    def open_virtual_table(self, name):
        if name == 'datasd':
            return LDAPVirtualDataSD(self.options, self, name)

    def open_special_table(self, name):
        if name == 'categories':
            return LDAPCategories()


class LDAPCategories(SpecialTable):
    person = 'person'
    computer = 'computer'

    def assert_consistency(self):
        pass


class LDAPReqBuilder(bta.tools.expr.Builder):
    flags = {'userAccountControl': bta.datatable.UserAccountControl}

    @classmethod
    def get_flag_num(cls, field, flag):
        f = cls.flags[field]
        return f[flag]

    @classmethod
    def _field_(cls, name):
        return name

    @classmethod
    def _eq_(cls, op1, op2):
        return '(%s=%s)' % (op1, op2)

    @classmethod
    def _ne_(cls, op1, op2):
        return '(!%s=%s)' % (op1, op2)

    @classmethod
    def _and_(cls, op1, op2):
        return '(&%s%s)' % (op1, op2)

    @classmethod
    def _or_(cls, op1, op2):
        return '(|%s%s)' % (op1, op2)

    @classmethod
    def _present_(cls, op1):
        return '(%s=*)' % op1

    @classmethod
    def _absent_(cls, op1):
        return '(!%s=*)' % op1

    @classmethod
    def _flagon_(cls, op1, op2):
        op2num = cls.get_flag_num(op1, op2)
        return '(%s:1.2.840.113556.1.4.803:=%i)' % (op1, op2num)

    @classmethod
    def _flagoff_(cls, op1, op2):
        op2num = cls.get_flag_num(op1, op2)
        return '(!%s:1.2.840.113556.1.4.804:=%i)' % (op1, op2num)


LDAP_NORMALIZERS = {'userAccountControl': lambda x: bta.datatable.UserAccountControl(int(x)).to_json(), 
   'msExchUserAccountControl': lambda x: bta.datatable.UserAccountControl(int(x)).to_json(), 
   'objectSid': lambda x: bta.tools.decoding.decode_sid(x, '>'), 
   'primaryGroupID': int, 
   'msExchRecipientDisplayType': int, 
   'instanceType': int, 
   'dSCorePropagationData': lambda x: map(lambda y: datetime.datetime.strptime(y[:14], '%Y%m%d%H%M%S'), x), 
   'whenCreated': lambda y: datetime.datetime.strptime(y[:14], '%Y%m%d%H%M%S'), 
   'whenChanged': lambda y: datetime.datetime.strptime(y[:14], '%Y%m%d%H%M%S'), 
   'msExchWhenMailboxCreated': lambda y: datetime.datetime.strptime(y[:14], '%Y%m%d%H%M%S'), 
   'msExchMailboxSecurityDescriptor': bta.sd.sd_to_json, 
   'uSNCreated': int, 
   'uSNChanged': int, 
   'objectGUID': bta.tools.decoding.decode_guid, 
   'msExchMailboxGUID': bta.tools.decoding.decode_guid, 
   'sAMAccountType': int, 
   'msExchVersion': int, 
   'pwdLastSet': lambda x: datetime.datetime.fromtimestamp(int(x) / 10000000 - 11644473600)}

def normalize_ldap_entry(e):
    n = {}
    for k, v in e.iteritems():
        if len(v) == 1 and k not in ('dSCorePropagationData', ):
            v = v[0]
        if k in LDAP_NORMALIZERS:
            v = LDAP_NORMALIZERS[k](v)
        try:
            if type(v) is str:
                v = v.decode('utf8')
            elif type(v) is list and len(v) > 0 and type(v[0]) is str:
                v = [ vv.decode('utf8') for vv in v ]
        except UnicodeDecodeError:
            pass

        n[k] = v

    return n


class LDAPVirtualDataSD(VirtualTable):

    def __init__(self, options, backend, name):
        VirtualTable.__init__(self, options, backend, name)

    def find(self, request, projection=None):
        dtreq = request.build(LDAPReqBuilder)
        log.debug('LDAP request: [%s]' % dtreq)
        entries = self.backend.cnx.search_s('', ldap.SCOPE_SUBTREE, dtreq)
        return (normalize_ldap_entry(e[1]) for e in entries)

    def assert_consistency(self):
        pass