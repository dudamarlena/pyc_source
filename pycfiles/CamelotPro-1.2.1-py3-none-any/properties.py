# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/orm/properties.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = "\nThis module provides support for defining properties on your entities. It both\nprovides, the `Property` class which acts as a building block for common\nproperties such as fields and relationships (for those, please consult the\ncorresponding modules), but also provides some more specialized properties,\nsuch as `ColumnProperty` and `Synonym`. It also provides the GenericProperty\nclass which allows you to wrap any SQLAlchemy property, and its DSL-syntax\nequivalent: has_property_.\n\n`has_property`\n--------------\nThe ``has_property`` statement allows you to define properties which rely on\ntheir entity's table (and columns) being defined before they can be declared\nthemselves. The `has_property` statement takes two arguments: first the name of\nthe property to be defined and second a function (often given as an anonymous\nlambda) taking one argument and returning the desired SQLAlchemy property. That\nfunction will be called whenever the entity table is completely defined, and\nwill be given the .c attribute of the entity as argument (as a way to access\nthe entity columns).\n\nHere is a quick example of how to use ``has_property``.\n\n.. sourcecode:: python\n\n    class OrderLine(Entity):\n        has_field('quantity', Float)\n        has_field('unit_price', Float)\n        has_property('price',\n                     lambda c: column_property(\n                         (c.quantity * c.unit_price).label('price')))\n"
from sqlalchemy import orm
from .statements import ClassMutator

class EntityBuilder(object):
    """
    Abstract base class for all entity builders. An Entity builder is a class
    of objects which can be added to an Entity (usually by using special
    properties or statements) to "build" that entity. Building an entity,
    meaning to add columns to its "main" table, create other tables, add
    properties to its mapper, ... To do so an EntityBuilder must override the
    corresponding method(s). This is to ensure the different operations happen
    in the correct order (for example, that the table is fully created before
    the mapper that use it is defined).
    """

    def create_pk_cols(self):
        pass

    def create_non_pk_cols(self):
        pass

    def before_table(self):
        pass

    def create_tables(self):
        """
        Subclasses may override this method to create tables.
        """
        pass

    def after_table(self):
        pass

    def create_properties(self):
        """
        Subclasses may override this method to add properties to the involved
        entity.
        """
        pass

    def before_mapper(self):
        pass

    def after_mapper(self):
        pass

    def finalize(self):
        pass


class CounterMeta(type):
    """
    A simple meta class which adds a ``_counter`` attribute to the instances of
    the classes it is used on. This counter is simply incremented for each new
    instance.
    """
    counter = 0

    def __call__(self, *args, **kwargs):
        instance = type.__call__(self, *args, **kwargs)
        instance.counter = CounterMeta.counter
        CounterMeta.counter += 1
        return instance


class Property(EntityBuilder):
    """
    Abstract base class for all properties of an Entity that are not handled
    by Declarative but should be handled by EntityMeta before a new Entity
    subclass is constructed
    """
    __metaclass__ = CounterMeta

    def __init__(self, *args, **kwargs):
        self.entity = None
        self.name = None
        return

    def attach(self, entity, name):
        """Attach this property to its entity, using 'name' as name.

        Properties will be attached in the order they were declared.
        """
        self.entity = entity
        self.name = name

    def __repr__(self):
        return 'Property(%s, %s)' % (self.name, self.entity)


class DeferredProperty(Property):
    """Abstract base class for all properties of an Entity that are not 
    handled by Declarative but should be handled after a mapper was
    configured"""

    def _setup_reverse(self, key, rel, target_cls):
        """Setup bidirectional behavior between two relationships."""
        reverse = self.kw.get('reverse')
        if reverse:
            reverse_attr = getattr(target_cls, reverse)
            if not isinstance(reverse_attr, DeferredProperty):
                reverse_attr.property._add_reverse_property(key)
                rel._add_reverse_property(reverse)


class GenericProperty(DeferredProperty):
    """
    Generic catch-all class to wrap an SQLAlchemy property.

    .. sourcecode:: python

        class OrderLine(Entity):
            quantity = Field(Float)
            unit_price = Field(Numeric)
            price = GenericProperty(lambda c: column_property(
                             (c.quantity * c.unit_price).label('price')))
    """
    process_order = 4

    def __init__(self, prop, *args, **kwargs):
        super(GenericProperty, self).__init__()
        self.prop = prop
        self.args = args
        self.kwargs = kwargs

    def create_properties(self):
        table = orm.class_mapper(self.entity).local_table
        if hasattr(self.prop, '__call__'):
            prop_value = self.prop(table.c)
        else:
            prop_value = self.prop
        prop_value = self.evaluate_property(prop_value)
        setattr(self.entity, self.name, prop_value)

    def evaluate_property(self, prop):
        if self.args or self.kwargs:
            raise Exception('superfluous arguments passed to GenericProperty')
        return prop

    def _config(self, cls, mapper, key):
        if hasattr(self.prop, '__call__'):
            prop_value = self.prop(mapper.local_table.c)
        else:
            prop_value = self.prop
        setattr(cls, key, prop_value)


class ColumnProperty(GenericProperty):
    """A specialized form of the GenericProperty to generate SQLAlchemy
    ``column_property``'s.

    It takes a function (often given as an anonymous lambda) as its first
    argument. Other arguments and keyword arguments are forwarded to the
    column_property construct. That first-argument function must accept exactly
    one argument and must return the desired (scalar-returning) SQLAlchemy
    ClauseElement.

    The function will be called whenever the entity table is completely
    defined, and will be given
    the .c attribute of the table of the entity as argument (as a way to
    access the entity columns). The ColumnProperty will first wrap your
    ClauseElement in an
    "empty" label (ie it will be labelled automatically during queries),
    then wrap that in a column_property.

    .. sourcecode:: python

        class OrderLine(Entity):
            quantity = Field(Float)
            unit_price = Field(Numeric)
            price = ColumnProperty(lambda c: c.quantity * c.unit_price,
                                   deferred=True)

    Please look at the `corresponding SQLAlchemy
    documentation <http://docs.sqlalchemy.org/en/rel_0_7/orm/mapper_config.html#sql-expressions-as-mapped-attributes>`_ 
    for details."""

    def evaluate_property(self, prop):
        return orm.column_property(prop.label(None), *self.args, **self.kwargs)


class has_property(ClassMutator):

    def process(self, entity_dict, name, prop, *args, **kwargs):
        entity_dict[name] = GenericProperty(prop, *args, **kwargs)