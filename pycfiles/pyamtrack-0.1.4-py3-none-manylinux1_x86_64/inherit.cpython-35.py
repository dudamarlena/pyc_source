# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/inherit.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 7499 bytes
__doc__ = 'PyAMS_utils.inherit module\n\nThis module is used to manage a generic inheritance between a content and\nit\'s parent container. It also defines a custom InheritedFieldProperty which\nallows to automatically manage inherited properties.\n\nThis PyAMS module is used to handle inheritance between a parent object and a child which can\n"inherit" from some of it\'s properties, as long as they share the same "target" interface.\n\n    >>> from zope.interface import implementer, Interface, Attribute\n    >>> from zope.schema import TextLine\n    >>> from zope.schema.fieldproperty import FieldProperty\n\n    >>> from pyams_utils.adapter import adapter_config\n    >>> from pyams_utils.interfaces.inherit import IInheritInfo\n    >>> from pyams_utils.inherit import BaseInheritInfo, InheritedFieldProperty\n    >>> from pyams_utils.registry import get_global_registry\n\nLet\'s start by creating a "content" interface, and a marker interface for objects for which we\nwant to provide this interface:\n\n    >>> class IMyInfoInterface(IInheritInfo):\n    ...     \'\'\'Custom interface\'\'\'\n    ...     value = TextLine(title="Custom attribute")\n\n    >>> class IMyTargetInterface(Interface):\n    ...     \'\'\'Target interface\'\'\'\n\n    >>> @implementer(IMyInfoInterface)\n    ... class MyInfo(BaseInheritInfo):\n    ...     target_interface = IMyTargetInterface\n    ...     adapted_interface = IMyInfoInterface\n    ...\n    ...     _value = FieldProperty(IMyInfoInterface[\'value\'])\n    ...     value = InheritedFieldProperty(IMyInfoInterface[\'value\'])\n\nPlease note that for each field of the interface which can be inherited, you must define to\nproperties: one using "InheritedFieldProperty" with the name of the field, and one using a classic\n"FieldProperty" with the same name prefixed by "_"; this property is used to store the "local"\nproperty value, when inheritance is unset.\n\nThe adapter is created to adapt an object providing IMyTargetInterface to IMyInfoInterface;\nplease note that the adapter *must* attach the created object to it\'s parent by setting\n__parent__ attribute:\n\n    >>> @adapter_config(context=IMyTargetInterface, provides=IMyInfoInterface)\n    ... def my_info_factory(context):\n    ...     info = getattr(context, \'__info__\', None)\n    ...     if info is None:\n    ...         info = context.__info__ = MyInfo()\n    ...         info.__parent__ = context\n    ...     return info\n\nAdapter registration is here only for testing; the "adapter_config" decorator may do the job in\na normal application context:\n\n    >>> registry = get_global_registry()\n    >>> registry.registerAdapter(my_info_factory, (IMyTargetInterface, ), IMyInfoInterface)\n\nWe can then create classes which will be adapted to support inheritance:\n\n    >>> @implementer(IMyTargetInterface)\n    ... class MyTarget:\n    ...     \'\'\'Target class\'\'\'\n    ...     __parent__ = None\n    ...     __info__ = None\n\n    >>> parent = MyTarget()\n    >>> parent_info = IMyInfoInterface(parent)\n    >>> parent.__info__\n    <pyams_utils.tests.test_utils...MyInfo object at ...>\n    >>> parent_info.value = \'parent\'\n    >>> parent_info.value\n    \'parent\'\n    >>> parent_info.can_inherit\n    False\n\nAs soon as a parent is defined, the child object can inherit from it\'s parent:\n\n    >>> child = MyTarget()\n    >>> child.__parent__ = parent\n    >>> child_info = IMyInfoInterface(child)\n    >>> child.__info__\n    <pyams_utils.tests.test_utils...MyInfo object at ...>\n\n    >>> child_info.can_inherit\n    True\n    >>> child_info.inherit\n    True\n    >>> child_info.value\n    \'parent\'\n\nSetting child value while inheritance is enabled donesn\'t have any effect:\n\n    >>> child_info.value = \'child\'\n    >>> child_info.value\n    \'parent\'\n    >>> child_info.inherit_from == parent\n    True\n\nYou can disable inheritance and define your own value:\n\n    >>> child_info.inherit = False\n    >>> child_info.value = \'child\'\n    >>> child_info.value\n    \'child\'\n    >>> child_info.inherit_from == child\n    True\n\nPlease note that parent and child in this example share the same class, but this is not a\nrequirement; they just have to implement the same marker interface, to be adapted to the same\ncontent interface.\n'
from zope.interface import Interface, implementer
from zope.location import Location
from zope.schema.fieldproperty import FieldProperty
from pyams_utils.interfaces.inherit import IInheritInfo
from pyams_utils.traversing import get_parent
from pyams_utils.zodb import volatile_property
__docformat__ = 'restructuredtext'

@implementer(IInheritInfo)
class BaseInheritInfo(Location):
    """BaseInheritInfo"""
    target_interface = Interface
    adapted_interface = Interface
    _inherit = FieldProperty(IInheritInfo['inherit'])

    @volatile_property
    def parent(self):
        """Get current parent"""
        return get_parent(self.__parent__, self.target_interface, allow_context=False)

    @property
    def can_inherit(self):
        """Check if inheritance is possible"""
        return self.target_interface.providedBy(self.parent)

    @property
    def inherit(self):
        """Check if inheritance is possible and activated"""
        if self.can_inherit:
            return self._inherit
        return False

    @inherit.setter
    def inherit(self, value):
        """Activate inheritance"""
        if self.can_inherit:
            self._inherit = value
        del self.parent

    @property
    def no_inherit(self):
        """Inverted boolean value to check if inheritance is possible and activated"""
        return not bool(self.inherit)

    @no_inherit.setter
    def no_inherit(self, value):
        """Inverted inheritance setter"""
        self.inherit = not bool(value)

    @property
    def inherit_from(self):
        """Get current parent from which we inherit"""
        if not self.inherit:
            return self.__parent__
        parent = self.parent
        while self.adapted_interface(parent).inherit:
            parent = parent.parent

        return parent


class InheritedFieldProperty:
    """InheritedFieldProperty"""

    def __init__(self, field, name=None):
        if name is None:
            name = field.__name__
        self._InheritedFieldProperty__field = field
        self._InheritedFieldProperty__name = name

    def __get__(self, inst, klass):
        if inst is None:
            return self
        inherit_info = IInheritInfo(inst)
        if inherit_info.inherit and inherit_info.parent is not None:
            return getattr(inherit_info.adapted_interface(inherit_info.parent), self._InheritedFieldProperty__name)
        return getattr(inst, '_{0}'.format(self._InheritedFieldProperty__name))

    def __set__(self, inst, value):
        inherit_info = IInheritInfo(inst)
        if not (inherit_info.can_inherit and inherit_info.inherit):
            setattr(inst, '_{0}'.format(self._InheritedFieldProperty__name), value)