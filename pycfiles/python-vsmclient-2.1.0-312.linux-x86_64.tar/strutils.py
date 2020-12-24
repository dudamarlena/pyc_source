# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/openstack/common/strutils.py
# Compiled at: 2016-06-13 14:11:03
"""
System-level utilities and helper functions.
"""
import math, re, sys, unicodedata, six
from vsmclient.openstack.common.gettextutils import _
UNIT_PREFIX_EXPONENT = {'k': 1, 
   'K': 1, 
   'Ki': 1, 
   'M': 2, 
   'Mi': 2, 
   'G': 3, 
   'Gi': 3, 
   'T': 4, 
   'Ti': 4}
UNIT_SYSTEM_INFO = {'IEC': (
         1024, re.compile('(^[-+]?\\d*\\.?\\d+)([KMGT]i?)?(b|bit|B)$')), 
   'SI': (
        1000, re.compile('(^[-+]?\\d*\\.?\\d+)([kMGT])?(b|bit|B)$'))}
TRUE_STRINGS = ('1', 't', 'true', 'on', 'y', 'yes')
FALSE_STRINGS = ('0', 'f', 'false', 'off', 'n', 'no')
SLUGIFY_STRIP_RE = re.compile('[^\\w\\s-]')
SLUGIFY_HYPHENATE_RE = re.compile('[-\\s]+')
_SANITIZE_KEYS = [
 'adminPass', 'admin_pass', 'password', 'admin_password']
_SANITIZE_PATTERNS = []
_FORMAT_PATTERNS = [
 '(%(key)s\\s*[=]\\s*[\\"\\\']).*?([\\"\\\'])',
 '(<%(key)s>).*?(</%(key)s>)',
 '([\\"\\\']%(key)s[\\"\\\']\\s*:\\s*[\\"\\\']).*?([\\"\\\'])',
 '([\\\'"].*?%(key)s[\\\'"]\\s*:\\s*u?[\\\'"]).*?([\\\'"])',
 '([\\\'"].*?%(key)s[\\\'"]\\s*,\\s*\\\'--?[A-z]+\\\'\\s*,\\s*u?[\\\'"]).*?([\'"])',
 '(%(key)s\\s*--?[A-z]+\\s*)\\S+(\\s*)']
for key in _SANITIZE_KEYS:
    for pattern in _FORMAT_PATTERNS:
        reg_ex = re.compile(pattern % {'key': key}, re.DOTALL)
        _SANITIZE_PATTERNS.append(reg_ex)

def int_from_bool_as_string(subject):
    """Interpret a string as a boolean and return either 1 or 0.

    Any string value in:

        ('True', 'true', 'On', 'on', '1')

    is interpreted as a boolean True.

    Useful for JSON-decoded stuff and config file parsing
    """
    return bool_from_string(subject) and 1 or 0


def bool_from_string(subject, strict=False, default=False):
    """Interpret a string as a boolean.

    A case-insensitive match is performed such that strings matching 't',
    'true', 'on', 'y', 'yes', or '1' are considered True and, when
    `strict=False`, anything else returns the value specified by 'default'.

    Useful for JSON-decoded stuff and config file parsing.

    If `strict=True`, unrecognized values, including None, will raise a
    ValueError which is useful when parsing values passed in from an API call.
    Strings yielding False are 'f', 'false', 'off', 'n', 'no', or '0'.
    """
    if not isinstance(subject, six.string_types):
        subject = six.text_type(subject)
    lowered = subject.strip().lower()
    if lowered in TRUE_STRINGS:
        return True
    if lowered in FALSE_STRINGS:
        return False
    if strict:
        acceptable = (', ').join("'%s'" % s for s in sorted(TRUE_STRINGS + FALSE_STRINGS))
        msg = _("Unrecognized value '%(val)s', acceptable values are: %(acceptable)s") % {'val': subject, 'acceptable': acceptable}
        raise ValueError(msg)
    else:
        return default


def safe_decode(text, incoming=None, errors='strict'):
    """Decodes incoming text/bytes string using `incoming` if they're not
       already unicode.

    :param incoming: Text's current encoding
    :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html
    :returns: text or a unicode `incoming` encoded
                representation of it.
    :raises TypeError: If text is not an instance of str
    """
    if not isinstance(text, (six.string_types, six.binary_type)):
        raise TypeError("%s can't be decoded" % type(text))
    if isinstance(text, six.text_type):
        return text
    if not incoming:
        incoming = sys.stdin.encoding or sys.getdefaultencoding()
    try:
        return text.decode(incoming, errors)
    except UnicodeDecodeError:
        return text.decode('utf-8', errors)


def safe_encode(text, incoming=None, encoding='utf-8', errors='strict'):
    """Encodes incoming text/bytes string using `encoding`.

    If incoming is not specified, text is expected to be encoded with
    current python's default encoding. (`sys.getdefaultencoding`)

    :param incoming: Text's current encoding
    :param encoding: Expected encoding for text (Default UTF-8)
    :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html
    :returns: text or a bytestring `encoding` encoded
                representation of it.
    :raises TypeError: If text is not an instance of str
    """
    if not isinstance(text, (six.string_types, six.binary_type)):
        raise TypeError("%s can't be encoded" % type(text))
    if not incoming:
        incoming = sys.stdin.encoding or sys.getdefaultencoding()
    if isinstance(text, six.text_type):
        return text.encode(encoding, errors)
    else:
        if text and encoding != incoming:
            text = safe_decode(text, incoming, errors)
            return text.encode(encoding, errors)
        return text


def string_to_bytes(text, unit_system='IEC', return_int=False):
    """Converts a string into an float representation of bytes.

    The units supported for IEC ::

        Kb(it), Kib(it), Mb(it), Mib(it), Gb(it), Gib(it), Tb(it), Tib(it)
        KB, KiB, MB, MiB, GB, GiB, TB, TiB

    The units supported for SI ::

        kb(it), Mb(it), Gb(it), Tb(it)
        kB, MB, GB, TB

    Note that the SI unit system does not support capital letter 'K'

    :param text: String input for bytes size conversion.
    :param unit_system: Unit system for byte size conversion.
    :param return_int: If True, returns integer representation of text
                       in bytes. (default: decimal)
    :returns: Numerical representation of text in bytes.
    :raises ValueError: If text has an invalid value.

    """
    try:
        base, reg_ex = UNIT_SYSTEM_INFO[unit_system]
    except KeyError:
        msg = _('Invalid unit system: "%s"') % unit_system
        raise ValueError(msg)

    match = reg_ex.match(text)
    if match:
        magnitude = float(match.group(1))
        unit_prefix = match.group(2)
        if match.group(3) in ('b', 'bit'):
            magnitude /= 8
    else:
        msg = _('Invalid string format: %s') % text
        raise ValueError(msg)
    if not unit_prefix:
        res = magnitude
    else:
        res = magnitude * pow(base, UNIT_PREFIX_EXPONENT[unit_prefix])
    if return_int:
        return int(math.ceil(res))
    return res


def to_slug(value, incoming=None, errors='strict'):
    """Normalize string.

    Convert to lowercase, remove non-word characters, and convert spaces
    to hyphens.

    Inspired by Django's `slugify` filter.

    :param value: Text to slugify
    :param incoming: Text's current encoding
    :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html
    :returns: slugified unicode representation of `value`
    :raises TypeError: If text is not an instance of str
    """
    value = safe_decode(value, incoming, errors)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = SLUGIFY_STRIP_RE.sub('', value).strip().lower()
    return SLUGIFY_HYPHENATE_RE.sub('-', value)


def mask_password(message, secret='***'):
    """Replace password with 'secret' in message.

    :param message: The string which includes security information.
    :param secret: value with which to replace passwords.
    :returns: The unicode value of message with the password fields masked.

    For example:

    >>> mask_password("'adminPass' : 'aaaaa'")
    "'adminPass' : '***'"
    >>> mask_password("'admin_pass' : 'aaaaa'")
    "'admin_pass' : '***'"
    >>> mask_password('"password" : "aaaaa"')
    '"password" : "***"'
    >>> mask_password("'original_password' : 'aaaaa'")
    "'original_password' : '***'"
    >>> mask_password("u'original_password' :   u'aaaaa'")
    "u'original_password' :   u'***'"
    """
    message = six.text_type(message)
    if not any(key in message for key in _SANITIZE_KEYS):
        return message
    secret = '\\g<1>' + secret + '\\g<2>'
    for pattern in _SANITIZE_PATTERNS:
        message = re.sub(pattern, secret, message)

    return message