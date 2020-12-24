# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/principal.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 2856 bytes
__doc__ = 'PyAMS_security.principal module\n\nThis module provides principal related classes.\n'
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility
from zope.schema.fieldproperty import FieldProperty
from pyams_security.interfaces.base import IPrincipalInfo
from pyams_utils.adapter import adapter_config
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'
from pyams_security import _

@implementer(IPrincipalInfo)
class PrincipalInfo:
    """PrincipalInfo"""
    id = FieldProperty(IPrincipalInfo['id'])
    title = FieldProperty(IPrincipalInfo['title'])
    attributes = FieldProperty(IPrincipalInfo['attributes'])

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.title = kwargs.pop('title', '__unknown__')
        self.attributes = kwargs

    def __eq__(self, other):
        return isinstance(other, PrincipalInfo) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


@implementer(IPrincipalInfo)
class UnknownPrincipal:
    """UnknownPrincipal"""
    id = '__none__'
    title = _('< unknown principal >')


UnknownPrincipal = UnknownPrincipal()

@implementer(IPrincipalInfo)
class MissingPrincipal:
    """MissingPrincipal"""
    id = FieldProperty(IPrincipalInfo['id'])

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')

    @property
    def title(self):
        """Get principal title"""
        return 'MissingPrincipal: {id}'.format(id=self.id)

    def __eq__(self, other):
        return isinstance(other, PrincipalInfo) and self.id == other.id


@adapter_config(context=IPrincipalInfo, provides=IAnnotations)
def get_principal_annotations(principal):
    """Principal annotations adapter"""
    annotations = query_utility(IPrincipalAnnotationUtility)
    if annotations is not None:
        return annotations.getAnnotations(principal)