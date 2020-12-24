# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/constant2-project/constant2/_constant2.py
# Compiled at: 2018-12-19 11:16:53
from __future__ import print_function, unicode_literals
import inspect
from copy import deepcopy
from pprint import pprint
from collections import OrderedDict
try:
    from .pkg.pylru import lrudecorator
    from .pkg.sixmini import integer_types, string_types, add_metaclass
    from .pkg.inspect_mate import is_class_method, is_regular_method, get_all_attributes
    from .pkg.pytest import approx
    from .pkg.superjson import json
except:
    from constant2.pkg.pylru import lrudecorator
    from constant2.pkg.sixmini import integer_types, string_types, add_metaclass
    from constant2.pkg.inspect_mate import is_class_method, is_regular_method, get_all_attributes
    from constant2.pkg.pytest import approx
    from constant2.pkg.superjson import json

try:
    del json._dumpers[b'collections.OrderedDict']
except KeyError:
    pass

class _Constant(object):
    """Generic Constantant.

    Inherit from this class to define a data container class.

    all nested Constant class automatically inherit from :class:`Constant`.
    """
    __creation_index__ = 0

    def __init__(self):
        """

        .. versionadded:: 0.0.3
        """
        for attr, value in self.__class__.Items():
            value = deepcopy(value)
            setattr(self, attr, value)

        for attr, Subclass in self.Subclasses():
            value = Subclass()
            setattr(self, attr, value)

        self.__creation_index__ = Constant.__creation_index__
        Constant.__creation_index__ += 1

    def __repr__(self):
        items_str = (b', ').join([ b'%s=%r' % (attr, value) for attr, value in self.items() ])
        nested_str = (b', ').join([ b'%s=%r' % (attr, subclass) for attr, subclass in self.subclasses() ])
        l = list()
        if items_str:
            l.append(items_str)
        if nested_str:
            l.append(nested_str)
        return (b'{classname}({args})').format(classname=self.__class__.__name__, args=(b', ').join(l))

    @classmethod
    def Items(cls):
        """non-class attributes ordered by alphabetical order.

        ::

            >>> class MyClass(Constant):
            ...     a = 1 # non-class attributre
            ...     b = 2 # non-class attributre
            ...
            ...     class C(Constant):
            ...         pass
            ...
            ...     class D(Constant):
            ...         pass

            >>> MyClass.Items()
            [("a", 1), ("b", 2)]

        .. versionadded:: 0.0.5
        """
        l = list()
        for attr, value in get_all_attributes(cls):
            if not inspect.isclass(value):
                l.append((attr, value))

        return list(sorted(l, key=lambda x: x[0]))

    def items(self):
        """non-class attributes ordered by alphabetical order.

        ::

            >>> class MyClass(Constant):
            ...     a = 1 # non-class attributre
            ...     b = 2 # non-class attributre
            ...
            ...     class C(Constant):
            ...         pass
            ...
            ...     class D(Constant):
            ...         pass

            >>> my_class = MyClass()
            >>> my_class.items()
            [("a", 1), ("b", 2)]

        .. versionchanged:: 0.0.5
        """
        l = list()
        for attr, value in get_all_attributes(self.__class__):
            value = getattr(self, attr)
            if not isinstance(value, Constant):
                l.append((attr, value))

        return list(sorted(l, key=lambda x: x[0]))

    def __eq__(self, other):
        return self.items() == other.items()

    @classmethod
    def Keys(cls):
        """All non-class attribute name list.

        .. versionadded:: 0.0.5
        """
        return [ attr for attr, _ in cls.Items() ]

    def keys(self):
        """All non-class attribute name list.

        .. versionchanged:: 0.0.5
        """
        return [ attr for attr, _ in self.items() ]

    @classmethod
    def Values(cls):
        """All non-class attribute value list.

        .. versionadded:: 0.0.5
        """
        return [ value for _, value in cls.Items() ]

    def values(self):
        """All non-class attribute value list.

        .. versionchanged:: 0.0.5
        """
        return [ value for _, value in self.items() ]

    @classmethod
    def ToDict(cls):
        """Return regular class variable and it's value as a dictionary data.

        .. versionadded:: 0.0.5
        """
        return dict(cls.Items())

    def to_dict(self):
        """Return regular class variable and it's value as a dictionary data.

        .. versionchanged:: 0.0.5
        """
        return dict(self.items())

    @classmethod
    def Subclasses(cls, sort_by=None, reverse=False):
        """Get all nested Constant class and it's name pair.

        :param sort_by: the attribute name used for sorting.
        :param reverse: if True, return in descend order.
        :returns: [(attr, value),...] pairs.

        ::

        >>> class MyClass(Constant):
        ...     a = 1 # non-class attributre
        ...     b = 2 # non-class attributre
        ...
        ...     class C(Constant):
        ...         pass
        ...
        ...     class D(Constant):
        ...         pass

        >>> MyClass.Subclasses()
        [("C", MyClass.C), ("D", MyClass.D)]

        .. versionadded:: 0.0.3
        """
        l = list()
        for attr, value in get_all_attributes(cls):
            try:
                if issubclass(value, Constant):
                    l.append((attr, value))
            except:
                pass

        if sort_by is None:
            sort_by = b'__creation_index__'
        l = list(sorted(l, key=lambda x: getattr(x[1], sort_by), reverse=reverse))
        return l

    def subclasses(self, sort_by=None, reverse=False):
        """Get all nested Constant class instance and it's name pair.

        :param sort_by: the attribute name used for sorting.
        :param reverse: if True, return in descend order.
        :returns: [(attr, value),...] pairs.

        ::

            >>> class MyClass(Constant):
            ...     a = 1 # non-class attributre
            ...     b = 2 # non-class attributre
            ...
            ...     class C(Constant):
            ...         pass
            ...
            ...     class D(Constant):
            ...         pass

            >>> my_class = MyClass()
            >>> my_class.subclasses()
            [("C", my_class.C), ("D", my_class.D)]

        .. versionadded:: 0.0.4
        """
        l = list()
        for attr, _ in self.Subclasses(sort_by, reverse):
            value = getattr(self, attr)
            l.append((attr, value))

        return l

    @classmethod
    @lrudecorator(size=64)
    def GetFirst(cls, attr, value, e=1e-06, sort_by=b'__name__'):
        """Get the first nested Constant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.

        .. versionadded:: 0.0.5
        """
        for _, klass in cls.Subclasses(sort_by=sort_by):
            try:
                if klass.__dict__[attr] == approx(value, e):
                    return klass
            except:
                pass

        return

    def get_first(self, attr, value, e=1e-06, sort_by=b'__name__', reverse=False):
        """Get the first nested Constant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.

        .. versionchanged:: 0.0.5
        """
        for _, klass in self.subclasses(sort_by, reverse):
            try:
                if getattr(klass, attr) == approx(value, e):
                    return klass
            except:
                pass

        return

    @classmethod
    @lrudecorator(size=64)
    def GetAll(cls, attr, value, e=1e-06, sort_by=b'__name__'):
        """Get all nested Constant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.

        .. versionadded:: 0.0.5
        """
        matched = list()
        for _, klass in cls.Subclasses(sort_by=sort_by):
            try:
                if klass.__dict__[attr] == approx(value, e):
                    matched.append(klass)
            except:
                pass

        return matched

    def get_all(self, attr, value, e=1e-06, sort_by=b'__name__', reverse=False):
        """Get all nested Constant class that met ``klass.attr == value``.

        :param attr: attribute name.
        :param value: value.
        :param e: used for float value comparison.
        :param sort_by: nested class is ordered by <sort_by> attribute.

        .. versionchanged:: 0.0.5
        """
        matched = list()
        for _, klass in self.subclasses(sort_by, reverse):
            try:
                if getattr(klass, attr) == approx(value, e):
                    matched.append(klass)
            except:
                pass

        return matched

    @classmethod
    def ToIds(cls, klass_list, id_field=b'id'):
        return [ getattr(klass, id_field) for klass in klass_list ]

    def to_ids(self, instance_list, id_field=b'id'):
        return [ getattr(instance, id_field) for instance in instance_list ]

    @classmethod
    def ToClasses(cls, klass_id_list, id_field=b'id'):
        return [ cls.GetFirst(id_field, klass_id) for klass_id in klass_id_list ]

    def to_instances(self, instance_id_list, id_field=b'id'):
        return [ self.get_first(id_field, instance_id) for instance_id in instance_id_list ]

    @classmethod
    def SubIds(cls, id_field=b'id', sort_by=None, reverse=False):
        return [ getattr(klass, id_field) for _, klass in cls.Subclasses(sort_by=sort_by, reverse=reverse)
               ]

    def sub_ids(self, id_field=b'id', sort_by=None, reverse=False):
        return [ getattr(instance, id_field) for _, instance in self.subclasses(sort_by=sort_by, reverse=reverse)
               ]

    @classmethod
    def BackAssign(cls, other_entity_klass, this_entity_backpopulate_field, other_entity_backpopulate_field, is_many_to_one=False):
        """
        Assign defined one side mapping relationship to other side.

        For example, each employee belongs to one department, then one department
        includes many employees. If you defined each employee's department,
        this method will assign employees to ``Department.employees`` field.
        This is an one to many (department to employee) example.

        Another example would be, each employee has multiple tags. If you defined
        tags for each employee, this method will assign employees to
        ``Tag.employees`` field. This is and many to many (employee to tag) example.

        Support:

        - many to many mapping
        - one to many mapping

        :param other_entity_klass: a :class:`Constant` class.
        :param this_entity_backpopulate_field: str
        :param other_entity_backpopulate_field: str
        :param is_many_to_one: bool
        :return:
        """
        data = dict()
        for _, other_klass in other_entity_klass.Subclasses():
            other_field_value = getattr(other_klass, this_entity_backpopulate_field)
            if isinstance(other_field_value, (tuple, list)):
                for self_klass in other_field_value:
                    self_key = self_klass.__name__
                    try:
                        data[self_key].append(other_klass)
                    except KeyError:
                        data[self_key] = [
                         other_klass]

            elif other_field_value is not None:
                self_klass = other_field_value
                self_key = self_klass.__name__
                try:
                    data[self_key].append(other_klass)
                except KeyError:
                    data[self_key] = [
                     other_klass]

        if is_many_to_one:
            new_data = dict()
            for key, value in data.items():
                try:
                    new_data[key] = value[0]
                except:
                    pass

            data = new_data
        for self_key, other_klass_list in data.items():
            setattr(getattr(cls, self_key), other_entity_backpopulate_field, other_klass_list)

        return

    @classmethod
    def dump(cls):
        """Dump data into a dict.

        .. versionadded:: 0.0.2
        """
        d = OrderedDict(cls.Items())
        d[b'__classname__'] = cls.__name__
        for attr, klass in cls.Subclasses():
            d[attr] = klass.dump()

        return OrderedDict([(cls.__name__, d)])

    @classmethod
    def load(cls, data):
        """Construct a Constant class from it's dict data.

        .. versionadded:: 0.0.2
        """
        if len(data) == 1:
            for key, value in data.items():
                if b'__classname__' not in value:
                    raise ValueError
                name = key
                bases = (Constant,)
                attrs = dict()
                for k, v in value.items():
                    if isinstance(v, dict):
                        if b'__classname__' in v:
                            attrs[k] = cls.load({k: v})
                        else:
                            attrs[k] = v
                    else:
                        attrs[k] = v

            return type(name, bases, attrs)
        raise ValueError

    @classmethod
    def pprint(cls):
        """Pretty print it's data.

        .. versionadded:: 0.0.2
        """
        pprint(cls.dump())

    @classmethod
    def jprint(cls):
        """Json print it's data.

        .. versionadded:: 0.0.2
        """
        print(json.dumps(cls.dump(), pretty=4))


_reserved_attrs = {
 b'Items', b'Keys', b'Values',
 b'items', b'keys', b'values',
 b'ToDict', b'to_dict',
 b'Subclasses', b'subclasses',
 b'GetFirst', b'get_first',
 b'GetAll', b'get_all',
 b'ToIds', b'to_ids',
 b'SubIds', b'sub_ids',
 b'BackAssign',
 b'ToClasses', b'to_instances',
 b'dump', b'load', b'pprint', b'jprint'}

class Meta(type):
    """Meta class for :class:`Constant`.
    """

    def __new__(cls, name, bases, attrs):
        klass = super(Meta, cls).__new__(cls, name, bases, attrs)
        for attr in attrs:
            if attr in _reserved_attrs:
                if is_class_method(klass, attr) or is_regular_method(klass, attr):
                    if not getattr(klass, attr) == getattr(_Constant, attr):
                        msg = b'%s is a reserved attribute / method name' % attr
                        raise AttributeError(msg)
                else:
                    raise AttributeError(b'%r is not a valid attribute name' % attr)

        return klass


@add_metaclass(Meta)
class Constant(_Constant):
    pass


def is_same_dict(d1, d2):
    """Test two dictionary is equal on values. (ignore order)
    """
    for k, v in d1.items():
        if isinstance(v, dict):
            is_same_dict(v, d2[k])
        elif not d1[k] == d2[k]:
            raise AssertionError

    for k, v in d2.items():
        if isinstance(v, dict):
            is_same_dict(v, d1[k])
        elif not d1[k] == d2[k]:
            raise AssertionError


if __name__ == b'__main__':

    class Food(Constant):

        class Fruit:
            id = 1
            name = b'fruit'

            class Apple:
                id = 1
                name = b'apple'

                class RedApple:
                    id = 1
                    name = b'red apple'

                class GreenApple:
                    id = 2
                    name = b'green apple'

            class Banana:
                id = 2
                name = b'banana'

                class YellowBanana:
                    id = 1
                    name = b'yellow banana'

                class GreenBanana:
                    id = 2
                    name = b'green banana'

        class Meat:
            id = 2
            name = b'meat'

            class Pork:
                id = 1
                name = b'pork'

            class Beef:
                id = 2
                name = b'beef'


    food = Food()