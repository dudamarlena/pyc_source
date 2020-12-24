# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/validators.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import os, re
from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
from django.utils.functional import SimpleLazyObject
from django.utils.ipv6 import is_valid_ipv6_address
from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit
from django.utils.translation import ugettext_lazy as _, ungettext_lazy
EMPTY_VALUES = (
 None, b'', [], (), {})

def _lazy_re_compile(regex, flags=0):
    """Lazily compile a regex with flags."""

    def _compile():
        if isinstance(regex, six.string_types):
            return re.compile(regex, flags)
        else:
            assert not flags, b'flags must be empty if regex is passed pre-compiled'
            return regex

    return SimpleLazyObject(_compile)


@deconstructible
class RegexValidator(object):
    regex = b''
    message = _(b'Enter a valid value.')
    code = b'invalid'
    inverse_match = False
    flags = 0

    def __init__(self, regex=None, message=None, code=None, inverse_match=None, flags=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if inverse_match is not None:
            self.inverse_match = inverse_match
        if flags is not None:
            self.flags = flags
        if self.flags and not isinstance(self.regex, six.string_types):
            raise TypeError(b'If the flags are set, regex must be a regular expression string.')
        self.regex = _lazy_re_compile(self.regex, self.flags)
        return

    def __call__(self, value):
        """
        Validate that the input contains a match for the regular expression
        if inverse_match is False, otherwise raise ValidationError.
        """
        if self.inverse_match is bool(self.regex.search(force_text(value))):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return isinstance(other, RegexValidator) and self.regex.pattern == other.regex.pattern and self.regex.flags == other.regex.flags and self.message == other.message and self.code == other.code and self.inverse_match == other.inverse_match

    def __ne__(self, other):
        return not self == other


@deconstructible
class URLValidator(RegexValidator):
    ul = b'¡-\uffff'
    ipv4_re = b'(?:25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)(?:\\.(?:25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)){3}'
    ipv6_re = b'\\[[0-9a-f:\\.]+\\]'
    hostname_re = b'[a-z' + ul + b'0-9](?:[a-z' + ul + b'0-9-]{0,61}[a-z' + ul + b'0-9])?'
    domain_re = b'(?:\\.(?!-)[a-z' + ul + b'0-9-]{1,63}(?<!-))*'
    tld_re = b'\\.(?!-)(?:[a-z' + ul + b'-]{2,63}|xn--[a-z0-9]{1,59})(?<!-)\\.?'
    host_re = b'(' + hostname_re + domain_re + tld_re + b'|localhost)'
    regex = _lazy_re_compile(b'^(?:[a-z0-9\\.\\-\\+]*)://(?:\\S+(?::\\S*)?@)?(?:' + ipv4_re + b'|' + ipv6_re + b'|' + host_re + b')(?::\\d{2,5})?(?:[/?#][^\\s]*)?\\Z', re.IGNORECASE)
    message = _(b'Enter a valid URL.')
    schemes = [b'http', b'https', b'ftp', b'ftps']

    def __init__(self, schemes=None, **kwargs):
        super(URLValidator, self).__init__(**kwargs)
        if schemes is not None:
            self.schemes = schemes
        return

    def __call__(self, value):
        value = force_text(value)
        scheme = value.split(b'://')[0].lower()
        if scheme not in self.schemes:
            raise ValidationError(self.message, code=self.code)
        try:
            super(URLValidator, self).__call__(value)
        except ValidationError as e:
            if value:
                try:
                    scheme, netloc, path, query, fragment = urlsplit(value)
                except ValueError:
                    raise ValidationError(self.message, code=self.code)

                try:
                    netloc = netloc.encode(b'idna').decode(b'ascii')
                except UnicodeError:
                    raise e

                url = urlunsplit((scheme, netloc, path, query, fragment))
                super(URLValidator, self).__call__(url)
            else:
                raise

        host_match = re.search(b'^\\[(.+)\\](?::\\d{2,5})?$', urlsplit(value).netloc)
        if host_match:
            potential_ip = host_match.groups()[0]
            try:
                validate_ipv6_address(potential_ip)
            except ValidationError:
                raise ValidationError(self.message, code=self.code)

        if len(urlsplit(value).netloc) > 253:
            raise ValidationError(self.message, code=self.code)


integer_validator = RegexValidator(_lazy_re_compile(b'^-?\\d+\\Z'), message=_(b'Enter a valid integer.'), code=b'invalid')

def validate_integer(value):
    return integer_validator(value)


@deconstructible
class EmailValidator(object):
    message = _(b'Enter a valid email address.')
    code = b'invalid'
    user_regex = _lazy_re_compile(b'(^[-!#$%&\'*+/=?^_`{}|~0-9A-Z]+(\\.[-!#$%&\'*+/=?^_`{}|~0-9A-Z]+)*\\Z|^"([\\001-\\010\\013\\014\\016-\\037!#-\\[\\]-\\177]|\\\\[\\001-\\011\\013\\014\\016-\\177])*"\\Z)', re.IGNORECASE)
    domain_regex = _lazy_re_compile(b'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\\Z', re.IGNORECASE)
    literal_regex = _lazy_re_compile(b'\\[([A-f0-9:\\.]+)\\]\\Z', re.IGNORECASE)
    domain_whitelist = [b'localhost']

    def __init__(self, message=None, code=None, whitelist=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if whitelist is not None:
            self.domain_whitelist = whitelist
        return

    def __call__(self, value):
        value = force_text(value)
        if not value or b'@' not in value:
            raise ValidationError(self.message, code=self.code)
        user_part, domain_part = value.rsplit(b'@', 1)
        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, code=self.code)
        if domain_part not in self.domain_whitelist and not self.validate_domain_part(domain_part):
            try:
                domain_part = domain_part.encode(b'idna').decode(b'ascii')
                if self.validate_domain_part(domain_part):
                    return
            except UnicodeError:
                pass

            raise ValidationError(self.message, code=self.code)

    def validate_domain_part(self, domain_part):
        if self.domain_regex.match(domain_part):
            return True
        literal_match = self.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match.group(1)
            try:
                validate_ipv46_address(ip_address)
                return True
            except ValidationError:
                pass

        return False

    def __eq__(self, other):
        return isinstance(other, EmailValidator) and self.domain_whitelist == other.domain_whitelist and self.message == other.message and self.code == other.code


validate_email = EmailValidator()
slug_re = _lazy_re_compile(b'^[-a-zA-Z0-9_]+\\Z')
validate_slug = RegexValidator(slug_re, _(b"Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens."), b'invalid')
slug_unicode_re = _lazy_re_compile(b'^[-\\w]+\\Z', re.U)
validate_unicode_slug = RegexValidator(slug_unicode_re, _(b"Enter a valid 'slug' consisting of Unicode letters, numbers, underscores, or hyphens."), b'invalid')
ipv4_re = _lazy_re_compile(b'^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])(\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])){3}\\Z')
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


ip_address_validator_map = {b'both': (
           [
            validate_ipv46_address], _(b'Enter a valid IPv4 or IPv6 address.')), 
   b'ipv4': (
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


def int_list_validator(sep=b',', message=None, code=b'invalid', allow_negative=False):
    regexp = _lazy_re_compile(b'^%(neg)s\\d+(?:%(sep)s%(neg)s\\d+)*\\Z' % {b'neg': b'(-)?' if allow_negative else b'', 
       b'sep': re.escape(sep)})
    return RegexValidator(regexp, message=message, code=code)


validate_comma_separated_integer_list = int_list_validator(message=_(b'Enter only digits separated by commas.'))

@deconstructible
class BaseValidator(object):
    message = _(b'Ensure this value is %(limit_value)s (it is %(show_value)s).')
    code = b'limit_value'

    def __init__(self, limit_value, message=None):
        self.limit_value = limit_value
        if message:
            self.message = message

    def __call__(self, value):
        cleaned = self.clean(value)
        params = {b'limit_value': self.limit_value, b'show_value': cleaned, b'value': value}
        if self.compare(cleaned, self.limit_value):
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.limit_value == other.limit_value and self.message == other.message and self.code == other.code

    def compare(self, a, b):
        return a is not b

    def clean(self, x):
        return x


@deconstructible
class MaxValueValidator(BaseValidator):
    message = _(b'Ensure this value is less than or equal to %(limit_value)s.')
    code = b'max_value'

    def compare(self, a, b):
        return a > b


@deconstructible
class MinValueValidator(BaseValidator):
    message = _(b'Ensure this value is greater than or equal to %(limit_value)s.')
    code = b'min_value'

    def compare(self, a, b):
        return a < b


@deconstructible
class MinLengthValidator(BaseValidator):
    message = ungettext_lazy(b'Ensure this value has at least %(limit_value)d character (it has %(show_value)d).', b'Ensure this value has at least %(limit_value)d characters (it has %(show_value)d).', b'limit_value')
    code = b'min_length'

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return len(x)


@deconstructible
class MaxLengthValidator(BaseValidator):
    message = ungettext_lazy(b'Ensure this value has at most %(limit_value)d character (it has %(show_value)d).', b'Ensure this value has at most %(limit_value)d characters (it has %(show_value)d).', b'limit_value')
    code = b'max_length'

    def compare(self, a, b):
        return a > b

    def clean(self, x):
        return len(x)


@deconstructible
class DecimalValidator(object):
    """
    Validate that the input does not exceed the maximum number of digits
    expected, otherwise raise ValidationError.
    """
    messages = {b'max_digits': ungettext_lazy(b'Ensure that there are no more than %(max)s digit in total.', b'Ensure that there are no more than %(max)s digits in total.', b'max'), 
       b'max_decimal_places': ungettext_lazy(b'Ensure that there are no more than %(max)s decimal place.', b'Ensure that there are no more than %(max)s decimal places.', b'max'), 
       b'max_whole_digits': ungettext_lazy(b'Ensure that there are no more than %(max)s digit before the decimal point.', b'Ensure that there are no more than %(max)s digits before the decimal point.', b'max')}

    def __init__(self, max_digits, decimal_places):
        self.max_digits = max_digits
        self.decimal_places = decimal_places

    def __call__(self, value):
        digit_tuple, exponent = value.as_tuple()[1:]
        decimals = abs(exponent)
        digits = len(digit_tuple)
        if decimals > digits:
            digits = decimals
        whole_digits = digits - decimals
        if self.max_digits is not None and digits > self.max_digits:
            raise ValidationError(self.messages[b'max_digits'], code=b'max_digits', params={b'max': self.max_digits})
        if self.decimal_places is not None and decimals > self.decimal_places:
            raise ValidationError(self.messages[b'max_decimal_places'], code=b'max_decimal_places', params={b'max': self.decimal_places})
        if self.max_digits is not None and self.decimal_places is not None and whole_digits > self.max_digits - self.decimal_places:
            raise ValidationError(self.messages[b'max_whole_digits'], code=b'max_whole_digits', params={b'max': self.max_digits - self.decimal_places})
        return

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.max_digits == other.max_digits and self.decimal_places == other.decimal_places


@deconstructible
class FileExtensionValidator(object):
    message = _(b"File extension '%(extension)s' is not allowed. Allowed extensions are: '%(allowed_extensions)s'.")
    code = b'invalid_extension'

    def __init__(self, allowed_extensions=None, message=None, code=None):
        self.allowed_extensions = allowed_extensions
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        return

    def __call__(self, value):
        extension = os.path.splitext(value.name)[1][1:].lower()
        if self.allowed_extensions is not None and extension not in self.allowed_extensions:
            raise ValidationError(self.message, code=self.code, params={b'extension': extension, 
               b'allowed_extensions': (b', ').join(self.allowed_extensions)})
        return

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.allowed_extensions == other.allowed_extensions and self.message == other.message and self.code == other.code


def get_available_image_extensions():
    try:
        from PIL import Image
    except ImportError:
        return []

    Image.init()
    return [ ext.lower()[1:] for ext in Image.EXTENSION.keys() ]


validate_image_file_extension = FileExtensionValidator(allowed_extensions=get_available_image_extensions())