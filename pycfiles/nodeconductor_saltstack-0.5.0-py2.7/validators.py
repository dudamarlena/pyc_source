# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/validators.py
# Compiled at: 2016-09-28 02:05:53
import re
from django.core.validators import ValidationError

def domain_validator(hostname):
    """
    Fully validates a domain name as compilant with the standard rules:
        - Composed of series of labels concatenated with dots, as are all domain names.
        - Each label must be between 1 and 63 characters long.
        - The entire hostname (including the delimiting dots) has a maximum of 255 characters.
        - Only characters 'a' through 'z' (in a case-insensitive manner), the digits '0' through '9'.
        - Labels can't start or end with a hyphen.
    """
    HOSTNAME_LABEL_PATTERN = re.compile('(?!-)[A-Z\\d-]+(?<!-)$', re.IGNORECASE)
    if not hostname:
        return
    if len(hostname) > 255:
        raise ValidationError('The domain name cannot be composed of more than 255 characters.')
    if hostname[-1:] == '.':
        hostname = hostname[:-1]
    for label in hostname.split('.'):
        if len(label) > 63:
            raise ValidationError("The label '%(label)s' is too long (maximum is 63 characters)." % {'label': label})
        if not HOSTNAME_LABEL_PATTERN.match(label):
            raise ValidationError("Unallowed characters in label '%(label)s'." % {'label': label})