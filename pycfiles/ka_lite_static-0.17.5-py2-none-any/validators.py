# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/validators.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import re
try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:
    from urlparse import urlsplit, urlunsplit

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.ipv6 import is_valid_ipv6_address
from django.utils import six
EMPTY_VALUES = (
 None, b'', [], (), {})

class RegexValidator(object):
    regex = b''
    message = _(b'Enter a valid value.')
    code = b'invalid'

    def __init__(self, regex=None, message=None, code=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if isinstance(self.regex, six.string_types):
            self.regex = re.compile(self.regex)
        return

    def __call__(self, value):
        """
        Validates that the input matches the regular expression.
        """
        if not self.regex.search(force_text(value)):
            raise ValidationError(self.message, code=self.code)


class URLValidator(RegexValidator):
    regex = re.compile(b'^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}\\.?|[A-Z0-9-]{2,}\\.?)|localhost|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}|\\[?[A-F0-9]*:[A-F0-9:]+\\]?)(?::\\d+)?(?:/?|[/?]\\S+)$', re.IGNORECASE)

    def __call__(self, value):
        try:
            super(URLValidator, self).__call__(value)
        except ValidationError as e:
            if value:
                value = force_text(value)
                scheme, netloc, path, query, fragment = urlsplit(value)
                try:
                    netloc = netloc.encode(b'idna').decode(b'ascii')
                except UnicodeError:
                    raise e

                url = urlunsplit((scheme, netloc, path, query, fragment))
                super(URLValidator, self).__call__(url)
            else:
                raise
        else:
            url = value


def validate_integer(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError(b'')


class EmailValidator(RegexValidator):

    def __call__(self, value):
        try:
            super(EmailValidator, self).__call__(value)
        except ValidationError as e:
            if value and b'@' in value:
                parts = value.split(b'@')
                try:
                    parts[-1] = parts[(-1)].encode(b'idna').decode(b'ascii')
                except UnicodeError:
                    raise e

                super(EmailValidator, self).__call__((b'@').join(parts))
            else:
                raise


email_re = re.compile(b'(^[-!#$%&\'*+/=?^_`{}|~0-9A-Z]+(\\.[-!#$%&\'*+/=?^_`{}|~0-9A-Z]+)*|^"([\\001-\\010\\013\\014\\016-\\037!#-\\[\\]-\\177]|\\\\[\\001-\\011\\013\\014\\016-\\177])*")@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}\\.?|[A-Z0-9-]{2,}\\.?)$)|\\[(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)(\\.(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)){3}\\]$', re.IGNORECASE)
validate_email = EmailValidator(email_re, _(b'Enter a valid email address.'), b'invalid')
slug_re = re.compile(b'^[-a-zA-Z0-9_]+$')
validate_slug = RegexValidator(slug_re, _(b"Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens."), b'invalid')
ipv4_re = re.compile(b'^(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)(\\.(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)){3}$')
validate_ipv4_address = RegexValidator(ipv4_re, _(b'Enter a valid IPv4 address.'), b'invalid')

def validate_ipv6_address(value):
    if not is_valid_ipv6_address(value):
        raise ValidationError(_(b'Enter a valid IPv6 address.'), code=b'invalid')


def validate_ipv46_address(value):
    try:
        validate_ipv4_address(value)
    except ValidationError:
        try:
            validate_ipv6_address(value)
        except ValidationError:
            raise ValidationError(_(b'Enter a valid IPv4 or IPv6 address.'), code=b'invalid')


ip_address_validator_map = {b'both': ([validate_ipv46_address], _(b'Enter a valid IPv4 or IPv6 address.')), b'ipv4': (
           [
            validate_ipv4_address], _(b'Enter a valid IPv4 address.')), 
   b'ipv6': (
           [
            validate_ipv6_address], _(b'Enter a valid IPv6 address.'))}

def ip_address_validators(protocol, unpack_ipv4):
    """
    Depending on the given parameters returns the appropriate validators for
    the GenericIPAddressField.

    This code is here, because it is exactly the same for the model and the form field.
    """
    if protocol != b'both' and unpack_ipv4:
        raise ValueError(b"You can only use `unpack_ipv4` if `protocol` is set to 'both'")
    try:
        return ip_address_validator_map[protocol.lower()]
    except KeyError:
        raise ValueError(b"The protocol '%s' is unknown. Supported: %s" % (
         protocol, list(ip_address_validator_map)))


comma_separated_int_list_re = re.compile(b'^[\\d,]+$')
validate_comma_separated_integer_list = RegexValidator(comma_separated_int_list_re, _(b'Enter only digits separated by commas.'), b'invalid')

class BaseValidator(object):
    compare = lambda self, a, b: a is not b
    clean = lambda self, x: x
    message = _(b'Ensure this value is %(limit_value)s (it is %(show_value)s).')
    code = b'limit_value'

    def __init__(self, limit_value):
        self.limit_value = limit_value

    def __call__(self, value):
        cleaned = self.clean(value)
        params = {b'limit_value': self.limit_value, b'show_value': cleaned}
        if self.compare(cleaned, self.limit_value):
            raise ValidationError(self.message % params, code=self.code, params=params)


class MaxValueValidator(BaseValidator):
    compare = lambda self, a, b: a > b
    message = _(b'Ensure this value is less than or equal to %(limit_value)s.')
    code = b'max_value'


class MinValueValidator(BaseValidator):
    compare = lambda self, a, b: a < b
    message = _(b'Ensure this value is greater than or equal to %(limit_value)s.')
    code = b'min_value'


class MinLengthValidator(BaseValidator):
    compare = lambda self, a, b: a < b
    clean = lambda self, x: len(x)
    message = _(b'Ensure this value has at least %(limit_value)d characters (it has %(show_value)d).')
    code = b'min_length'


class MaxLengthValidator(BaseValidator):
    compare = lambda self, a, b: a > b
    clean = lambda self, x: len(x)
    message = _(b'Ensure this value has at most %(limit_value)d characters (it has %(show_value)d).')
    code = b'max_length'