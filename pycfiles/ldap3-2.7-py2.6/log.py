# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\utils\log.py
# Compiled at: 2020-02-23 02:04:04
"""
"""
from logging import getLogger, DEBUG
from copy import deepcopy
from pprint import pformat
from ..protocol.rfc4511 import LDAPMessage
OFF = 0
ERROR = 10
BASIC = 20
PROTOCOL = 30
NETWORK = 40
EXTENDED = 50
_sensitive_lines = ('simple', 'credentials', 'serversaslcreds')
_sensitive_args = ('simple', 'password', 'sasl_credentials', 'saslcreds', 'server_creds')
_sensitive_attrs = ('userpassword', 'unicodepwd')
_hide_sensitive_data = None
DETAIL_LEVELS = [
 OFF, ERROR, BASIC, PROTOCOL, NETWORK, EXTENDED]
_max_line_length = 4096
_logging_level = None
_detail_level = None
_logging_encoding = 'ascii'
try:
    from logging import NullHandler
except ImportError:
    from logging import Handler

    class NullHandler(Handler):

        def handle(self, record):
            pass

        def emit(self, record):
            pass

        def createLock(self):
            self.lock = None
            return


def _strip_sensitive_data_from_dict(d):
    if not isinstance(d, dict):
        return d
    try:
        d = deepcopy(d)
    except Exception:
        return d
    else:
        for k in d.keys():
            if isinstance(d[k], dict):
                d[k] = _strip_sensitive_data_from_dict(d[k])
            elif k.lower() in _sensitive_args and d[k]:
                d[k] = '<stripped %d characters of sensitive data>' % len(d[k])

    return d


def get_detail_level_name(level_name):
    if level_name == OFF:
        return 'OFF'
    if level_name == ERROR:
        return 'ERROR'
    if level_name == BASIC:
        return 'BASIC'
    if level_name == PROTOCOL:
        return 'PROTOCOL'
    if level_name == NETWORK:
        return 'NETWORK'
    if level_name == EXTENDED:
        return 'EXTENDED'
    raise ValueError('unknown detail level')


def log(detail, message, *args):
    global _detail_level
    global _hide_sensitive_data
    global _logging_level
    global _max_line_length
    if detail <= _detail_level:
        if _hide_sensitive_data:
            args = tuple([ _strip_sensitive_data_from_dict(arg) if isinstance(arg, dict) else arg for arg in args ])
        encoded_message = (get_detail_level_name(detail) + ':' + message % args).encode(_logging_encoding, 'backslashreplace')
        if str is not bytes:
            encoded_message = encoded_message.decode()
        if len(encoded_message) > _max_line_length:
            logger.log(_logging_level, encoded_message[:_max_line_length] + ' <removed %d remaining bytes in this log line>' % (len(encoded_message) - _max_line_length,))
        else:
            logger.log(_logging_level, encoded_message)


def log_enabled(detail):
    if detail <= _detail_level:
        if logger.isEnabledFor(_logging_level):
            return True
    return False


def set_library_log_hide_sensitive_data(hide=True):
    global _hide_sensitive_data
    if hide:
        _hide_sensitive_data = True
    else:
        _hide_sensitive_data = False
    if log_enabled(ERROR):
        log(ERROR, 'hide sensitive data set to ' + str(_hide_sensitive_data))


def get_library_log_hide_sensitive_data():
    if _hide_sensitive_data:
        return True
    return False


def set_library_log_activation_level(logging_level):
    global _logging_level
    if isinstance(logging_level, int):
        _logging_level = logging_level
    else:
        if log_enabled(ERROR):
            log(ERROR, 'invalid library log activation level <%s> ', logging_level)
        raise ValueError('invalid library log activation level')


def get_library_log_activation_lavel():
    return _logging_level


def set_library_log_max_line_length(length):
    global _max_line_length
    if isinstance(length, int):
        _max_line_length = length
    else:
        if log_enabled(ERROR):
            log(ERROR, 'invalid log max line length <%s> ', length)
        raise ValueError('invalid library log max line length')


def get_library_log_max_line_length():
    return _max_line_length


def set_library_log_detail_level(detail):
    global _detail_level
    if detail in DETAIL_LEVELS:
        _detail_level = detail
        if log_enabled(ERROR):
            log(ERROR, 'detail level set to ' + get_detail_level_name(_detail_level))
    else:
        if log_enabled(ERROR):
            log(ERROR, 'unable to set log detail level to <%s>', detail)
        raise ValueError('invalid library log detail level')


def get_library_log_detail_level():
    return _detail_level


def format_ldap_message(message, prefix):
    if isinstance(message, LDAPMessage):
        try:
            formatted = message.prettyPrint().split('\n')
        except Exception, e:
            formatted = [
             'pyasn1 exception', str(e)]

    else:
        formatted = pformat(message).split('\n')
    prefixed = ''
    for line in formatted:
        if line:
            if _hide_sensitive_data and line.strip().lower().startswith(_sensitive_lines):
                (tag, _, data) = line.partition('=')
                if data.startswith("b'") and data.endswith("'") or data.startswith('b"') and data.endswith('"'):
                    prefixed += '\n' + prefix + tag + '=<stripped %d characters of sensitive data>' % (len(data) - 3,)
                else:
                    prefixed += '\n' + prefix + tag + '=<stripped %d characters of sensitive data>' % len(data)
            else:
                prefixed += '\n' + prefix + line

    return prefixed


logger = getLogger('ldap3')
logger.addHandler(NullHandler())
set_library_log_activation_level(DEBUG)
set_library_log_detail_level(OFF)
set_library_log_hide_sensitive_data(True)