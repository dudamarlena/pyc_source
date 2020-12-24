# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_vendor/urllib3/util/ssl_.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 14163 bytes
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

        def load_verify_locations(self, cafile=None, capath=None):
            self.ca_certs = cafile
            if capath is not None:
                raise SSLError('CA directories not supported in older Pythons')

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
    Defaults to :data:`ssl.CERT_NONE`.
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

        from pip._vendor.urllib3.util import ssl_
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

 L. 327         0  LOAD_FAST                'ssl_context'
                2  STORE_FAST               'context'

 L. 328         4  LOAD_FAST                'context'
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L. 332        12  LOAD_GLOBAL              create_urllib3_context
               14  LOAD_FAST                'ssl_version'
               16  LOAD_FAST                'cert_reqs'
               18  LOAD_FAST                'ciphers'
               20  LOAD_CONST               ('ciphers',)
               22  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               24  STORE_FAST               'context'
             26_0  COME_FROM            10  '10'

 L. 334        26  LOAD_FAST                'ca_certs'
               28  POP_JUMP_IF_TRUE     34  'to 34'
               30  LOAD_FAST                'ca_cert_dir'
               32  POP_JUMP_IF_FALSE   150  'to 150'
             34_0  COME_FROM            28  '28'

 L. 335        34  SETUP_EXCEPT         52  'to 52'

 L. 336        36  LOAD_FAST                'context'
               38  LOAD_METHOD              load_verify_locations
               40  LOAD_FAST                'ca_certs'
               42  LOAD_FAST                'ca_cert_dir'
               44  CALL_METHOD_2         2  '2 positional arguments'
               46  POP_TOP          
               48  POP_BLOCK        
               50  JUMP_ABSOLUTE       176  'to 176'
             52_0  COME_FROM_EXCEPT     34  '34'

 L. 337        52  DUP_TOP          
               54  LOAD_GLOBAL              IOError
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    92  'to 92'
               60  POP_TOP          
               62  STORE_FAST               'e'
               64  POP_TOP          
               66  SETUP_FINALLY        80  'to 80'

 L. 338        68  LOAD_GLOBAL              SSLError
               70  LOAD_FAST                'e'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  RAISE_VARARGS_1       1  'exception instance'
               76  POP_BLOCK        
               78  LOAD_CONST               None
             80_0  COME_FROM_FINALLY    66  '66'
               80  LOAD_CONST               None
               82  STORE_FAST               'e'
               84  DELETE_FAST              'e'
               86  END_FINALLY      
               88  POP_EXCEPT       
               90  JUMP_ABSOLUTE       176  'to 176'
             92_0  COME_FROM            58  '58'

 L. 341        92  DUP_TOP          
               94  LOAD_GLOBAL              OSError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   146  'to 146'
              100  POP_TOP          
              102  STORE_FAST               'e'
              104  POP_TOP          
              106  SETUP_FINALLY       134  'to 134'

 L. 342       108  LOAD_FAST                'e'
              110  LOAD_ATTR                errno
              112  LOAD_GLOBAL              errno
              114  LOAD_ATTR                ENOENT
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L. 343       120  LOAD_GLOBAL              SSLError
              122  LOAD_FAST                'e'
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'

 L. 344       128  RAISE_VARARGS_0       0  'reraise'
              130  POP_BLOCK        
              132  LOAD_CONST               None
            134_0  COME_FROM_FINALLY   106  '106'
              134  LOAD_CONST               None
              136  STORE_FAST               'e'
              138  DELETE_FAST              'e'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_ABSOLUTE       176  'to 176'
            146_0  COME_FROM            98  '98'
              146  END_FINALLY      
              148  JUMP_FORWARD        176  'to 176'
            150_0  COME_FROM            32  '32'

 L. 346       150  LOAD_FAST                'ssl_context'
              152  LOAD_CONST               None
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   176  'to 176'
              158  LOAD_GLOBAL              hasattr
              160  LOAD_FAST                'context'
              162  LOAD_STR                 'load_default_certs'
              164  CALL_FUNCTION_2       2  '2 positional arguments'
              166  POP_JUMP_IF_FALSE   176  'to 176'

 L. 348       168  LOAD_FAST                'context'
              170  LOAD_METHOD              load_default_certs
              172  CALL_METHOD_0         0  '0 positional arguments'
              174  POP_TOP          
            176_0  COME_FROM_EXCEPT_CLAUSE   166  '166'
            176_1  COME_FROM_EXCEPT_CLAUSE   156  '156'
            176_2  COME_FROM_EXCEPT_CLAUSE   148  '148'
            176_3  COME_FROM_EXCEPT_CLAUSE    90  '90'

 L. 353       176  LOAD_FAST                'keyfile'
              178  POP_JUMP_IF_FALSE   204  'to 204'
              180  LOAD_FAST                'key_password'
              182  LOAD_CONST               None
              184  COMPARE_OP               is
              186  POP_JUMP_IF_FALSE   204  'to 204'
              188  LOAD_GLOBAL              _is_key_file_encrypted
              190  LOAD_FAST                'keyfile'
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  POP_JUMP_IF_FALSE   204  'to 204'

 L. 354       196  LOAD_GLOBAL              SSLError
              198  LOAD_STR                 'Client private key is encrypted, password is required'
              200  CALL_FUNCTION_1       1  '1 positional argument'
              202  RAISE_VARARGS_1       1  'exception instance'
            204_0  COME_FROM           194  '194'
            204_1  COME_FROM           186  '186'
            204_2  COME_FROM           178  '178'

 L. 356       204  LOAD_FAST                'certfile'
              206  POP_JUMP_IF_FALSE   244  'to 244'

 L. 357       208  LOAD_FAST                'key_password'
              210  LOAD_CONST               None
              212  COMPARE_OP               is
              214  POP_JUMP_IF_FALSE   230  'to 230'

 L. 358       216  LOAD_FAST                'context'
              218  LOAD_METHOD              load_cert_chain
              220  LOAD_FAST                'certfile'
              222  LOAD_FAST                'keyfile'
              224  CALL_METHOD_2         2  '2 positional arguments'
              226  POP_TOP          
              228  JUMP_FORWARD        244  'to 244'
            230_0  COME_FROM           214  '214'

 L. 360       230  LOAD_FAST                'context'
              232  LOAD_METHOD              load_cert_chain
              234  LOAD_FAST                'certfile'
              236  LOAD_FAST                'keyfile'
              238  LOAD_FAST                'key_password'
              240  CALL_METHOD_3         3  '3 positional arguments'
              242  POP_TOP          
            244_0  COME_FROM           228  '228'
            244_1  COME_FROM           206  '206'

 L. 367       244  LOAD_FAST                'server_hostname'
              246  LOAD_CONST               None
              248  COMPARE_OP               is-not
          250_252  POP_JUMP_IF_FALSE   264  'to 264'
              254  LOAD_GLOBAL              is_ipaddress
              256  LOAD_FAST                'server_hostname'
              258  CALL_FUNCTION_1       1  '1 positional argument'
          260_262  POP_JUMP_IF_FALSE   270  'to 270'
            264_0  COME_FROM           250  '250'

 L. 368       264  LOAD_GLOBAL              IS_SECURETRANSPORT
          266_268  POP_JUMP_IF_FALSE   312  'to 312'
            270_0  COME_FROM           260  '260'

 L. 369       270  LOAD_GLOBAL              HAS_SNI
          272_274  POP_JUMP_IF_FALSE   300  'to 300'
              276  LOAD_FAST                'server_hostname'
              278  LOAD_CONST               None
              280  COMPARE_OP               is-not
          282_284  POP_JUMP_IF_FALSE   300  'to 300'

 L. 370       286  LOAD_FAST                'context'
              288  LOAD_ATTR                wrap_socket
              290  LOAD_FAST                'sock'
              292  LOAD_FAST                'server_hostname'
              294  LOAD_CONST               ('server_hostname',)
              296  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              298  RETURN_VALUE     
            300_0  COME_FROM           282  '282'
            300_1  COME_FROM           272  '272'

 L. 372       300  LOAD_GLOBAL              warnings
              302  LOAD_METHOD              warn

 L. 373       304  LOAD_STR                 'An HTTPS request has been made, but the SNI (Server Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings'

 L. 380       306  LOAD_GLOBAL              SNIMissingWarning
              308  CALL_METHOD_2         2  '2 positional arguments'
              310  POP_TOP          
            312_0  COME_FROM           266  '266'

 L. 383       312  LOAD_FAST                'context'
              314  LOAD_METHOD              wrap_socket
              316  LOAD_FAST                'sock'
              318  CALL_METHOD_1         1  '1 positional argument'
              320  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 176_0


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