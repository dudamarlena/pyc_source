# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/types/ip_address.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 1723 bytes
from ipaddress import ip_address
from sqlalchemy import types
from .choice import ScalarCoercible, ImproperlyConfigured

class IPAddressType(types.TypeDecorator, ScalarCoercible):
    """IPAddressType"""
    impl = types.Unicode(50)

    def __init__(self, max_length=50, *args, **kwargs):
        if not ip_address:
            raise ImproperlyConfigured("'ipaddr' package is required to use 'IPAddressType' in python 2")
        (super().__init__)(*args, **kwargs)
        self.impl = types.Unicode(max_length)

    def process_bind_param(self, value, dialect):
        if value:
            return str(value)

    def process_result_value(self, value, dialect):
        if value:
            return ip_address(value)

    def _coerce(self, value):
        if value:
            return ip_address(value)

    @property
    def python_type(self):
        return self.impl.type.python_type