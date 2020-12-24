# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/credential.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 1240 bytes
__doc__ = 'PyAMS_security.credential module\n\nThis module defines credentials class.\n'
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from pyams_security.interfaces import ICredentials
__docformat__ = 'restructuredtext'

@implementer(ICredentials)
class Credentials:
    """Credentials"""
    prefix = FieldProperty(ICredentials['prefix'])
    id = FieldProperty(ICredentials['id'])
    attributes = FieldProperty(ICredentials['attributes'])

    def __init__(self, prefix, id, **attributes):
        self.prefix = prefix
        self.id = id
        self.attributes.update(**attributes)