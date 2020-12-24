# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/validator.py
# Compiled at: 2016-06-13 14:11:03
import base64, re
from vsm.openstack.common import log as logging
LOG = logging.getLogger(__name__)

def _get_path_validator_regex():
    pchar = "([A-Za-z0-9\\-._~!$&'()*+,;=:@]|%[0-9A-Fa-f]{2})"
    path = '((/{pchar}*)*|'
    path += '/({pchar}+(/{pchar}*)*)?|'
    path += '{pchar}+(/{pchar}*)*|'
    path += '{pchar}+(/{pchar}*)*|)'
    path = path.format(pchar=pchar)
    return re.compile(path)


VALIDATE_PATH_RE = _get_path_validator_regex()

def validate_str(max_length=None):

    def _do(val):
        if not isinstance(val, basestring):
            return False
        if max_length and len(val) > max_length:
            return False
        return True

    return _do


def validate_int(max_value=None):

    def _do(val):
        if not isinstance(val, int):
            return False
        if max_value and val > max_value:
            return False
        return True

    return _do


def validate_url_path(val):
    """True if val is matched by the path component grammar in rfc3986."""
    if not validate_str()(val):
        return False
    return VALIDATE_PATH_RE.match(val).end() == len(val)


def validate_image_path(val):
    if not validate_str()(val):
        return False
    bucket_name = val.split('/')[0]
    manifest_path = val[len(bucket_name) + 1:]
    if not len(bucket_name) or not len(manifest_path):
        return False
    if val[0] == '/':
        return False
    if not validate_url_path('/' + val):
        return False
    return True


def validate_user_data(user_data):
    """Check if the user_data is encoded properly."""
    try:
        user_data = base64.b64decode(user_data)
    except TypeError:
        return False

    return True


def validate(args, validator):
    """Validate values of args against validators in validator.

    :param args:      Dict of values to be validated.
    :param validator: A dict where the keys map to keys in args
                      and the values are validators.
                      Applies each validator to ``args[key]``
    :returns: True if validation succeeds. Otherwise False.

    A validator should be a callable which accepts 1 argument and which
    returns True if the argument passes validation. False otherwise.
    A validator should not raise an exception to indicate validity of the
    argument.

    Only validates keys which show up in both args and validator.

    """
    for key in validator:
        if key not in args:
            continue
        f = validator[key]
        if not callable(f):
            raise AssertionError
            f(args[key]) or LOG.debug(_('%(key)s with value %(value)s failed validator %(name)s'), {'key': key, 'value': args[key], 'name': f.__name__})
            return False

    return True