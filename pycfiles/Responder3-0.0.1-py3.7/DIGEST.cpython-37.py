# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\protocols\authentication\DIGEST.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 7848 bytes
import enum, hashlib, collections
from responder3.protocols.authentication.common import *
from responder3.core.logging.log_objects import Credential

def n2e(x):
    if x is None:
        return ''
    return x


class DIGESTAlgo(enum.Enum):
    MD5 = 'MD5'
    MD5_SESS = 'MD5-Sess'
    TOKEN = 'TOKEN'


class DIGESTStatus(enum.Enum):
    START = enum.auto()
    AUTHENTICATE = enum.auto()
    AUTHORIZE = enum.auto()
    FINISH = enum.auto()


class DIGESTAuthenticate:

    def __init__(self):
        self.method = 'DIGEST'
        self.challenge = None
        self.realm = None
        self.domain = None
        self.nonce = None
        self.opaque = None
        self.stale = None
        self.algorithm = None
        self.qop = None
        self.auth = []
        self.uri = None

    def to_line(self):
        data = ''
        t = collections.OrderedDict()
        t['realm'] = '"%s"' % self.realm if self.realm else '""'
        if not self.nonce:
            raise Exception('DIGEST nonce needs to be set!')
        t['nonce'] = '"%s"' % self.nonce
        t['opaque'] = '"%s"' % self.opaque if self.opaque else '"AAAAAAAAAAAAAA"'
        t['stale'] = str(self.stale)
        t['algorithm'] = self.algorithm.name
        if self.domain:
            t['domain'] = self.domain
        if self.qop:
            t['qop'] = self.qop
        if self.auth:
            t['auth'] = self.auth
        tt = []
        for key in t:
            tt.append('%s=%s' % (key, t[key]))

        data += ','.join(tt)
        return data

    @staticmethod
    def from_dict(kv):
        ds = DIGESTAuthenticate()
        ds.challenge = kv['challenge']
        ds.realm = kv['realm']
        ds.domain = kv['domain']
        ds.nonce = kv['nonce']
        ds.opaque = kv['opaque']
        ds.stale = bool(kv['stale'])
        ds.algorithm = DIGESTAlgo(kv['algorithm'].upper())
        if 'domain' in kv:
            ds.domain = kv['domain']
        if 'qop' in kv:
            ds.qop_options = kv['qop'].split(',')
        if 'auth' in kv:
            ds.auth = kv['auth'].split(',')
        return ds

    @staticmethod
    def from_line(data):
        m = data.find(' ')
        t_method = data[:m].upper()
        if t_method != 'DIGEST':
            raise Exception('Expected DIGEST, got %s' % t_method)
        t_data = data[m + 1:]
        kv = {}
        for elem in t_data.split(','):
            key, value = elem.split('=')
            if value[0] == '"':
                value = value[1:-1]
            kv[key] = value

        da = DIGESTAuthenticate.from_dict(kv)
        return da


class DIGESTAuthorize:

    def __init__(self):
        self.username = None
        self.realm = None
        self.uri = None
        self.qop = None
        self.nonce = None
        self.cnonce = None
        self.nonce_count = None
        self.response = None
        self.algorithm = None
        self.opaque = None
        self.auth = None

    def to_line(self):
        data = ''
        return data

    @staticmethod
    def from_dict(kv):
        ds = DIGESTAuthorize()
        ds.username = kv['username']
        ds.realm = kv['realm']
        ds.uri = kv['uri']
        ds.nonce = kv['nonce']
        ds.opaque = kv.get('opaque', None)
        ds.algorithm = DIGESTAlgo(kv['algorithm'].upper())
        ds.response = kv['response']
        if 'qop' in kv:
            ds.cnonce = kv['cnonce']
            ds.nonce_count = kv['nonce-count']
            ds.qop = kv['qop'].split(',')
        if 'auth' in kv:
            ds.auth = kv['auth'].split(',')
        return ds

    @staticmethod
    def from_line(data):
        kv = {}
        for elem in data.split(','):
            elem = elem.strip()
            key, value = elem.split('=')
            if value[0] == '"':
                value = value[1:-1]
            kv[key] = value

        da = DIGESTAuthorize.from_dict(kv)
        return da


class DIGEST:

    def __init__(self, credentials):
        self.mode = None
        self.status = DIGESTStatus.START
        self.credentials = credentials
        self.authenticate = None
        self.authorize = None
        self.hash_obj = None
        self.HA1 = None
        self.HA2 = None
        self.response = None

    def setup_defaults(self):
        self.mode = AUTHModuleMode.SERVER
        kv = {'challenge':'AAAAAAAAAAAAAAAAAAAA', 
         'realm':'TEST', 
         'domain':'TEST', 
         'nonce':'AAAAAAAAAAAAAAAAAAAA', 
         'opaque':'AAAAAAAAAAAAAAAAAAAA', 
         'stale':False, 
         'algorithm':'MD5'}
        self.authenticate = DIGESTAuthenticate.from_dict(kv)

    def setup(self, settings):
        raise Exception('Not implemented!')

    def get_a1(self, password, ha1=None):
        a1 = '%s:%s:%s' % (self.authorize.username, self.authorize.realm, password)
        if DIGESTAlgo.MD5_SESS:
            if not ha1:
                ha1 = self.hash_obj(a1.encode()).digest()
            a1 = b'%s:%s:%s' % (ha1, self.authorize.nonce, self.authorize.cnonce)
        return a1

    def get_a2(self, method, body_data=None):
        a2 = b'%s:%s' % (method, self.authorize.uri.encode())
        if self.authenticate.qop == 'auth-int':
            a2 = b'%s:%s' % (a2, self.hash_obj(body_data).digest())
        return a2

    def verify_creds(self, method=None, body_data=None):
        """
                Verifyies user creds, returns a tuple with (verification_result, credential)
                currently it products SIP hash, sorry
                also it doesnt variy creds, todo
                """
        fullhash = '$sip$*%s' % '*'.join([
         n2e(self.authenticate.uri),
         n2e(self.authorize.uri),
         n2e(self.authorize.username),
         n2e(self.authorize.realm),
         n2e(method),
         n2e(''),
         n2e(''),
         n2e(''),
         n2e(self.authenticate.nonce),
         n2e(self.authorize.cnonce),
         n2e(self.authorize.nonce_count),
         n2e(self.authorize.qop),
         n2e(self.authenticate.algorithm.name),
         n2e(self.authorize.response)])
        credential = Credential('DIGEST',
          domain=(self.authorize.realm),
          username=(self.authorize.username),
          fullhash=fullhash)
        return (
         AuthResult.FAIL, credential)

    def do_auth(self, data=None, method=None, body_data=None):
        if self.mode == AUTHModuleMode.SERVER:
            if self.status == DIGESTStatus.START:
                if data is None:
                    self.status = DIGESTStatus.AUTHORIZE
                    return (
                     AuthResult.CONTINUE, self.authenticate.to_line())
                self.status = DIGESTStatus.AUTHORIZE
            if self.status == DIGESTStatus.AUTHORIZE:
                if data is not None:
                    self.status = DIGESTStatus.FINISH
                    self.authorize = DIGESTAuthorize.from_line(data)
                    return self.verify_creds(method=None, body_data=None)
                raise Exception('DIGEST AUTH: input data expected in SERVER|AUTHORIZE state')
            else:
                raise Exception('DIGEST AUTH: Unexpected SERVER state')
        elif self.mode == AUTHModuleMode.CLIENT:
            if self.status == DIGESTStatus.START:
                if data is not None:
                    self.status = DIGESTStatus.FINISH
                    self.authenticate = DIGESTAuthenticate.to_line()
                    self.authorize = DIGESTAuthorize.construct(self.authenticate, credential)
                    return (AuthResult.OK, self.authorize.to_line())
                raise Exception('DIGEST AUTH: input data expected in SERVER|AUTHORIZE state')
        else:
            raise Exception('DIGEST Unknown mode: %s' % self.mode)