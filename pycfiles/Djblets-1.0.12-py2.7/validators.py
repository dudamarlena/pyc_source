# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/compat/django/core/validators.py
# Compiled at: 2019-06-12 01:17:17
"""Compatibility fallbacks for django.core.validators."""
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator, validate_ipv6_address
from django.utils.translation import gettext_lazy as _
from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit
if not hasattr(URLValidator, 'hostname_re'):

    class URLValidator(RegexValidator):
        ul = '\\u00a1-\\uffff'
        ipv4_re = '(?:25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)(?:\\.(?:25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)){3}'
        ipv6_re = '\\[[0-9a-f:\\.]+\\]'
        hostname_re = '[a-z' + ul + '0-9](?:[a-z' + ul + '0-9-]{0,61}[a-z' + ul + '0-9])?'
        domain_re = '(?:\\.(?!-)[a-z' + ul + '0-9-]{1,63}(?<!-))*'
        tld_re = '\\.(?!-)(?:[a-z' + ul + '-]{2,63}|xn--[a-z0-9]{1,59})(?<!-)\\.?'
        host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'
        regex = re.compile('^(?:[a-z0-9\\.\\-\\+]*)://(?:\\S+(?::\\S*)?@)?(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')(?::\\d{2,5})?(?:[/?#][^\\s]*)?\\Z', re.IGNORECASE)
        message = _('Enter a valid URL.')
        schemes = ['http', 'https', 'ftp', 'ftps']

        def __init__(self, schemes=None, **kwargs):
            super(URLValidator, self).__init__(**kwargs)
            if schemes is not None:
                self.schemes = schemes
            return

        def __call__(self, value):
            scheme = value.split('://')[0].lower()
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
                        netloc = netloc.encode('idna').decode('ascii')
                    except UnicodeError:
                        raise e

                    url = urlunsplit((scheme, netloc, path, query, fragment))
                    super(URLValidator, self).__call__(url)
                else:
                    raise

            host_match = re.search('^\\[(.+)\\](?::\\d{2,5})?$', urlsplit(value).netloc)
            if host_match:
                potential_ip = host_match.groups()[0]
                try:
                    validate_ipv6_address(potential_ip)
                except ValidationError:
                    raise ValidationError(self.message, code=self.code)

            if len(urlsplit(value).netloc) > 253:
                raise ValidationError(self.message, code=self.code)


__all__ = [
 'URLValidator']