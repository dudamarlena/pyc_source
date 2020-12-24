# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\protocols\KerberosV5.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 29407 bytes
from asn1crypto import core
import enum, os
from responder3.core.commons import *
from responder3.core.logging.log_objects import Credential
from responder3.core.asyncio_helpers import *
TAG = 'explicit'
UNIVERSAL = 0
APPLICATION = 1
CONTEXT = 2
krb5_pvno = 5

class NAME_TYPE(enum.Enum):
    UNKNOWN = 0
    PRINCIPAL = 1
    SRV_INST = 2
    SRV_HST = 3
    SRV_XHST = 4
    UID = 5
    X500_PRINCIPAL = 6
    SMTP_NAME = 7
    ENTERPRISE_PRINCIPAL = 10
    WELLKNOWN = 11
    ENT_PRINCIPAL_AND_ID = -130
    MS_PRINCIPAL = -128
    MS_PRINCIPAL_AND_ID = -129
    NTLM = -1200


class MESSAGE_TYPE(enum.Enum):
    KRB_AS_REQ = 10
    KRB_AS_REP = 11
    KRB_TGS_REQ = 12
    KRB_TGS_REP = 13
    KRB_AP_REQ = 14
    KRB_AP_REP = 15
    KRB_SAFE = 20
    KRB_PRIV = 21
    KRB_CRED = 22
    KRB_ERROR = 30


class EncryptionType(enum.Enum):
    NULL = 0
    DES_CBC_CRC = 1
    DES_CBC_MD4 = 2
    DES_CBC_MD5 = 3
    DES3_CBC_MD5 = 5
    OLD_DES3_CBC_SHA1 = 7
    SIGN_DSA_GENERATE = 8
    ENCRYPT_RSA_PRIV = 9
    ENCRYPT_RSA_PUB = 10
    DES3_CBC_SHA1 = 16
    AES128_CTS_HMAC_SHA1_96 = 17
    AES256_CTS_HMAC_SHA1_96 = 18
    ARCFOUR_HMAC_MD5 = 23
    ARCFOUR_HMAC_MD5_56 = 24
    ENCTYPE_PK_CROSS = 48
    ARCFOUR_MD4 = -128
    ARCFOUR_HMAC_OLD = -133
    ARCFOUR_HMAC_OLD_EXP = -135
    DES_CBC_NONE = -4096
    DES3_CBC_NONE = -4097
    DES_CFB64_NONE = -4098
    DES_PCBC_NONE = -4099
    DIGEST_MD5_NONE = -4100
    CRAM_MD5_NONE = -4101


class PaDataType(enum.Enum):
    NONE = 0
    TGS_REQ = 1
    AP_REQ = 1
    ENC_TIMESTAMP = 2
    PW_SALT = 3
    ENC_UNIX_TIME = 5
    SANDIA_SECUREID = 6
    SESAME = 7
    OSF_DCE = 8
    CYBERSAFE_SECUREID = 9
    AFS3_SALT = 10
    ETYPE_INFO = 11
    SAM_CHALLENGE = 12
    SAM_RESPONSE = 13
    PK_AS_REQ_19 = 14
    PK_AS_REP_19 = 15
    PK_AS_REQ_WIN = 15
    PK_AS_REQ = 16
    PK_AS_REP = 17
    PA_PK_OCSP_RESPONSE = 18
    ETYPE_INFO2 = 19
    USE_SPECIFIED_KVNO = 20
    SVR_REFERRAL_INFO = 20
    SAM_REDIRECT = 21
    GET_FROM_TYPED_DATA = 22
    SAM_ETYPE_INFO = 23
    SERVER_REFERRAL = 25
    ALT_PRINC = 24
    SAM_CHALLENGE2 = 30
    SAM_RESPONSE2 = 31
    PA_EXTRA_TGT = 41
    TD_KRB_PRINCIPAL = 102
    PK_TD_TRUSTED_CERTIFIERS = 104
    PK_TD_CERTIFICATE_INDEX = 105
    TD_APP_DEFINED_ERROR = 106
    TD_REQ_NONCE = 107
    TD_REQ_SEQ = 108
    PA_PAC_REQUEST = 128
    FOR_USER = 129
    FOR_X509_USER = 130
    FOR_CHECK_DUPS = 131
    AS_CHECKSUM = 132
    PK_AS_09_BINDING = 132
    CLIENT_CANONICALIZED = 133
    FX_COOKIE = 133
    AUTHENTICATION_SET = 134
    AUTH_SET_SELECTED = 135
    FX_FAST = 136
    FX_ERROR = 137
    ENCRYPTED_CHALLENGE = 138
    OTP_CHALLENGE = 141
    OTP_REQUEST = 142
    OTP_CONFIRM = 143
    OTP_PIN_CHANGE = 144
    EPAK_AS_REQ = 145
    EPAK_AS_REP = 146
    PKINIT_KX = 147
    PKU2U_NAME = 148
    REQ_ENC_PA_REP = 149
    SUPPORTED_ETYPES = 165


class PADATA_TYPE(core.Enumerated):
    _map = {0:'NONE', 
     1:'TGS-REQ', 
     1:'AP-REQ', 
     2:'ENC-TIMESTAMP', 
     3:'PW-SALT', 
     5:'ENC-UNIX-TIME', 
     6:'SANDIA-SECUREID', 
     7:'SESAME', 
     8:'OSF-DCE', 
     9:'CYBERSAFE-SECUREID', 
     10:'AFS3-SALT', 
     11:'ETYPE-INFO', 
     12:'SAM-CHALLENGE', 
     13:'SAM-RESPONSE', 
     14:'PK-AS-REQ-19', 
     15:'PK-AS-REP-19', 
     15:'PK-AS-REQ-WIN', 
     16:'PK-AS-REQ', 
     17:'PK-AS-REP', 
     18:'PA-PK-OCSP-RESPONSE', 
     19:'ETYPE-INFO2', 
     20:'USE-SPECIFIED-KVNO', 
     20:'SVR-REFERRAL-INFO', 
     21:'SAM-REDIRECT', 
     22:'GET-FROM-TYPED-DATA', 
     23:'SAM-ETYPE-INFO', 
     25:'SERVER-REFERRAL', 
     24:'ALT-PRINC', 
     30:'SAM-CHALLENGE2', 
     31:'SAM-RESPONSE2', 
     41:'PA-EXTRA-TGT', 
     102:'TD-KRB-PRINCIPAL', 
     104:'PK-TD-TRUSTED-CERTIFIERS', 
     105:'PK-TD-CERTIFICATE-INDEX', 
     106:'TD-APP-DEFINED-ERROR', 
     107:'TD-REQ-NONCE', 
     108:'TD-REQ-SEQ', 
     128:'PA-PAC-REQUEST', 
     129:'FOR-USER', 
     130:'FOR-X509-USER', 
     131:'FOR-CHECK-DUPS', 
     132:'AS-CHECKSUM', 
     132:'PK-AS-09-BINDING', 
     133:'CLIENT-CANONICALIZED', 
     133:'FX-COOKIE', 
     134:'AUTHENTICATION-SET', 
     135:'AUTH-SET-SELECTED', 
     136:'FX-FAST', 
     137:'FX-ERROR', 
     138:'ENCRYPTED-CHALLENGE', 
     141:'OTP-CHALLENGE', 
     142:'OTP-REQUEST', 
     143:'OTP-CONFIRM', 
     144:'OTP-PIN-CHANGE', 
     145:'EPAK-AS-REQ', 
     146:'EPAK-AS-REP', 
     147:'PKINIT-KX', 
     148:'PKU2U-NAME', 
     149:'REQ-ENC-PA-REP', 
     165:'SUPPORTED-ETYPES'}


class AUTHDATA_TYPE(core.Enumerated):
    _map = {1:'IF-RELEVANT', 
     2:'INTENDED-FOR_SERVER', 
     3:'INTENDED-FOR-APPLICATION-CLASS', 
     4:'KDC-ISSUED', 
     5:'AND-OR', 
     6:'MANDATORY-TICKET-EXTENSIONS', 
     7:'IN-TICKET-EXTENSIONS', 
     8:'MANDATORY-FOR-KDC', 
     9:'INITIAL-VERIFIED-CAS', 
     64:'OSF-DCE', 
     65:'SESAME', 
     66:'OSF-DCE-PKI-CERTID', 
     128:'WIN2K-PAC', 
     129:'GSS-API-ETYPE-NEGOTIATION', 
     -17:'SIGNTICKET-OLDER', 
     142:'SIGNTICKET-OLD', 
     512:'SIGNTICKET'}


class CKSUMTYPE(core.Enumerated):
    _map = {0:'NONE', 
     1:'CRC32', 
     2:'RSA_MD4', 
     3:'RSA_MD4_DES', 
     4:'DES_MAC', 
     5:'DES_MAC_K', 
     6:'RSA_MD4_DES_K', 
     7:'RSA_MD5', 
     8:'RSA_MD5_DES', 
     9:'RSA_MD5_DES3', 
     10:'SHA1_OTHER', 
     12:'HMAC_SHA1_DES3', 
     14:'SHA1', 
     15:'HMAC_SHA1_96_AES_128', 
     16:'HMAC_SHA1_96_AES_256', 
     32771:'GSSAPI', 
     -138:'HMAC_MD5', 
     -1138:'HMAC_MD5_ENC'}


class ENCTYPE(core.Enumerated):
    _map = {0:'NULL', 
     1:'DES_CBC_CRC', 
     2:'DES_CBC_MD4', 
     3:'DES_CBC_MD5', 
     5:'DES3_CBC_MD5', 
     7:'OLD_DES3_CBC_SHA1', 
     8:'SIGN_DSA_GENERATE', 
     9:'ENCRYPT_RSA_PRIV', 
     10:'ENCRYPT_RSA_PUB', 
     16:'DES3_CBC_SHA1', 
     17:'AES128_CTS_HMAC_SHA1_96', 
     18:'AES256_CTS_HMAC_SHA1_96', 
     23:'ARCFOUR_HMAC_MD5', 
     24:'ARCFOUR_HMAC_MD5_56', 
     48:'ENCTYPE_PK_CROSS', 
     -128:'ARCFOUR_MD4', 
     -133:'ARCFOUR_HMAC_OLD', 
     -135:'ARCFOUR_HMAC_OLD_EXP', 
     -4096:'DES_CBC_NONE', 
     -4097:'DES3_CBC_NONE', 
     -4098:'DES_CFB64_NONE', 
     -4099:'DES_PCBC_NONE', 
     -4100:'DIGEST_MD5_NONE', 
     -4101:'CRAM_MD5_NONE'}


class SequenceOfEnctype(core.SequenceOf):
    _child_spec = core.Integer


class Microseconds(core.Integer):
    __doc__ = '    ::= INTEGER (0..999999)\n\t-- microseconds\n    '


class krb5int32(core.Integer):
    __doc__ = 'krb5int32  ::= INTEGER (-2147483648..2147483647)\n    '


class krb5uint32(core.Integer):
    __doc__ = 'krb5uint32  ::= INTEGER (0..4294967295)\n    '


class KerberosString(core.GeneralString):
    __doc__ = 'KerberosString ::= GeneralString (IA5String)\n\tFor compatibility, implementations MAY choose to accept GeneralString\n\tvalues that contain characters other than those permitted by\n\tIA5String...\n\t'


class SequenceOfKerberosString(core.SequenceOf):
    _child_spec = KerberosString


class Realm(KerberosString):
    __doc__ = 'Realm ::= KerberosString\n\t'


class PrincipalName(core.Sequence):
    __doc__ = 'PrincipalName for KDC-REQ-BODY and Ticket\n\tPrincipalName ::= SEQUENCE {\n\t\tname-type\t[0] Int32,\n\t\tname-string  [1] SEQUENCE OF KerberosString\n\t}\n\t'
    _fields = [
     (
      'name-type', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'name-string', SequenceOfKerberosString, {'tag_type':TAG,  'tag':1})]


class Principal(core.Sequence):
    _fields = [
     (
      'name', PrincipalName, {'tag_type':TAG,  'tag':0}),
     (
      'realm', Realm, {'tag_type':TAG,  'tag':1})]


class Principals(core.SequenceOf):
    _child_spec = Principal


class HostAddress(core.Sequence):
    __doc__ = 'HostAddress for HostAddresses\n    HostAddress ::= SEQUENCE {\n        addr-type        [0] Int32,\n        address  [1] OCTET STRING\n    }\n    '
    _fields = [
     (
      'addr-type', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'address', core.OctetString, {'tag_type':TAG,  'tag':1})]


class HostAddresses(core.SequenceOf):
    __doc__ = 'SEQUENCE OF HostAddress\n\t'
    _child_spec = HostAddress


class KerberosTime(core.GeneralizedTime):
    __doc__ = 'KerberosTime ::= GeneralizedTime\n    '


class AuthorizationDataElement(core.SequenceOf):
    _fields = [
     (
      'ad-type', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'ad-data', core.OctetString, {'tag_type':TAG,  'tag':1})]


class AuthorizationData(core.SequenceOf):
    __doc__ = 'SEQUENCE OF HostAddress\n\t'
    _child_spec = AuthorizationDataElement


class APOptions(core.BitString):
    _map = {0:'reserved', 
     1:'use-session-key', 
     2:'mutual-required'}


class TicketFlags(core.BitString):
    _map = {0:'reserved', 
     1:'forwardable', 
     2:'forwarded', 
     3:'proxiable', 
     4:'proxy', 
     5:'may-postdate', 
     6:'postdated', 
     7:'invalid', 
     8:'renewable', 
     9:'initial', 
     10:'pre-authent', 
     11:'hw-authent', 
     12:'transited-policy-checked', 
     13:'ok-as-delegate', 
     14:'anonymous', 
     15:'enc-pa-rep'}


class KDCOptions(core.BitString):
    _map = {0:'reserved', 
     1:'forwardable', 
     2:'forwarded', 
     3:'proxiable', 
     4:'proxy', 
     5:'allow-postdate', 
     6:'postdated', 
     7:'unused7', 
     8:'renewable', 
     9:'unused9', 
     10:'unused10', 
     11:'opt-hardware-auth', 
     12:'unused12', 
     13:'unused13', 
     14:'constrained-delegation', 
     15:'canonicalize', 
     16:'request-anonymous', 
     17:'unused17', 
     18:'unused18', 
     19:'unused19', 
     20:'unused20', 
     21:'unused21', 
     22:'unused22', 
     23:'unused23', 
     24:'unused24', 
     25:'unused25', 
     26:'disable-transited-check', 
     27:'renewable-ok', 
     28:'enc-tkt-in-skey', 
     30:'renew', 
     31:'validate'}


class LR_TYPE(core.Enumerated):
    _map = {0:'NONE', 
     1:'INITIAL_TGT', 
     2:'INITIAL', 
     3:'ISSUE_USE_TGT', 
     4:'RENEWAL', 
     5:'REQUEST', 
     6:'PW_EXPTIME', 
     7:'ACCT_EXPTIME'}


class LastReqInner(core.Sequence):
    _fields = [
     (
      'lr-type', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'lr-value', KerberosTime, {'tag_type':TAG,  'tag':1})]


class LastReq(core.SequenceOf):
    _child_spec = LastReqInner


class EncryptedData(core.Sequence):
    _fields = [
     (
      'etype', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'kvno', krb5uint32, {'tag_type':TAG,  'tag':1,  'optional':True}),
     (
      'cipher', core.OctetString, {'tag_type':TAG,  'tag':2})]


class EncryptionKey(core.Sequence):
    _fields = [
     (
      'keytype', krb5uint32, {'tag_type':TAG,  'tag':0}),
     (
      'keyvalue', core.OctetString, {'tag_type':TAG,  'tag':1})]


class TransitedEncoding(core.Sequence):
    _fields = [
     (
      'tr-type', krb5uint32, {'tag_type':TAG,  'tag':0}),
     (
      'contents', core.OctetString, {'tag_type':TAG,  'tag':1})]


class Ticket(core.Sequence):
    explicit = (
     APPLICATION, 1)
    _fields = [
     (
      'tkt-vno', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'realm', Realm, {'tag_type':TAG,  'tag':1}),
     (
      'sname', PrincipalName, {'tag_type':TAG,  'tag':2}),
     (
      'enc-part', EncryptedData, {'tag_type':TAG,  'tag':3})]


class SequenceOfTicket(core.SequenceOf):
    __doc__ = 'SEQUENCE OF Ticket for KDC-REQ-BODY\n\t'
    _child_spec = Ticket


class EncTicketPart(core.Sequence):
    explicit = (
     APPLICATION, 3)
    _fields = [
     (
      'flags', TicketFlags, {'tag_type':TAG,  'tag':0}),
     (
      'key', EncryptionKey, {'tag_type':TAG,  'tag':1}),
     (
      'crealm', Realm, {'tag_type':TAG,  'tag':2}),
     (
      'cname', PrincipalName, {'tag_type':TAG,  'tag':3}),
     (
      'transited', TransitedEncoding, {'tag_type':TAG,  'tag':4}),
     (
      'authtime', KerberosTime, {'tag_type':TAG,  'tag':5}),
     (
      'starttime', KerberosTime, {'tag_type':TAG,  'tag':6,  'optional':True}),
     (
      'endtime', KerberosTime, {'tag_type':TAG,  'tag':7}),
     (
      'renew-till', KerberosTime, {'tag_type':TAG,  'tag':8,  'optional':True}),
     (
      'caddr', HostAddresses, {'tag_type':TAG,  'tag':9,  'optional':True}),
     (
      'authorization-data', AuthorizationData, {'tag_type':TAG,  'tag':10,  'optional':True})]


class Checksum(core.Sequence):
    _fields = [
     (
      'cksumtype', CKSUMTYPE, {'tag_type':TAG,  'tag':0}),
     (
      'checksum', core.OctetString, {'tag_type':TAG,  'tag':1})]


class Authenticator(core.Sequence):
    explicit = (
     APPLICATION, 2)
    _fields = [
     (
      'authenticator-vno', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'crealm', Realm, {'tag_type':TAG,  'tag':1}),
     (
      'cname', PrincipalName, {'tag_type':TAG,  'tag':2}),
     (
      'cksum', Checksum, {'tag_type':TAG,  'tag':3,  'optional':True}),
     (
      'cusec', krb5int32, {'tag_type':TAG,  'tag':4}),
     (
      'ctime', KerberosTime, {'tag_type':TAG,  'tag':5}),
     (
      'subkey', EncryptionKey, {'tag_type':TAG,  'tag':6,  'optional':True}),
     (
      'seq-number', krb5uint32, {'tag_type':TAG,  'tag':7,  'optional':True}),
     (
      'authorization-data', AuthorizationData, {'tag_type':TAG,  'tag':8,  'optional':True})]


class PA_DATA(core.Sequence):
    _fields = [
     (
      'padata-type', core.Integer, {'tag_type':TAG,  'tag':1}),
     (
      'padata-value', core.OctetString, {'tag_type':TAG,  'tag':2})]


class ETYPE_INFO_ENTRY(core.Sequence):
    _fields = [
     (
      'etype', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'salt', core.OctetString, {'tag_type':TAG,  'tag':1,  'optional':True}),
     (
      'salttype', krb5int32, {'tag_type':TAG,  'tag':2,  'optional':True})]


class ETYPE_INFO(core.SequenceOf):
    _child_spec = ETYPE_INFO_ENTRY


class ETYPE_INFO2_ENTRY(core.Sequence):
    _fields = [
     (
      'etype', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'salt', KerberosString, {'tag_type':TAG,  'tag':1,  'optional':True}),
     (
      's2kparams', core.OctetString, {'tag_type':TAG,  'tag':2,  'optional':True})]


class ETYPE_INFO2(core.SequenceOf):
    _child_spec = ETYPE_INFO2_ENTRY


class METHOD_DATA(core.SequenceOf):
    _child_spec = PA_DATA


class TypedData(core.Sequence):
    _fields = [
     (
      'data-type', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'data-value', core.OctetString, {'tag_type':TAG,  'tag':1,  'optional':True})]


class KDC_REQ_BODY(core.Sequence):
    _fields = [
     (
      'kdc-options', KDCOptions, {'tag_type':TAG,  'tag':0}),
     (
      'cname', PrincipalName, {'tag_type':TAG,  'tag':1,  'optional':True}),
     (
      'realm', Realm, {'tag_type':TAG,  'tag':2}),
     (
      'sname', PrincipalName, {'tag_type':TAG,  'tag':3,  'optional':True}),
     (
      'from', KerberosTime, {'tag_type':TAG,  'tag':4,  'optional':True}),
     (
      'till', KerberosTime, {'tag_type':TAG,  'tag':5,  'optional':True}),
     (
      'rtime', KerberosTime, {'tag_type':TAG,  'tag':6,  'optional':True}),
     (
      'nonce', krb5int32, {'tag_type':TAG,  'tag':7}),
     (
      'etype', SequenceOfEnctype, {'tag_type':TAG,  'tag':8}),
     (
      'addresses', HostAddresses, {'tag_type':TAG,  'tag':9,  'optional':True}),
     (
      'enc-authorization-data', EncryptedData, {'tag_type':TAG,  'tag':10,  'optional':True}),
     (
      'additional-tickets', SequenceOfTicket, {'tag_type':TAG,  'tag':11,  'optional':True})]


class KDC_REQ(core.Sequence):
    _fields = [
     (
      'pvno', krb5int32, {'tag_type':TAG,  'tag':1}),
     (
      'msg-type', krb5int32, {'tag_type':TAG,  'tag':2}),
     (
      'padata', METHOD_DATA, {'tag_type':TAG,  'tag':3,  'optional':True}),
     (
      'req-body', KDC_REQ_BODY, {'tag_type':TAG,  'tag':4})]


class AS_REQ(KDC_REQ):
    explicit = (
     APPLICATION, 10)


class TGS_REQ(KDC_REQ):
    explicit = (
     APPLICATION, 12)


class PA_ENC_TS_ENC(core.Sequence):
    _fields = [
     (
      'patimestamp', KerberosTime, {'tag_type':TAG,  'tag':0}),
     (
      'pausec', krb5int32, {'tag_type':TAG,  'tag':1,  'optional':True})]


class PA_PAC_REQUEST(core.Sequence):
    _fields = [
     (
      'include-pac', core.Boolean, {'tag_type':TAG,  'tag':0})]


class PROV_SRV_LOCATION(core.GeneralString):
    pass


class KDC_REP(core.Sequence):
    _fields = [
     (
      'pvno', core.Integer, {'tag_type':TAG,  'tag':0}),
     (
      'msg-type', krb5int32, {'tag_type':TAG,  'tag':1}),
     (
      'padata', METHOD_DATA, {'tag_type':TAG,  'tag':2,  'optional':True}),
     (
      'crealm', Realm, {'tag_type':TAG,  'tag':3}),
     (
      'cname', PrincipalName, {'tag_type':TAG,  'tag':4}),
     (
      'ticket', Ticket, {'tag_type':TAG,  'tag':5}),
     (
      'enc-part', EncryptedData, {'tag_type':TAG,  'tag':6})]


class AS_REP(KDC_REP):
    explicit = (
     APPLICATION, 11)


class TGS_REP(KDC_REP):
    explicit = (
     APPLICATION, 13)


class EncKDCRepPart(core.Sequence):
    _fields = [
     (
      'key', EncryptionKey, {'tag_type':TAG,  'tag':0}),
     (
      'last-req', LastReq, {'tag_type':TAG,  'tag':1}),
     (
      'nonce', krb5int32, {'tag_type':TAG,  'tag':2}),
     (
      'key-expiration', KerberosTime, {'tag_type':TAG,  'tag':3,  'optional':True}),
     (
      'flags', TicketFlags, {'tag_type':TAG,  'tag':4}),
     (
      'authtime', KerberosTime, {'tag_type':TAG,  'tag':5}),
     (
      'starttime', KerberosTime, {'tag_type':TAG,  'tag':6,  'optional':True}),
     (
      'endtime', KerberosTime, {'tag_type':TAG,  'tag':7}),
     (
      'renew-till', KerberosTime, {'tag_type':TAG,  'tag':8,  'optional':True}),
     (
      'srealm', Realm, {'tag_type':TAG,  'tag':9}),
     (
      'sname', PrincipalName, {'tag_type':TAG,  'tag':10}),
     (
      'caddr', HostAddresses, {'tag_type':TAG,  'tag':11,  'optional':True}),
     (
      'encrypted-pa-data', METHOD_DATA, {'tag_type':TAG,  'tag':12,  'optional':True})]


class EncASRepPart(EncKDCRepPart):
    explicit = (
     APPLICATION, 25)


class EncTGSRepPart(EncKDCRepPart):
    explicit = (
     APPLICATION, 26)


class AP_REQ(core.Sequence):
    explicit = (
     APPLICATION, 14)
    _fields = [
     (
      'pvno', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'msg-type', krb5int32, {'tag_type':TAG,  'tag':1}),
     (
      'ap-options', APOptions, {'tag_type':TAG,  'tag':2}),
     (
      'ticket', Ticket, {'tag_type':TAG,  'tag':3}),
     (
      'authenticator', EncryptedData, {'tag_type':TAG,  'tag':4})]


class AP_REP(core.Sequence):
    explicit = (
     APPLICATION, 15)
    _fields = [
     (
      'pvno', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'msg-type', krb5int32, {'tag_type':TAG,  'tag':1}),
     (
      'enc-part', EncryptedData, {'tag_type':TAG,  'tag':2})]


class EncAPRepPart(core.Sequence):
    explicit = (
     APPLICATION, 27)
    _fields = [
     (
      'ctime', KerberosTime, {'tag_type':TAG,  'tag':0}),
     (
      'cusec', krb5int32, {'tag_type':TAG,  'tag':1}),
     (
      'subkey', EncryptionKey, {'tag_type':TAG,  'tag':2}),
     (
      'seq-number', krb5uint32, {'tag_type':TAG,  'tag':3,  'optional':True})]


class KRB_SAFE_BODY(core.Sequence):
    _fields = [
     (
      'user-data', core.OctetString, {'tag_type':TAG,  'tag':0}),
     (
      'timestamp', KerberosTime, {'tag_type':TAG,  'tag':1,  'optional':True}),
     (
      'usec', krb5int32, {'tag_type':TAG,  'tag':2,  'optional':True}),
     (
      'seq-number', krb5uint32, {'tag_type':TAG,  'tag':3,  'optional':True}),
     (
      's-address', HostAddress, {'tag_type':TAG,  'tag':4,  'optional':True}),
     (
      'r-address', HostAddress, {'tag_type':TAG,  'tag':5,  'optional':True})]


class KRB_SAFE(core.Sequence):
    explicit = (
     APPLICATION, 20)
    _fields = [
     (
      'pvno', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'msg-type', krb5int32, {'tag_type':TAG,  'tag':1}),
     (
      'safe-body', KRB_SAFE_BODY, {'tag_type':TAG,  'tag':2}),
     (
      'cksum', Checksum, {'tag_type':TAG,  'tag':3})]


class KRB_PRIV(core.Sequence):
    explicit = (
     APPLICATION, 21)
    _fields = [
     (
      'pvno', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'msg-type', krb5int32, {'tag_type':TAG,  'tag':1}),
     (
      'enc-part', EncryptedData, {'tag_type':TAG,  'tag':2})]


class EncKrbPrivPart(core.Sequence):
    explicit = (
     APPLICATION, 28)
    _fields = [
     (
      'user-data', core.OctetString, {'tag_type':TAG,  'tag':0}),
     (
      'timestamp', KerberosTime, {'tag_type':TAG,  'tag':1,  'optional':True}),
     (
      'usec', krb5int32, {'tag_type':TAG,  'tag':2,  'optional':True}),
     (
      'seq-number', krb5uint32, {'tag_type':TAG,  'tag':3,  'optional':True}),
     (
      's-address', HostAddress, {'tag_type':TAG,  'tag':4,  'optional':True}),
     (
      'r-address', HostAddress, {'tag_type':TAG,  'tag':5,  'optional':True})]


class KRB_CRED(core.Sequence):
    explicit = (
     APPLICATION, 22)
    _fields = [
     (
      'pvno', core.Integer, {'tag_type':TAG,  'tag':0}),
     (
      'msg-type', core.Integer, {'tag_type':TAG,  'tag':1}),
     (
      'tickets', SequenceOfTicket, {'tag_type':TAG,  'tag':2}),
     (
      'enc-part', EncryptedData, {'tag_type':TAG,  'tag':3})]


class KrbCredInfo(core.Sequence):
    _fields = [
     (
      'key', EncryptionKey, {'tag_type':TAG,  'tag':0}),
     (
      'prealm', Realm, {'tag_type':TAG,  'tag':1,  'optional':True}),
     (
      'pname', PrincipalName, {'tag_type':TAG,  'tag':2,  'optional':True}),
     (
      'flags', TicketFlags, {'tag_type':TAG,  'tag':3,  'optional':True}),
     (
      'authtime', KerberosTime, {'tag_type':TAG,  'tag':4,  'optional':True}),
     (
      'starttime', KerberosTime, {'tag_type':TAG,  'tag':5,  'optional':True}),
     (
      'endtime', KerberosTime, {'tag_type':TAG,  'tag':6,  'optional':True}),
     (
      'renew-till', KerberosTime, {'tag_type':TAG,  'tag':7,  'optional':True}),
     (
      'srealm', Realm, {'tag_type':TAG,  'tag':8,  'optional':True}),
     (
      'sname', PrincipalName, {'tag_type':TAG,  'tag':9,  'optional':True}),
     (
      'caddr', HostAddresses, {'tag_type':TAG,  'tag':10,  'optional':True})]


class SequenceOfKrbCredInfo(core.SequenceOf):
    _child_spec = KrbCredInfo


class EncKrbCredPart(core.Sequence):
    explicit = (
     APPLICATION, 29)
    _fields = [
     (
      'ticket-info', SequenceOfKrbCredInfo, {'tag_type':TAG,  'tag':0}),
     (
      'nonce', krb5int32, {'tag_type':TAG,  'tag':1,  'optional':True}),
     (
      'timestamp', KerberosTime, {'tag_type':TAG,  'tag':2,  'optional':True}),
     (
      'usec', krb5int32, {'tag_type':TAG,  'tag':3,  'optional':True}),
     (
      's-address', HostAddress, {'tag_type':TAG,  'tag':4,  'optional':True}),
     (
      'r-address', HostAddress, {'tag_type':TAG,  'tag':5,  'optional':True})]


class KRB_ERROR(core.Sequence):
    explicit = (
     APPLICATION, 30)
    _fields = [
     (
      'pvno', krb5int32, {'tag_type':TAG,  'tag':0}),
     (
      'msg-type', krb5int32, {'tag_type':TAG,  'tag':1}),
     (
      'ctime', KerberosTime, {'tag_type':TAG,  'tag':2,  'optional':True}),
     (
      'cusec', krb5int32, {'tag_type':TAG,  'tag':3,  'optional':True}),
     (
      'stime', KerberosTime, {'tag_type':TAG,  'tag':4}),
     (
      'susec', krb5int32, {'tag_type':TAG,  'tag':5}),
     (
      'error-code', krb5int32, {'tag_type':TAG,  'tag':6}),
     (
      'crealm', Realm, {'tag_type':TAG,  'tag':7,  'optional':True}),
     (
      'cname', PrincipalName, {'tag_type':TAG,  'tag':8,  'optional':True}),
     (
      'realm', Realm, {'tag_type':TAG,  'tag':9}),
     (
      'sname', PrincipalName, {'tag_type':TAG,  'tag':10}),
     (
      'e-text', core.GeneralString, {'tag_type':TAG,  'tag':11,  'optional':True}),
     (
      'e-data', core.OctetString, {'tag_type':TAG,  'tag':12,  'optional':True})]


class ChangePasswdDataMS(core.Sequence):
    _fields = [
     (
      'newpasswd', core.OctetString, {'tag_type':TAG,  'tag':0}),
     (
      'targname', PrincipalName, {'tag_type':TAG,  'tag':1,  'optional':True}),
     (
      'targrealm', Realm, {'tag_type':TAG,  'tag':2,  'optional':True})]


class EtypeList(core.SequenceOf):
    _child_spec = ENCTYPE


class KerberosResponse(core.Choice):
    _alternatives = [
     (
      'AS_REP', AS_REP, {'implicit': (APPLICATION, 11)}),
     (
      'TGS_REP', TGS_REP, {'implicit': (APPLICATION, 13)}),
     (
      'KRB_ERROR', KRB_ERROR, {'implicit': (APPLICATION, 30)})]


class KRBCRED(core.Sequence):
    explicit = (
     APPLICATION, 22)
    _fields = [
     (
      'pvno', core.Integer, {'tag_type':TAG,  'tag':0}),
     (
      'msg-type', core.Integer, {'tag_type':TAG,  'tag':1}),
     (
      'tickets', SequenceOfTicket, {'tag_type':TAG,  'tag':2}),
     (
      'enc-part', EncryptedData, {'tag_type':TAG,  'tag':3})]


class KerberosParser:

    def __init__(self):
        pass

    @staticmethod
    async def from_streamreader(reader):
        lb = await read_or_exc(reader, 4)
        length = int.from_bytes(lb, byteorder='big', signed=False)
        data = await read_or_exc(reader, length)
        krb_message = AS_REQ.load(data)
        return krb_message