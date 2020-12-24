# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/inherit.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 7499 bytes
"""PyAMS_utils.inherit module

This module is used to manage a generic inheritance between a content and
it's parent container. It also defines a custom InheritedFieldProperty which
allows to automatically manage inherited properties.

This PyAMS module is used to handle inheritance between a parent object and a child which can
"inherit" from some of it's properties, as long as they share the same "target" interface.

    >>> from zope.interface import implementer, Interface, Attribute
    >>> from zope.schema import TextLine
    >>> from zope.schema.fieldproperty import FieldProperty

    >>> from pyams_utils.adapter import adapter_config
    >>> from pyams_utils.interfaces.inherit import IInheritInfo
    >>> from pyams_utils.inherit import BaseInheritInfo, InheritedFieldProperty
    >>> from pyams_utils.registry import get_global_registry

Let's start by creating a "content" interface, and a marker interface for objects for which we
want to provide this interface:

    >>> class IMyInfoInterface(IInheritInfo):
    ...     '''Custom interface'''
    ...     value = TextLine(title="Custom attribute")

    >>> class IMyTargetInterface(Interface):
    ...     '''Target interface'''

    >>> @implementer(IMyInfoInterface)
    ... class MyInfo(BaseInheritInfo):
    ...     target_interface = IMyTargetInterface
    ...     adapted_interface = IMyInfoInterface
    ...
    ...     _value = FieldProperty(IMyInfoInterface['value'])
    ...     value = InheritedFieldProperty(IMyInfoInterface['value'])

Please note that for each field of the interface which can be inherited, you must define to
properties: one using "InheritedFieldProperty" with the name of the field, and one using a classic
"FieldProperty" with the same name prefixed by "_"; this property is used to store the "local"
property value, when inheritance is unset.

The adapter is created to adapt an object providing IMyTargetInterface to IMyInfoInterface;
please note that the adapter *must* attach the created object to it's parent by setting
__parent__ attribute:

    >>> @adapter_config(context=IMyTargetInterface, provides=IMyInfoInterface)
    ... def my_info_factory(context):
    ...     info = getattr(context, '__info__', None)
    ...     if info is None:
    ...         info = context.__info__ = MyInfo()
    ...         info.__parent__ = context
    ...     return info

Adapter registration is here only for testing; the "adapter_config" decorator may do the job in
a normal application context:

    >>> registry = get_global_registry()
    >>> registry.registerAdapter(my_info_factory, (IMyTargetInterface, ), IMyInfoInterface)

We can then create classes which will be adapted to support inheritance:

    >>> @implementer(IMyTargetInterface)
    ... class MyTarget:
    ...     '''Target class'''
    ...     __parent__ = None
    ...     __info__ = None

    >>> parent = MyTarget()
    >>> parent_info = IMyInfoInterface(parent)
    >>> parent.__info__
    <pyams_utils.tests.test_utils...MyInfo object at ...>
    >>> parent_info.value = 'parent'
    >>> parent_info.value
    'parent'
    >>> parent_info.can_inherit
    False

As soon as a parent is defined, the child object can inherit from it's parent:

    >>> child = MyTarget()
    >>> child.__parent__ = parent
    >>> child_info = IMyInfoInterface(child)
    >>> child.__info__
    <pyams_utils.tests.test_utils...MyInfo object at ...>

    >>> child_info.can_inherit
    True
    >>> child_info.inherit
    True
    >>> child_info.value
    'parent'

Setting child value while inheritance is enabled donesn't have any effect:

    >>> child_info.value = 'child'
    >>> child_info.value
    'parent'
    >>> child_info.inherit_from == parent
    True

You can disable inheritance and define your own value:

    >>> child_info.inherit = False
    >>> child_info.value = 'child'
    >>> child_info.value
    'child'
    >>> child_info.inherit_from == child
    True

Please note that parent and child in this example share the same class, but this is not a
requirement; they just have to implement the same marker interface, to be adapted to the same
content interface.
"""
from zope.interface import Interface, implementer
from zope.location import Location
from zope.schema.fieldproperty import FieldProperty
from pyams_utils.interfaces.inherit import IInheritInfo
from pyams_utils.traversing import get_parent
from pyams_utils.zodb import volatile_property
__docformat__ = 'restructuredtext'

@implementer(IInheritInfo)
class BaseInheritInfo(Location):
    __doc__ = "Base inherit class\n\n    Subclasses may generaly override target_interface and adapted_interface to\n    correctly handle inheritance (see example in doctests).\n    Please note also that adapters to this interface must correctly 'locate'\n    "
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
    __doc__ = 'Inherited field property'

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