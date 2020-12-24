# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/dataql/solvers/base.py
# Compiled at: 2015-06-15 17:25:09
# Size of source mod 2**32: 13219 bytes
"""``base`` module of ``dataql.solvers``.

This module holds the base solvers, one for simple attributes (``AttributeSolver``, one for
objects (``ObjectSolver``), and one for lists (``ListSolver``).

Notes
-----
When we talk about "resources", we talk about instances of classes defined in ``dataql.resources``
(or inherited classes of course)

"""
from collections import Iterable
from dataql.resources import NamedArg, PosArg, Field, Filter, Object, List

class Solver:
    __doc__ = 'Base class for all solvers.\n\n    The main entry point of a solver is the ``solve_resource`` method, which must be defined\n    for every solver.\n\n    Attributes\n    ----------\n    solvable_resources : tuple (class attribute)\n        Holds the resource classes (from ``dataql.resources``) that can be solved by this solver.\n        Must be defined in each sub-classes.\n    registry : dataql.solvers.registry.Registry\n        The registry that instantiated this solver.\n    source : dataql.solvers.registry.Source\n        The ``Source`` object that will be used to solve a value.\n\n    '
    solvable_resources = ()

    def __init__(self, registry, source):
        """Init the solver.

        Arguments
        ---------
        registry : dataql.solvers.registry.Registry
            The registry to use to get the source and solve sub-resources if any.
        source : ?
            An instance of a class (or the class itself) that must be available in the registry.

        """
        self.registry = registry
        self.source = self.registry[source]

    def solve_resource(self, value, resource):
        """Solve a resource with a value.

        Arguments
        ---------
        value : ?
            A value to solve in combination with the given resource. Must be a value that has
            an attribute named as the resource name.
        resource : Resource
            An instance of a subclass of ``dataql.resources.Resource`` to solve with the given
            value.

        Returns
        -------
        (depends on the implementation of the ``cast`` method.

        Notes
        -----
        This method simply calls ``solve_attribute_and_filters``, then ``cast`` with the result.
        To change the behavior, simply override one of these two methods.

        """
        result = self.solve_attribute_and_filters(value, resource)
        return self.cast(result, resource)

    def solve_attribute_and_filters(self, value, resource):
        """Solve a resource with a value, without casting.

        Arguments
        ---------
        value : ?
            A value to solve in combination with the given resource. Must be a value that has
            an attribute named as the resource name.
        resource : Resource
            An instance of a subclass of ``dataql.resources.Resource`` to solve with the given
            value.

        Returns
        -------
        The content of the attribute from ``value`` defined by the resource, with all filters
        applied.

        Example
        -------

        >>> from dataql.solvers.registry import Registry
        >>> registry = Registry()
        >>> from datetime import date
        >>> registry.register(date, allow_class=True)
        >>> registry.register(str, allow_class=True)
        >>> solver = Solver(registry, date)
        >>> solver.solve_attribute_and_filters(date, Field('fromtimestamp',
        ...     args=[PosArg(1433109600)],
        ...     filters=[
        ...         Filter(name='replace', args=[NamedArg('year', '=', 2014)]),
        ...         Filter(name='strftime', args=[PosArg('%F')]),
        ...         Filter(name='replace', args=[PosArg('2014'), PosArg('2015')]),
        ...     ]
        ... ))
        '2015-06-01'

        """
        args, kwargs = resource.get_args_and_kwargs()
        result = self.source.solve(value, resource.name, args, kwargs)
        for filter_ in resource.filters:
            args, kwargs = filter_.get_args_and_kwargs()
            source = self.registry[result]
            result = source.solve(result, filter_.name, args, kwargs)

        return result

    def cast(self, value, resource):
        """Convert the value got after ``solve_attribute_and_filters``.

        Must be implemented in subclasses.

        """
        raise NotImplementedError()

    @classmethod
    def can_solve(cls, resource):
        """Tells if the solver is able to resolve the given resource.

        Arguments
        ---------
        resource : subclass of ``dataql.resources.Resource``
            The resource to check if it is solvable by the current solver class

        Returns
        -------
        boolean
            ``True`` if the current solver class can solve the given resource, ``False`` otherwise.

        Example
        -------

        >>> AttributeSolver.solvable_resources
        (<class 'dataql.resources.Field'>,)
        >>> AttributeSolver.can_solve(Field('foo'))
        True
        >>> AttributeSolver.can_solve(Object('bar'))
        False

        """
        for solvable_resource in cls.solvable_resources:
            if isinstance(resource, solvable_resource):
                return True

        return False


class AttributeSolver(Solver):
    __doc__ = "Solver aimed to retrieve attributes from values.\n\n    This solver can only handle ``dataql.resources.Field`` resources.\n\n    Attributes\n    ----------\n    solvable_resources : tuple (class attribute)\n        Holds the resource classes (from ``dataql.resources``) that can be solved by this solver.\n\n    Example\n    -------\n\n    >>> from dataql.solvers.registry import Registry\n    >>> registry = Registry()\n    >>> from datetime import date\n    >>> registry.register(date)\n    >>> solver = AttributeSolver(registry, date)\n    >>> solver.solve_resource(date(2015, 6, 1), Field('year'))\n    2015\n\n    "
    solvable_resources = (
     Field,)

    def cast(self, value, resource):
        """Cast the value to an acceptable one.

        Only these kinds of values are returned as is:
        - str
        - int
        - float
        - True
        - False
        - None

        For all others values, it will be casted using ``self.cast_default`` (with convert the
        value to a string in the default implementation).

        Arguments
        ---------
        value : ?
            The value to be casted.

        Returns
        -------
        str | int | float | True | False | None
            The casted value.

        Example
        -------

        >>> from dataql.solvers.registry import Registry
        >>> registry = Registry()
        >>> from datetime import date
        >>> registry.register(date)
        >>> solver = AttributeSolver(registry, date)
        >>> solver.cast('foo', None)
        'foo'
        >>> solver.cast(11, None)
        11
        >>> solver.cast(1.1, None)
        1.1
        >>> solver.cast(True, None)
        True
        >>> solver.cast(False, None)
        False
        >>> solver.cast(date(2015, 6, 1), None)
        '2015-06-01'
        >>> solver.cast(None, None)

        """
        if value in (True, False, None):
            return value
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            return value
        return self.cast_default(value, resource)

    def cast_default(self, value, resource):
        """Cast a value using a default converter, ``str()``.

        Arguments
        ---------
        value : ?
            The value to be casted.
        attribute : str
            The name of the attribute from which the value was fetched.

        Returns
        -------
        str
            The casted value.

        Example
        -------

        >>> from dataql.solvers.registry import Registry
        >>> registry = Registry()
        >>> from datetime import date
        >>> registry.register(date)
        >>> solver = AttributeSolver(registry, date)
        >>> solver.cast_default(date(2015, 6, 1), None)
        '2015-06-01'
        >>> solver.cast_default(date, None)
        "<class 'datetime.date'>"

        """
        return str(value)


class MultiResourcesBaseSolver(Solver):
    __doc__ = 'A base class for solver for resources with sub-resources.\n\n    Notes\n    -----\n    This base class simply provides a ``solve_subresources`` method to return a dict containing\n    each solved resources.\n\n    '

    def solve_subresources(self, value, resources):
        """Solve many resources from a value.

        Arguments
        ---------
        value : ?
            The value to get some resources from.
        resources : iterable[dataql.resource.Resource]
            A list (or other iterable) of resources (instances of ``dataql.resource.Resource``
            subclasses.

        Returns
        -------
        dict
            A dictionary containing the wanted resources for the given value.
            Key are the ``entry_name`` attributes of the resources, and the values are the
            solved values.

        Example
        -------
        >>> from dataql.solvers.registry import Registry
        >>> registry = Registry()
        >>> from datetime import date
        >>> registry.register(date)
        >>> solver = ObjectSolver(registry, date)
        >>> d = solver.solve_subresources(date(2015, 6, 1), [
        ... Field('day'), Field('month'), Field('year')])
        >>> [(k, d[k]) for k in sorted(d)]
        [('day', 1), ('month', 6), ('year', 2015)]

        """
        return {r.entry_name:self.registry.solve(value, r) for r in resources}


class ObjectSolver(MultiResourcesBaseSolver):
    __doc__ = "Solver aimed to retrieve many attributes from values.\n\n    This solver can only handle ``dataql.resources.Object`` resources.\n\n    Example\n    -------\n\n        >>> from dataql.solvers.registry import Registry\n        >>> registry = Registry()\n        >>> from datetime import date\n        >>> registry.register(date)\n\n        # Create an object from which we'll want an object (``date``)\n        >>> from dataql.solvers.registry import EntryPoints\n        >>> obj = EntryPoints(registry,\n        ...     date = date(2015, 6, 1),\n        ... )\n\n        >>> solver = ObjectSolver(registry, obj.__class__)\n        >>> d = solver.solve_resource(\n        ...     obj,\n        ...     Object('date', resources=[Field('day'), Field('month'), Field('year')])\n        ... )\n        >>> [(k, d[k]) for k in sorted(d)]\n        [('day', 1), ('month', 6), ('year', 2015)]\n\n    "
    solvable_resources = (
     Object,)

    def cast(self, value, resource):
        """Get a dict with attributes from ``value``.

        Arguments
        ---------
        value : ?
            The value to get some resources from.
        resource : dataql.resources.Object
            An instance of ``dataql.resources.Object`` (or a sub-class)

        Returns
        -------
        dict
            A dictionary containing the wanted resources for the given value.
            Key are the ``entry_name`` attributes of the resources, and the values are the
            solved values.

        """
        return self.solve_subresources(value, resource.resources)


class ListSolver(MultiResourcesBaseSolver):
    __doc__ = "Solver aimed to retrieve many attributes from many values of the same type.\n\n    This solver can only handle ``dataql.resources.List`` resources.\n\n    Example\n    -------\n\n        >>> from dataql.solvers.registry import Registry\n        >>> registry = Registry()\n        >>> from datetime import date\n        >>> registry.register(date)\n\n        # Create an object from which we'll want a list (``dates``)\n        >>> from dataql.solvers.registry import EntryPoints\n        >>> obj = EntryPoints(registry,\n        ...     dates = [date(2015, 6, 1), date(2015, 6, 2)],\n        ... )\n\n        >>> solver = ListSolver(registry, obj.__class__)\n\n        >>> ds = list(solver.solve_resource(\n        ...     obj,\n        ...     List('dates', resources=[Field('day'), Field('month'), Field('year')])\n        ... ))\n        >>> [[(k, d[k]) for k in sorted(d)] for d in ds]\n        [[('day', 1), ('month', 6), ('year', 2015)], [('day', 2), ('month', 6), ('year', 2015)]]\n\n    "
    solvable_resources = (
     List,)

    def cast(self, value, resource):
        """Convert a list of objects in a list of dicts.

        Arguments
        ---------
        value : iterable
            The list (or other iterable) to get values to get some resources from.
        resource : dataql.resources.List
            An instance of ``dataql.resources.List`` (or a sub-class)

        Returns
        -------
        list[dict]
            A list of dictionaries containing the wanted resources for the given values.
            Key are the ``entry_name`` attributes of the resources, and the values are the
            solved values.

        """
        if not isinstance(value, Iterable):
            raise Exception('`%s` from source `%s` is not iterable' % (
             resource.name, self.source.name))
        return [self.solve_subresources(entry, resource.resources) for entry in value]