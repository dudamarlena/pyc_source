# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/permission.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 2578 bytes
"""PyAMS_security.permission module

This module provides classes related to permissions definition and registration.
"""
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from pyams_security.interfaces.base import IPermission
from pyams_security.interfaces.names import PERMISSIONS_VOCABULARY_NAME
from pyams_utils.request import check_request
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'

@implementer(IPermission)
class Permission:
    __doc__ = 'Permission utility class'
    id = FieldProperty(IPermission['id'])
    title = FieldProperty(IPermission['title'])
    description = FieldProperty(IPermission['description'])

    def __init__(self, values=None, **args):
        if not isinstance(values, dict):
            values = args
        self.id = values.get('id')
        self.title = values.get('title')
        self.description = values.get('description')


def register_permission(config, permission):
    """Register a new permission

    Permissions registry is not required.
    But only registered permissions can be applied via default
    ZMI features
    """
    if not IPermission.providedBy(permission):
        permission = Permission(permission)
    config.registry.registerUtility(permission, IPermission, name=permission.id)


@vocabulary_config(name=PERMISSIONS_VOCABULARY_NAME)
class PermissionsVocabulary(SimpleVocabulary):
    __doc__ = 'Permissions vocabulary'
    interface = IPermission

    def __init__(self, *args, **kwargs):
        request = check_request()
        registry = request.registry
        translate = request.localizer.translate
        terms = [SimpleTerm(p.id, title=translate(p.title)) for n, p in registry.getUtilitiesFor(self.interface)]
        terms.sort(key=lambda x: x.title)
        super(PermissionsVocabulary, self).__init__(terms)