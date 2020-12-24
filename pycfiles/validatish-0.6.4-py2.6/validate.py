# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/validatish/validate.py
# Compiled at: 2010-02-16 12:33:11
"""
Library of basic validation functions.
"""
import re
from validatish.error import Invalid
_domain_name_regex = re.compile('^[a-z0-9][a-z0-9\\.\\-_]*\\.[a-z]+$', re.I)
_domain_user_regex = re.compile('^[^ \\t\\n\\r@<>()]+$', re.I)

def is_required(v, messages=None, none_zero=True):
    """ Checks the non_zero attribute but allows numberic zero to pass """
    _messages = {'required': 'is required'}
    if messages:
        _messages.update(messages)
    if none_zero:
        if not v and v != 0:
            raise Invalid(_messages['required'])
    elif v is None:
        raise Invalid(_messages['required'])
    return


def is_string(v, messages=None):
    """ checks that the value is an instance of basestring """
    if v is None:
        return
    else:
        _messages = {'type-string': 'must be a string'}
        if messages:
            _messages.update(messages)
        if not isinstance(v, basestring):
            raise Invalid(_messages['type-string'])
        return


def is_plaintext(v, extra=None, messages=None):
    """
    Checks that the value contains only alpha-numberics

    :arg extra: A list of extra characters that are allowed
    """
    if v is None:
        return
    else:
        if extra:
            extra.replace('-', '\\-')
        regex = '^[a-zA-Z0-9%s]*$' % extra
        _messages = {'type-string': 'must be a string', 
           'characters-and-numbers': 'must consist of characters and numbers only', 
           'characters-and-numbers-extra': 'must consist of characters and numbers plus any of %(extra)s'}
        if messages:
            _messages.update(messages)
        if not isinstance(v, basestring):
            raise Invalid(_messages['type-string'])
        msg = _messages['characters-and-numbers']
        if extra is not None:
            msg = _messages['characters-and-numbers-extra'] % {'extra': extra}
        p = re.compile(regex, re.UNICODE)
        if not p.match(v):
            raise Invalid(msg)
        return


def is_integer(v, messages=None):
    """ Checks that the value can be converted into an integer """
    if v is None:
        return
    else:
        _messages = {'type-integer': 'must be a integer'}
        if messages:
            _messages.update(messages)
        try:
            if v != int(v):
                raise Invalid(_messages['type-integer'])
        except (ValueError, TypeError):
            raise Invalid(_messages['type-integer'])

        return


def is_number(v, messages=None):
    """ Checks that the value is not a string but can be converted to a float """
    if v is None:
        return
    else:
        _messages = {'type-number': 'must be a number'}
        if messages:
            _messages.update(messages)
        try:
            if isinstance(v, basestring):
                raise Invalid(_messages['type-number'])
            float(v)
        except (ValueError, TypeError):
            raise Invalid(_messages['type-number'])

        return


def is_email(v, messages=None):
    """
    Validate the value looks like an email address.
    """
    if v is None:
        return
    else:
        _messages = {'type-string': 'must be a string', 
           'contain-at': 'must contain one @', 
           'username-incorrect': 'username part before the @ is incorrect', 
           'domain-incorrect': 'domain name part after the @ is incorrect'}
        if messages:
            _messages.update(messages)
        if not isinstance(v, basestring):
            raise Invalid(_messages['type-string'])
        parts = v.split('@')
        if len(parts) != 2:
            raise Invalid(_messages['contain-at'])
        (username, address) = parts
        if _domain_user_regex.match(username) is None:
            raise Invalid(_messages['username-incorrect'])
        if _domain_name_regex.match(address) is None:
            raise Invalid(_messages['domain-incorrect'])
        return


def is_domain_name(value, messages=None):
    """
    Validate the value looks like a domain name.
    """
    if value is None:
        return
    else:
        _messages = {'type-string': 'must be a string', 
           'invalid': 'is invalid'}
        if messages:
            _messages.update(messages)
        if not isinstance(value, basestring):
            raise Invalid(_messages['type-string'])
        if _domain_name_regex.match(value) is None:
            raise Invalid(_messages['invalid'])
        return


def is_url(v, with_scheme=False, messages=None):
    """ Uses a simple regex from FormEncode to check for a url """
    if v is None:
        return
    else:
        _messages = {'type-url': 'must be a url'}
        if messages:
            _messages.update(messages)
        if not isinstance(v, basestring):
            raise Invalid(_messages['type-url'])
        urlRE = re.compile('^(http|https)://(?:[a-z0-9\\-]+|[a-z0-9][a-z0-9\\-\\.\\_]*\\.[a-z]+)(?::[0-9]+)?(?:/.*)?$', re.I)
        schemeRE = re.compile('^[a-zA-Z]+:')
        if not with_scheme:
            if not schemeRE.search(v):
                v = 'http://' + v
        match = schemeRE.search(v)
        if match is None:
            raise Invalid(_messages['type-url'])
        v = match.group(0).lower() + v[len(match.group(0)):]
        if not urlRE.search(v):
            raise Invalid(_messages['type-url'])
        return


def is_equal(v, compared_to, messages=None):
    """
    Check the value, v, is equal to the comparison value.

    :arg compared_to: the value to compare to
    """
    _messages = {'incorrect': 'incorrect'}
    if messages:
        _messages.update(messages)
    if v is None or v == compared_to:
        return
    else:
        raise Invalid(_messages['incorrect'])
        return


def is_one_of(v, set_of_values, messages=None):
    """
    Check that the value is one of the set of values given

    :arg set_of_values: the set of values to check against
    """
    if v is None:
        return
    else:
        _messages = {'one-of-empty': 'must be one of []', 
           'one-of': 'must be one of %(values)r'}
        if messages:
            _messages.update(messages)
        if not set_of_values:
            raise Invalid(_messages['one-of-empty'])
        if isinstance(v, list):
            v = tuple(v)
        if v not in set(set_of_values):
            raise Invalid(_messages['one-of'] % {'values': set_of_values})
        return


def has_length(v, min=None, max=None, messages=None):
    """
    Check that the length of the string or sequence is not less than an optional min value and not greater than an optional max value

    :arg max: optional max value
    :arg min: optional min value
    """
    if v is None:
        return
    else:
        if min is None and max is None:
            return
        _messages = {'between': 'must have between %(min)s and %(max)s %(unit)s', 'fewer-than': 'must have %(max)s or fewer %(unit)s', 
           'more-than': 'must have %(min)s or more %(unit)s'}
        if messages:
            _messages.update(messages)
        if isinstance(v, basestring):
            unit = 'characters'
        else:
            unit = 'items'
        if max is not None and min is not None and (len(v) > max or len(v) < min):
            raise Invalid(_messages['between'] % {'min': min, 'max': max, 'unit': unit})
        if max is not None and len(v) > max:
            raise Invalid(_messages['fewer-than'] % {'max': max, 'unit': unit})
        if min is not None and len(v) < min:
            raise Invalid(_messages['more-than'] % {'min': min, 'unit': unit})
        return


def is_in_range(v, min=None, max=None, messages=None):
    """
    Check that the value is not less than an optional min value and not greater than an optional max value

    :arg max: optional max value
    :arg min: optional min value
    """
    if min is None and max is None:
        return
    else:
        if min is None and max is None:
            return
        _messages = {'between': 'must have between %(min)s and %(max)s', 'greater-than': 'must be greater than or equal to %(min)s', 
           'less-than': 'must be less than or equal to %(max)s'}
        if min is not None and max is not None:
            error = _messages['between'] % {'min': min, 'max': max}
        elif min is not None:
            error = _messages['greater-than'] % {'min': min}
        else:
            error = _messages['less-than'] % {'max': max}
        if max is not None and v > max:
            raise Invalid(error)
        if min is not None and v < min:
            raise Invalid(error)
        return