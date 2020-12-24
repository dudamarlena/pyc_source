# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/types/ip_address.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 1723 bytes
from ipaddress import ip_address
from sqlalchemy import types
from .choice import ScalarCoercible, ImproperlyConfigured

class IPAddressType(types.TypeDecorator, ScalarCoercible):
    __doc__ = "\n    Changes IPAddress objects to a string representation on the way in and\n    changes them back to IPAddress objects on the way out.\n\n    IPAddressType uses ipaddress package on Python >= 3 and ipaddr_ package on\n    Python 2. In order to use IPAddressType with python you need to install\n    ipaddr_ first.\n\n    .. _ipaddr: https://pypi.python.org/pypi/ipaddr\n\n    ::\n\n\n        from odm.types import IPAddressType\n\n\n        class User(Base):\n            __tablename__ = 'user'\n            id = sa.Column(sa.Integer, autoincrement=True)\n            name = sa.Column(sa.Unicode(255))\n            ip_address = sa.Column(IPAddressType)\n\n\n        user = User()\n        user.ip_address = '123.123.123.123'\n        session.add(user)\n        session.commit()\n\n        user.ip_address  # IPAddress object\n    "
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