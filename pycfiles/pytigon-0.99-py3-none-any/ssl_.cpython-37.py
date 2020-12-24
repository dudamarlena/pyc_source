# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/urllib3/urllib3/util/ssl_.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 14511 bytes
from __future__ import absolute_import
import errno, warnings, hmac, sys
from binascii import hexlify, unhexlify
from hashlib import md5, sha1, sha256
from .url import IPV4_RE, BRACELESS_IPV6_ADDRZ_RE
from ..exceptions import SSLError, InsecurePlatformWarning, SNIMissingWarning
from ..packages import six
SSLContext = None
HAS_SNI = False
IS_PYOPENSSL = False
IS_SECURETRANSPORT = False
HASHFUNC_MAP = {32:md5, 
 40:sha1,  64:sha256}

def _const_compare_digest_backport(a, b):
    """
    Compare two digests of equal length in constant time.

    The digests must be of type str/bytes.
    Returns True if the digests match, and False otherwise.
    """
    result = abs(len(a) - len(b))
    for l, r in zip(bytearray(a), bytearray(b)):
        result |= l ^ r

    return result == 0


_const_compare_digest = getattr(hmac, 'compare_digest', _const_compare_digest_backport)
try:
    import ssl
    from ssl import wrap_socket, CERT_REQUIRED
    from ssl import HAS_SNI
except ImportError:
    pass

try:
    from ssl import PROTOCOL_TLS
    PROTOCOL_SSLv23 = PROTOCOL_TLS
except ImportError:
    try:
        from ssl import PROTOCOL_SSLv23 as PROTOCOL_TLS
        PROTOCOL_SSLv23 = PROTOCOL_TLS
    except ImportError:
        PROTOCOL_SSLv23 = PROTOCOL_TLS = 2

try:
    from ssl import OP_NO_SSLv2, OP_NO_SSLv3, OP_NO_COMPRESSION
except ImportError:
    OP_NO_SSLv2, OP_NO_SSLv3 = (16777216, 33554432)
    OP_NO_COMPRESSION = 131072

DEFAULT_CIPHERS = ':'.join([
 'ECDHE+AESGCM',
 'ECDHE+CHACHA20',
 'DHE+AESGCM',
 'DHE+CHACHA20',
 'ECDH+AESGCM',
 'DH+AESGCM',
 'ECDH+AES',
 'DH+AES',
 'RSA+AESGCM',
 'RSA+AES',
 '!aNULL',
 '!eNULL',
 '!MD5',
 '!DSS'])
try:
    from ssl import SSLContext
except ImportError:

    class SSLContext(object):

        def __init__(self, protocol_version):
            self.protocol = protocol_version
            self.check_hostname = False
            self.verify_mode = ssl.CERT_NONE
            self.ca_certs = None
            self.options = 0
            self.certfile = None
            self.keyfile = None
            self.ciphers = None

        def load_cert_chain(self, certfile, keyfile):
            self.certfile = certfile
            self.keyfile = keyfile

        def load_verify_locations(self, cafile=None, capath=None, cadata=None):
            self.ca_certs = cafile
            if capath is not None:
                raise SSLError('CA directories not supported in older Pythons')
            if cadata is not None:
                raise SSLError('CA data not supported in older Pythons')

        def set_ciphers(self, cipher_suite):
            self.ciphers = cipher_suite

        def wrap_socket(self, socket, server_hostname=None, server_side=False):
            warnings.warn('A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings', InsecurePlatformWarning)
            kwargs = {'keyfile':self.keyfile, 
             'certfile':self.certfile, 
             'ca_certs':self.ca_certs, 
             'cert_reqs':self.verify_mode, 
             'ssl_version':self.protocol, 
             'server_side':server_side}
            return wrap_socket(socket, ciphers=self.ciphers, **kwargs)


def assert_fingerprint(cert, fingerprint):
    """
    Checks if given fingerprint matches the supplied certificate.

    :param cert:
        Certificate as bytes object.
    :param fingerprint:
        Fingerprint as string of hexdigits, can be interspersed by colons.
    """
    fingerprint = fingerprint.replace(':', '').lower()
    digest_length = len(fingerprint)
    hashfunc = HASHFUNC_MAP.get(digest_length)
    if not hashfunc:
        raise SSLError('Fingerprint of invalid length: {0}'.format(fingerprint))
    fingerprint_bytes = unhexlify(fingerprint.encode())
    cert_digest = hashfunc(cert).digest()
    if not _const_compare_digest(cert_digest, fingerprint_bytes):
        raise SSLError('Fingerprints did not match. Expected "{0}", got "{1}".'.format(fingerprint, hexlify(cert_digest)))


def resolve_cert_reqs(candidate):
    """
    Resolves the argument to a numeric constant, which can be passed to
    the wrap_socket function/method from the ssl module.
    Defaults to :data:`ssl.CERT_REQUIRED`.
    If given a string it is assumed to be the name of the constant in the
    :mod:`ssl` module or its abbreviation.
    (So you can specify `REQUIRED` instead of `CERT_REQUIRED`.
    If it's neither `None` nor a string we assume it is already the numeric
    constant which can directly be passed to wrap_socket.
    """
    if candidate is None:
        return CERT_REQUIRED
    if isinstance(candidate, str):
        res = getattr(ssl, candidate, None)
        if res is None:
            res = getattr(ssl, 'CERT_' + candidate)
        return res
    return candidate


def resolve_ssl_version(candidate):
    """
    like resolve_cert_reqs
    """
    if candidate is None:
        return PROTOCOL_TLS
    if isinstance(candidate, str):
        res = getattr(ssl, candidate, None)
        if res is None:
            res = getattr(ssl, 'PROTOCOL_' + candidate)
        return res
    return candidate


def create_urllib3_context(ssl_version=None, cert_reqs=None, options=None, ciphers=None):
    """All arguments have the same meaning as ``ssl_wrap_socket``.

    By default, this function does a lot of the same work that
    ``ssl.create_default_context`` does on Python 3.4+. It:

    - Disables SSLv2, SSLv3, and compression
    - Sets a restricted set of server ciphers

    If you wish to enable SSLv3, you can do::

        from urllib3.util import ssl_
        context = ssl_.create_urllib3_context()
        context.options &= ~ssl_.OP_NO_SSLv3

    You can do the same to enable compression (substituting ``COMPRESSION``
    for ``SSLv3`` in the last line above).

    :param ssl_version:
        The desired protocol version to use. This will default to
        PROTOCOL_SSLv23 which will negotiate the highest protocol that both
        the server and your installation of OpenSSL support.
    :param cert_reqs:
        Whether to require the certificate verification. This defaults to
        ``ssl.CERT_REQUIRED``.
    :param options:
        Specific OpenSSL options. These default to ``ssl.OP_NO_SSLv2``,
        ``ssl.OP_NO_SSLv3``, ``ssl.OP_NO_COMPRESSION``.
    :param ciphers:
        Which cipher suites to allow the server to select.
    :returns:
        Constructed SSLContext object with specified options
    :rtype: SSLContext
    """
    context = SSLContext(ssl_version or PROTOCOL_TLS)
    context.set_ciphers(ciphers or DEFAULT_CIPHERS)
    cert_reqs = ssl.CERT_REQUIRED if cert_reqs is None else cert_reqs
    if options is None:
        options = 0
        options |= OP_NO_SSLv2
        options |= OP_NO_SSLv3
        options |= OP_NO_COMPRESSION
    context.options |= options
    if cert_reqs == ssl.CERT_REQUIRED or sys.version_info >= (3, 7, 4):
        if getattr(context, 'post_handshake_auth', None) is not None:
            context.post_handshake_auth = True
    context.verify_mode = cert_reqs
    if getattr(context, 'check_hostname', None) is not None:
        context.check_hostname = False
    return context


def ssl_wrap_socket--- This code section failed: ---

 L. 334         0  LOAD_FAST                'ssl_context'
                2  STORE_FAST               'context'

 L. 335         4  LOAD_FAST                'context'
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L. 339        12  LOAD_GLOBAL              create_urllib3_context
               14  LOAD_FAST                'ssl_version'
               16  LOAD_FAST                'cert_reqs'
               18  LOAD_FAST                'ciphers'
               20  LOAD_CONST               ('ciphers',)
               22  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               24  STORE_FAST               'context'
             26_0  COME_FROM            10  '10'

 L. 341        26  LOAD_FAST                'ca_certs'
               28  POP_JUMP_IF_TRUE     38  'to 38'
               30  LOAD_FAST                'ca_cert_dir'
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  LOAD_FAST                'ca_cert_data'
               36  POP_JUMP_IF_FALSE   156  'to 156'
             38_0  COME_FROM            32  '32'
             38_1  COME_FROM            28  '28'

 L. 342        38  SETUP_EXCEPT         58  'to 58'

 L. 343        40  LOAD_FAST                'context'
               42  LOAD_METHOD              load_verify_locations
               44  LOAD_FAST                'ca_certs'
               46  LOAD_FAST                'ca_cert_dir'
               48  LOAD_FAST                'ca_cert_data'
               50  CALL_METHOD_3         3  '3 positional arguments'
               52  POP_TOP          
               54  POP_BLOCK        
               56  JUMP_ABSOLUTE       182  'to 182'
             58_0  COME_FROM_EXCEPT     38  '38'

 L. 344        58  DUP_TOP          
               60  LOAD_GLOBAL              IOError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    98  'to 98'
               66  POP_TOP          
               68  STORE_FAST               'e'
               70  POP_TOP          
               72  SETUP_FINALLY        86  'to 86'

 L. 345        74  LOAD_GLOBAL              SSLError
               76  LOAD_FAST                'e'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  RAISE_VARARGS_1       1  'exception instance'
               82  POP_BLOCK        
               84  LOAD_CONST               None
             86_0  COME_FROM_FINALLY    72  '72'
               86  LOAD_CONST               None
               88  STORE_FAST               'e'
               90  DELETE_FAST              'e'
               92  END_FINALLY      
               94  POP_EXCEPT       
               96  JUMP_ABSOLUTE       182  'to 182'
             98_0  COME_FROM            64  '64'

 L. 348        98  DUP_TOP          
              100  LOAD_GLOBAL              OSError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   152  'to 152'
              106  POP_TOP          
              108  STORE_FAST               'e'
              110  POP_TOP          
              112  SETUP_FINALLY       140  'to 140'

 L. 349       114  LOAD_FAST                'e'
              116  LOAD_ATTR                errno
              118  LOAD_GLOBAL              errno
              120  LOAD_ATTR                ENOENT
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   134  'to 134'

 L. 350       126  LOAD_GLOBAL              SSLError
              128  LOAD_FAST                'e'
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           124  '124'

 L. 351       134  RAISE_VARARGS_0       0  'reraise'
              136  POP_BLOCK        
              138  LOAD_CONST               None
            140_0  COME_FROM_FINALLY   112  '112'
              140  LOAD_CONST               None
              142  STORE_FAST               'e'
              144  DELETE_FAST              'e'
              146  END_FINALLY      
              148  POP_EXCEPT       
              150  JUMP_ABSOLUTE       182  'to 182'
            152_0  COME_FROM           104  '104'
              152  END_FINALLY      
              154  JUMP_FORWARD        182  'to 182'
            156_0  COME_FROM            36  '36'

 L. 353       156  LOAD_FAST                'ssl_context'
              158  LOAD_CONST               None
              160  COMPARE_OP               is
              162  POP_JUMP_IF_FALSE   182  'to 182'
              164  LOAD_GLOBAL              hasattr
              166  LOAD_FAST                'context'
              168  LOAD_STR                 'load_default_certs'
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  POP_JUMP_IF_FALSE   182  'to 182'

 L. 355       174  LOAD_FAST                'context'
              176  LOAD_METHOD              load_default_certs
              178  CALL_METHOD_0         0  '0 positional arguments'
              180  POP_TOP          
            182_0  COME_FROM_EXCEPT_CLAUSE   172  '172'
            182_1  COME_FROM_EXCEPT_CLAUSE   162  '162'
            182_2  COME_FROM_EXCEPT_CLAUSE   154  '154'
            182_3  COME_FROM_EXCEPT_CLAUSE    96  '96'

 L. 360       182  LOAD_FAST                'keyfile'
              184  POP_JUMP_IF_FALSE   210  'to 210'
              186  LOAD_FAST                'key_password'
              188  LOAD_CONST               None
              190  COMPARE_OP               is
              192  POP_JUMP_IF_FALSE   210  'to 210'
              194  LOAD_GLOBAL              _is_key_file_encrypted
              196  LOAD_FAST                'keyfile'
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  POP_JUMP_IF_FALSE   210  'to 210'

 L. 361       202  LOAD_GLOBAL              SSLError
              204  LOAD_STR                 'Client private key is encrypted, password is required'
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           200  '200'
            210_1  COME_FROM           192  '192'
            210_2  COME_FROM           184  '184'

 L. 363       210  LOAD_FAST                'certfile'
              212  POP_JUMP_IF_FALSE   250  'to 250'

 L. 364       214  LOAD_FAST                'key_password'
              216  LOAD_CONST               None
              218  COMPARE_OP               is
              220  POP_JUMP_IF_FALSE   236  'to 236'

 L. 365       222  LOAD_FAST                'context'
              224  LOAD_METHOD              load_cert_chain
              226  LOAD_FAST                'certfile'
              228  LOAD_FAST                'keyfile'
              230  CALL_METHOD_2         2  '2 positional arguments'
              232  POP_TOP          
              234  JUMP_FORWARD        250  'to 250'
            236_0  COME_FROM           220  '220'

 L. 367       236  LOAD_FAST                'context'
              238  LOAD_METHOD              load_cert_chain
              240  LOAD_FAST                'certfile'
              242  LOAD_FAST                'keyfile'
              244  LOAD_FAST                'key_password'
              246  CALL_METHOD_3         3  '3 positional arguments'
              248  POP_TOP          
            250_0  COME_FROM           234  '234'
            250_1  COME_FROM           212  '212'

 L. 374       250  LOAD_FAST                'server_hostname'
              252  LOAD_CONST               None
              254  COMPARE_OP               is-not
          256_258  POP_JUMP_IF_FALSE   270  'to 270'
              260  LOAD_GLOBAL              is_ipaddress
              262  LOAD_FAST                'server_hostname'
              264  CALL_FUNCTION_1       1  '1 positional argument'
          266_268  POP_JUMP_IF_FALSE   276  'to 276'
            270_0  COME_FROM           256  '256'

 L. 375       270  LOAD_GLOBAL              IS_SECURETRANSPORT
          272_274  POP_JUMP_IF_FALSE   318  'to 318'
            276_0  COME_FROM           266  '266'

 L. 376       276  LOAD_GLOBAL              HAS_SNI
          278_280  POP_JUMP_IF_FALSE   306  'to 306'
              282  LOAD_FAST                'server_hostname'
              284  LOAD_CONST               None
              286  COMPARE_OP               is-not
          288_290  POP_JUMP_IF_FALSE   306  'to 306'

 L. 377       292  LOAD_FAST                'context'
              294  LOAD_ATTR                wrap_socket
              296  LOAD_FAST                'sock'
              298  LOAD_FAST                'server_hostname'
              300  LOAD_CONST               ('server_hostname',)
              302  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              304  RETURN_VALUE     
            306_0  COME_FROM           288  '288'
            306_1  COME_FROM           278  '278'

 L. 379       306  LOAD_GLOBAL              warnings
              308  LOAD_METHOD              warn

 L. 380       310  LOAD_STR                 'An HTTPS request has been made, but the SNI (Server Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings'

 L. 387       312  LOAD_GLOBAL              SNIMissingWarning
              314  CALL_METHOD_2         2  '2 positional arguments'
              316  POP_TOP          
            318_0  COME_FROM           272  '272'

 L. 390       318  LOAD_FAST                'context'
              320  LOAD_METHOD              wrap_socket
              322  LOAD_FAST                'sock'
              324  CALL_METHOD_1         1  '1 positional argument'
              326  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 182_0


def is_ipaddress(hostname):
    """Detects whether the hostname given is an IPv4 or IPv6 address.
    Also detects IPv6 addresses with Zone IDs.

    :param str hostname: Hostname to examine.
    :return: True if the hostname is an IP address, False otherwise.
    """
    if not six.PY2:
        if isinstance(hostname, bytes):
            hostname = hostname.decode('ascii')
    return bool(IPV4_RE.match(hostname) or BRACELESS_IPV6_ADDRZ_RE.match(hostname))


def _is_key_file_encrypted(key_file):
    """Detects if a key file is encrypted or not."""
    with open(key_file, 'r') as (f):
        for line in f:
            if 'ENCRYPTED' in line:
                return True

    return False