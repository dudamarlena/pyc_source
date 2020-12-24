# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/brainfreeze/properties.py
# Compiled at: 2008-11-13 00:52:50
"""OneToOne MapperProperty and Python Property implementations"""
from sqlalchemy import exceptions as sa_exc
from sqlalchemy.sql import and_
from sqlalchemy.orm.interfaces import PropComparator
from sqlalchemy.orm.properties import PropertyLoader, ColumnProperty, ComparableProperty
from sqlalchemy.ext.associationproxy import AssociationProxy
__all__ = [
 'OneToOneProxy', 'OneToOneMapperProperty',
 'OneToOnePropertyLoader', 'one_to_one']

class OneToOneProxy(AssociationProxy):
    """Property that proxies attribute access to columns on a related object.
    
    >>> class Publisher(object):
    ...     def __init__(self, name=None, address=None):
    ...         self.name = name
    ...         self.address = address

    >>> class Book(object):
    ...    def __init__(self, title=None, author=None, publisher=None):
    ...        self.title = title
    ...        self.author = author
    ...        self.publisher = publisher
    ...
    ...    publisher_name = OneToOneProxy('publisher_name', Publisher, 'name')
    ...    publisher_address = OneToOneProxy('publisher_address', Publisher, 'address')

    ... random_house = Publisher(name="Random House", address="NYC")
    ... beloved = Book(title='Beloved', author='Toni Morrison', publisher=random_house)

    ... beloved.publisher is random_house
    True

    .. beloved.publisher.name is beloved.publisher_name
    True
    
    """

    def __init__(self, relation_name, relation_class, attr_name):
        creator = lambda val: relation_class(**{attr_name: val})
        super(OneToOneProxy, self).__init__(relation_name, attr_name, creator=creator)
        assert self.target_collection == relation_name

    def __get__(self, obj, class_=None):
        """Until Alchemy is patched... """
        if obj is None:
            return self
        target = getattr(obj, self.target_collection, None)
        if target is None:
            return
        else:
            return super(OneToOneProxy, self).__get__(obj, class_)
        return


class OneToOneMapperProperty(ComparableProperty):
    """Instruments a OneToOneProxy python property for use in query expressions.
    
    Queries on the mapped class will be modified to contain the join condition
    necessary to locate the proxied property.
    
    The property is also registered with the session's unit-of-work machinery,
    so that changes to the property will be persisted.
    
    """

    def __init__(self, proxy_property):
        """Construct a OneToOneMapperProperty.  
        
        proxy_property
            The python descriptor or property to layer comparison behavior on top of.

        """
        if not isinstance(proxy_property, OneToOneProxy):
            raise sa_exc.ArgumentError("Unsupported proxy type: '%s'" % type(proxy_property))
        super(OneToOneMapperProperty, self).__init__(one_to_one_comparator, proxy_property)


def one_to_one_comparator(prop, mapper):
    """Return an appropriate OneToOneComparator for the given property."""
    intermediary_obj = mapper.get_property(prop.descriptor.target_collection)
    target_prop = intermediary_obj.mapper.get_property(prop.key)
    if isinstance(target_prop, ColumnProperty):
        return OneToOneColumnComparator(prop, mapper, intermediary_obj, target_prop)
    elif isinstance(target_prop, PropertyLoader):
        return OneToOneRelationComparator(prop, mapper, intermediary_obj, target_prop)
    else:
        raise sa_exc.ArgumentError("Unsupported property type: '%s'" % type(prop))


class OneToOneComparator(PropComparator):
    """Base class for other OneToOne Comparators"""

    def __init__(self, prop, mapper, intermediary_obj, target_prop):
        self.intermediary = intermediary_obj
        self.target = target_prop
        self.join_clauses = self.intermediary.primaryjoin
        if self.intermediary.secondaryjoin:
            self.join_clauses = and_(self.join_clauses, self.intermediary.secondaryjoin)
        super(OneToOneComparator, self).__init__(prop, mapper)


class OneToOneColumnComparator(OneToOneComparator):
    """Comparator for a OneToOneProxy that's proxying to a ColumnProperty"""

    def __clause_element__(self):
        return self.target.columns[0]._annotate({'parententity': self.intermediary.mapper})

    def operate(self, op, *other, **kwargs):
        """Return 'where' clauses for this operation."""
        join_clauses = self.join_clauses
        op_clauses = op(self.__clause_element__(), *other, **kwargs)
        return and_(join_clauses, op_clauses)

    def reverse_operate(self, op, other, **kwargs):
        """Return 'where' clauses for this operation."""
        join_clauses = self.join_clauses
        column = self.__clause_element__()
        op_clauses = op(column._bind_param(other), column, **kwargs)
        return and_(join_clauses, op_clauses)


class OneToOneRelationComparator(OneToOneComparator):
    """Comparator for a OneToOneProxy that's proxying to a PropertyLoader property relation"""

    def operate(self, op, *other, **kwargs):
        """Return 'where' clauses for this operation."""
        join_clauses = self.join_clauses
        op_clauses = op(self, *other, **kwargs)
        return sql.and_(join_clauses, op_clauses)

    def reverse_operate(self, op, other, **kwargs):
        return self.operate(self, op, *other, **kwargs)

    def __eq__(self, other):
        if other is None:
            raise sa_exc.InvalidRequestError('NOT IMPLEMENTED!')
        elif self.target.uselist:
            raise sa_exc.InvalidRequestError('NOT IMPLEMENTED!')
        else:
            return self.target._optimized_compare(other)
        return


class OneToOnePropertyLoader(PropertyLoader):
    """PropertyLoader that proxies access to all columns on a related object.
    
    Because this PropertyLoader adds other properties, it must be added
    after the mapper's ``properties`` mapping is already defined, 
    meaning it must be added using ``my_mapper.add_property`` after the
    mapper has already defined.
    """

    def __init__(self, *args, **kwargs):
        kwargs['uselist'] = False
        super(OneToOnePropertyLoader, self).__init__(*args, **kwargs)

    def do_init(self):
        super(OneToOnePropertyLoader, self).do_init()
        relation_name = self.key
        relation_class = self.argument
        for (prop_key, prop) in self.mapper._props.iteritems():
            if isinstance(prop, ColumnProperty) and prop.columns[0] in self.remote_side:
                continue
            proxy_property = OneToOneProxy(relation_name, relation_class, prop_key)
            setattr(self.parent.class_, prop_key, proxy_property)
            mapper_property = OneToOneMapperProperty(proxy_property)
            self.parent._init_properties[prop_key] = mapper_property
            self.parent._compile_property(prop_key, mapper_property, True)


def one_to_one(*args, **kwargs):
    return OneToOnePropertyLoader(*args, **kwargs)