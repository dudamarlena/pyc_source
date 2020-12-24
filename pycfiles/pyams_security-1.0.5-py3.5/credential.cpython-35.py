# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/credential.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 1240 bytes
"""PyAMS_security.credential module

This module defines credentials class.
"""
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from pyams_security.interfaces import ICredentials
__docformat__ = 'restructuredtext'

@implementer(ICredentials)
class Credentials:
    __doc__ = 'Credentials class'
    prefix = FieldProperty(ICredentials['prefix'])
    id = FieldProperty(ICredentials['id'])
    attributes = FieldProperty(ICredentials['attributes'])

    def __init__(self, prefix, id, **attributes):
        self.prefix = prefix
        self.id = id
        self.attributes.update(**attributes)