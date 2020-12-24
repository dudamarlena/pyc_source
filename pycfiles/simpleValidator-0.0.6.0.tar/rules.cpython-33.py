# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kenmartel/Development/Python/simpleValidator/simplevalidator/rules.py
# Compiled at: 2014-02-10 05:00:17
# Size of source mod 2**32: 5898 bytes
from __future__ import unicode_literals
import re, socket, datetime, json
messages = {'required': '{} is required', 
 'email': '{} must be a valid email', 
 'min': {'string': '{} must be more than {} characters', 
         'numeric': '{} must be higher than {}'}, 
 'max': {'string': '{} must be less than {} characters', 
         'numeric': '{} must be lower than {}'}, 
 'between': {'string': "{}'s length must be between {} and {} characters", 
             'numeric': "{}'s value must be higher than {} and lower than {}"}, 
 'ip4': '{} must be a valid ipv4 address', 
 'ip6': '{} must be a valid ipv6 address', 
 'numeric': '{} must be numerical', 
 'integer': '{} must be an integer', 
 'posinteger': '{} must be a positive integer', 
 'url': '{} must be a valid url', 
 'alpha': '{} must contain only alphabetical characters', 
 'alpha_num': '{} must contain only alphabetical characters and/or numbers', 
 'alpha_dash': '{} must contain only alphabetical characters or numbers or underscores and dashes', 
 'date': '{} is not a valid date, the format must be {}'}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def required(value):
    if is_number(value):
        return True
    return not len(value.strip()) == 0


def email(value):
    pattern = '^[a-z0-9]+([._-][a-z0-9]+)*@([a-z0-9]+([._-][a-z0-9]+))+$'
    return re.match(pattern, value) is not None


def min(value, constraint=None):
    if not constraint:
        raise ValueError('constraints are missing from the validation rule')
    if not is_number(constraint):
        raise ValueError('constraint is not a valid integer')
    constraint = float(constraint)
    if is_number(value):
        return float(value) >= constraint
    return len(value.strip()) >= constraint


def max(value, constraint=None):
    if not constraint:
        raise ValueError('constraints are missing from the validation rule')
    if not is_number(constraint):
        raise ValueError('constraint is not a valid integer')
    constraint = float(constraint)
    if is_number(value):
        return float(value) <= constraint
    return len(value.strip()) <= constraint


def between(value, constraint=None):
    if not constraint:
        raise ValueError('constraints are missing from the validation rule')
    try:
        constraints = constraint.split(',')
    except AttributeError:
        raise AttributeError('constraints must be written like so between:val1,val2')

    if len(constraints) < 2:
        raise ValueError('constraints are missing from the validation rule')
    try:
        lower = float(constraints[0])
        higher = float(constraints[1])
    except ValueError:
        raise ValueError('constraints are not valid numbers')

    if is_number(value):
        return lower <= float(value) <= higher
    return lower <= len(value.strip()) <= higher


def ip4(value):
    try:
        socket.inet_pton(socket.AF_INET, value)
    except socket.error:
        return False

    return True


def ip6(value):
    try:
        socket.inet_pton(socket.AF_INET6, value)
    except socket.error:
        return False

    return True


def url(value):
    """ Borrowed from Django ! Thanks to them """
    url_regex = re.compile('^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}\\.?|[A-Z0-9-]{2,}\\.?)|localhost|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})(?::\\d+)?(?:/?|[/?]\\S+)$', re.IGNORECASE)
    return url_regex.match(value) is not None


def numeric(value):
    return is_number(value)


def alpha(value):
    return re.match('^[a-zA-Z]+$', value) is not None


def alpha_num(value):
    return re.match('^[a-zA-Z0-9]+$', value) is not None


def alpha_dash(value):
    return re.match('^[a-zA-Z0-9][ A-Za-z0-9_-]*$', value) is not None


def integer(value):
    try:
        int(value)
    except ValueError:
        return False

    return True


def posinteger(value):
    try:
        int(value)
    except ValueError:
        return False

    return int(value) > 0


def date(value, constraint):
    try:
        datetime.datetime.strptime(value, constraint)
    except ValueError:
        return False

    return True


def is_json(value):
    try:
        json.loads(value)
    except ValueError:
        return False

    return True


def json_schema(value, constraint):
    pass