# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\__init__.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
from types import GeneratorType
ANONYMOUS = 'ANONYMOUS'
SIMPLE = 'SIMPLE'
SASL = 'SASL'
NTLM = 'NTLM'
EXTERNAL = 'EXTERNAL'
DIGEST_MD5 = 'DIGEST-MD5'
KERBEROS = GSSAPI = 'GSSAPI'
PLAIN = 'PLAIN'
AUTO_BIND_DEFAULT = 'DEFAULT'
AUTO_BIND_NONE = 'NONE'
AUTO_BIND_NO_TLS = 'NO_TLS'
AUTO_BIND_TLS_BEFORE_BIND = 'TLS_BEFORE_BIND'
AUTO_BIND_TLS_AFTER_BIND = 'TLS_AFTER_BIND'
IP_SYSTEM_DEFAULT = 'IP_SYSTEM_DEFAULT'
IP_V4_ONLY = 'IP_V4_ONLY'
IP_V6_ONLY = 'IP_V6_ONLY'
IP_V4_PREFERRED = 'IP_V4_PREFERRED'
IP_V6_PREFERRED = 'IP_V6_PREFERRED'
BASE = 'BASE'
LEVEL = 'LEVEL'
SUBTREE = 'SUBTREE'
DEREF_NEVER = 'NEVER'
DEREF_SEARCH = 'SEARCH'
DEREF_BASE = 'FINDING_BASE'
DEREF_ALWAYS = 'ALWAYS'
ALL_ATTRIBUTES = '*'
NO_ATTRIBUTES = '1.1'
ALL_OPERATIONAL_ATTRIBUTES = '+'
MODIFY_ADD = 'MODIFY_ADD'
MODIFY_DELETE = 'MODIFY_DELETE'
MODIFY_REPLACE = 'MODIFY_REPLACE'
MODIFY_INCREMENT = 'MODIFY_INCREMENT'
SYNC = 'SYNC'
ASYNC = 'ASYNC'
LDIF = 'LDIF'
RESTARTABLE = 'RESTARTABLE'
REUSABLE = 'REUSABLE'
MOCK_SYNC = 'MOCK_SYNC'
MOCK_ASYNC = 'MOCK_ASYNC'
ASYNC_STREAM = 'ASYNC_STREAM'
NONE = 'NO_INFO'
DSA = 'DSA'
SCHEMA = 'SCHEMA'
ALL = 'ALL'
OFFLINE_EDIR_8_8_8 = 'EDIR_8_8_8'
OFFLINE_EDIR_9_1_4 = 'EDIR_9_1_4'
OFFLINE_AD_2012_R2 = 'AD_2012_R2'
OFFLINE_SLAPD_2_4 = 'SLAPD_2_4'
OFFLINE_DS389_1_3_3 = 'DS389_1_3_3'
FIRST = 'FIRST'
ROUND_ROBIN = 'ROUND_ROBIN'
RANDOM = 'RANDOM'
HASHED_NONE = 'PLAIN'
HASHED_SHA = 'SHA'
HASHED_SHA256 = 'SHA256'
HASHED_SHA384 = 'SHA384'
HASHED_SHA512 = 'SHA512'
HASHED_MD5 = 'MD5'
HASHED_SALTED_SHA = 'SALTED_SHA'
HASHED_SALTED_SHA256 = 'SALTED_SHA256'
HASHED_SALTED_SHA384 = 'SALTED_SHA384'
HASHED_SALTED_SHA512 = 'SALTED_SHA512'
HASHED_SALTED_MD5 = 'SALTED_MD5'
if str is not bytes:
    NUMERIC_TYPES = (
     int, float)
    INTEGER_TYPES = (int,)
else:
    NUMERIC_TYPES = (
     int, long, float)
    INTEGER_TYPES = (int, long)
if str is not bytes:
    STRING_TYPES = (
     str,)
    SEQUENCE_TYPES = (set, list, tuple, GeneratorType, type(dict().keys()))
else:
    try:
        from future.types.newstr import newstr
    except ImportError:
        pass

    STRING_TYPES = (
     str, unicode)
    SEQUENCE_TYPES = (set, list, tuple, GeneratorType)
from .version import __author__, __version__, __email__, __description__, __status__, __license__, __url__
from .utils.config import get_config_parameter, set_config_parameter
from .core.server import Server
from .core.connection import Connection
from .core.tls import Tls
from .core.pooling import ServerPool
from .abstract.objectDef import ObjectDef
from .abstract.attrDef import AttrDef
from .abstract.attribute import Attribute, WritableAttribute, OperationalAttribute
from .abstract.entry import Entry, WritableEntry
from .abstract.cursor import Reader, Writer
from .protocol.rfc4512 import DsaInfo, SchemaInfo