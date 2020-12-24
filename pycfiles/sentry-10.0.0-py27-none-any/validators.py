# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/validators.py
# Compiled at: 2019-08-16 12:27:43
from __future__ import absolute_import
import ipaddress, six, uuid

def validate_ip(value, required=True):
    if not required and not value:
        return
    ipaddress.ip_network(six.text_type(value), strict=False)
    return value


def is_float(var):
    try:
        float(var)
    except (TypeError, ValueError):
        return False

    return True


def normalize_event_id(value):
    try:
        return uuid.UUID(value).hex
    except (TypeError, AttributeError, ValueError):
        return

    return


def is_event_id(value):
    return normalize_event_id(value) is not None