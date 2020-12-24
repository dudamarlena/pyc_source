# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socket_proxy/utils.py
# Compiled at: 2020-05-03 13:30:25
# Size of source mod 2**32: 4137 bytes
import argparse, logging, os, re, secrets, socket, ssl, sys
from random import shuffle
from urllib.parse import urlsplit
from .base import CLIENT_NAME_SIZE, LOG_FORMAT, LOG_LEVELS
_logger = logging.getLogger(__name__)

def configure_logging(log_file, level):
    level = LOG_LEVELS.get(level.lower(), logging.DEBUG)
    log = logging.getLogger()
    log.setLevel(level)
    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, style='{'))
    log.addHandler(handler)


def generate_token():
    return secrets.token_bytes(CLIENT_NAME_SIZE)


def generate_ssl_context(*, cert=None, key=None, ca=None, server=False, ciphers=None, check_hostname=False):
    proto = ssl.PROTOCOL_TLS_SERVER if server else ssl.PROTOCOL_TLS_CLIENT
    ctx = ssl.SSLContext(proto)
    ctx.check_hostname = check_hostname
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    if server:
        ctx.options |= ssl.OP_SINGLE_DH_USE | ssl.OP_SINGLE_ECDH_USE
    if cert:
        ctx.load_cert_chain(cert, keyfile=key)
    if ca:
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.load_verify_locations(cafile=ca)
    if ciphers:
        ctx.set_ciphers(ciphers)
    _logger.debug('CA usage: %s', bool(ca))
    _logger.debug('Certificate: %s', bool(cert))
    _logger.debug('Hostname verification: %s', bool(check_hostname))
    _logger.debug('Minimal TLS Versions: %s', ctx.minimum_version.name)
    ciphers = sorted((c['name'] for c in ctx.get_ciphers()))
    _logger.debug('Ciphers: %s', ', '.join(ciphers))
    return ctx


def get_unused_port--- This code section failed: ---

 L.  78         0  LOAD_GLOBAL              socket
                2  LOAD_METHOD              socket
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'sock'

 L.  79         8  LOAD_GLOBAL              list
               10  LOAD_GLOBAL              range
               12  LOAD_FAST                'min_port'
               14  LOAD_FAST                'max_port'
               16  LOAD_CONST               1
               18  BINARY_ADD       
               20  CALL_FUNCTION_2       2  ''
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'ports'

 L.  80        26  LOAD_GLOBAL              shuffle
               28  LOAD_FAST                'ports'
               30  CALL_FUNCTION_1       1  ''
               32  POP_TOP          

 L.  81        34  LOAD_FAST                'ports'
               36  GET_ITER         
               38  FOR_ITER             98  'to 98'
               40  STORE_FAST               'port'

 L.  82        42  SETUP_FINALLY        76  'to 76'

 L.  83        44  LOAD_FAST                'sock'
               46  LOAD_METHOD              bind
               48  LOAD_STR                 ''
               50  LOAD_FAST                'port'
               52  BUILD_TUPLE_2         2 
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.  84        58  LOAD_FAST                'sock'
               60  LOAD_METHOD              close
               62  CALL_METHOD_0         0  ''
               64  POP_TOP          

 L.  85        66  LOAD_FAST                'port'
               68  POP_BLOCK        
               70  ROT_TWO          
               72  POP_TOP          
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    42  '42'

 L.  86        76  DUP_TOP          
               78  LOAD_GLOBAL              Exception
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE    94  'to 94'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L.  87        90  POP_EXCEPT       
               92  JUMP_BACK            38  'to 38'
             94_0  COME_FROM            82  '82'
               94  END_FINALLY      
               96  JUMP_BACK            38  'to 38'

Parse error at or near `ROT_TWO' instruction at offset 70


def merge_settings(a, b):
    if a:
        if b:
            return minab
    return maxab


def parse_address(address, host=None, port=None):
    FORMAT_ERROR = 'Invalid address parsed. Only host and port are supported.'
    if '/' in address:
        raise argparse.ArgumentTypeError(FORMAT_ERROR)
    try:
        parsed = urlsplit(f"http://{address}")
        h, p = parsed.hostname, parsed.port
    except Exception:
        raise argparse.ArgumentTypeError(FORMAT_ERROR)
    else:
        if not h:
            if host is None:
                raise argparse.ArgumentTypeError('Host required.')
        if not p:
            if port is None:
                raise argparse.ArgumentTypeError('Port required.')
        return (
         h or host, p or port)


def valid_file(path):
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError('Not a file.')
    return path


def valid_ports(ports):
    m = re.match('^(\\d+):(\\d+)?$', ports, re.IGNORECASE)
    if m:
        a, b = mapintm.groups()
        if 0 < a < b < 65536:
            return (
             a, b)
        raise argparse.ArgumentTypeError('Port must be in range (1, 65536)')
    raise argparse.ArgumentTypeError('Invalid port scheme.')