# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/role.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 4359 bytes
__doc__ = 'PyAMS_security.role module\n\nThis module provides classes related to roles definition and registration.\n'
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from pyams_security.interfaces import IRoleEvent
from pyams_security.interfaces.base import IRole
from pyams_security.interfaces.names import ROLES_VOCABULARY_NAME
from pyams_utils.request import check_request
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'

@implementer(IRole)
class Role:
    """Role"""
    id = FieldProperty(IRole['id'])
    title = FieldProperty(IRole['title'])
    description = FieldProperty(IRole['description'])
    permissions = FieldProperty(IRole['permissions'])
    managers = FieldProperty(IRole['managers'])

    def __init__(self, values=None, **args):
        if not isinstance(values, dict):
            values = args
        self.id = values.get('id')
        self.title = values.get('title')
        self.description = values.get('description')
        self.permissions = values.get('permissions')
        self.managers = values.get('managers')


class RoleSelector:
    """RoleSelector"""

    def __init__(self, roles, config):
        if not isinstance(roles, (list, tuple, set)):
            roles = {
             roles}
        self.roles = roles

    def text(self):
        """Predicate text output"""
        return 'role_selector = %s' % str(self.roles)

    phash = text

    def __call__(self, event):
        assert IRoleEvent.providedBy(event)
        return event.role_id in self.roles


def register_role(config, role):
    """Register a new role

    Roles registry is not required.
    But only registered roles can be applied via default
    ZMI features.

    If a role is registered several times, previous registrations
    will just be updated to add new permissions.
    Title and description are not updated after first registration.
    """
    registry = config.registry
    if not IRole.providedBy(role):
        role_utility = registry.queryUtility(IRole, name=role.get('id'))
        if role_utility is None:
            role_utility = Role(role)
            registry.registerUtility(role_utility, IRole, name=role_utility.id)
        else:
            role_utility.permissions = (role_utility.permissions or set()) | (role.get('permissions') or set())
            role_utility.managers = (role_utility.managers or set()) | (role.get('managers') or set())
    else:
        registry.registerUtility(role, IRole, name=role.id)


@vocabulary_config(name=ROLES_VOCABULARY_NAME)
class RolesVocabulary(SimpleVocabulary):
    """RolesVocabulary"""
    interface = IRole

    def __init__(self, *args, **kwargs):
        request = check_request()
        registry = request.registry
        translate = request.localizer.translate
        terms = [SimpleTerm(r.id, title=translate(r.title)) for n, r in registry.getUtilitiesFor(self.interface)]
        terms.sort(key=lambda x: x.title)
        super(RolesVocabulary, self).__init__(terms)