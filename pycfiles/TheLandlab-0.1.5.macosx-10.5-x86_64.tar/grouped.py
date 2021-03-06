# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/field/grouped.py
# Compiled at: 2015-02-11 19:25:27
"""Store collections of data fields.
"""
import types, inspect
from .scalar_data_fields import ScalarDataFields, FieldError

class Error(Exception):
    """Base class for errors in this module."""
    pass


class GroupError(Error, KeyError):
    """Raise this error for a missing group name."""

    def __init__(self, group):
        self._group = group

    def __str__(self):
        return self._group


class ModelDataFields(object):
    """
    The ModelDataFields class holds a set of ScalarDataFields that are separated
    into *groups*. A typical use for this class would be to define the groups as
    being locations on a grid where the values are defined. For instance, the
    groups could be *node*, *cell*, *link*, and *face*.

    Most of the method functions for ModelDataFields are the same as those for
    the ScalarDataFields class but with the first argument being a string that
    defines the group name.

    Attributes
    ----------
    groups

    See Also
    --------
    landlab.field.ScalarDataFields : Data fields within a *group* are
        stored as :class:`landlab.field.ScalarDataFields`.
    landlab.grid.ModelGrid : Inherits from ModelDataFields.

    Examples
    --------

    Create two groups of data fields defined at *node* and *cell*. Each set can
    have a differenct number of values.

    >>> from landlab.field import ModelDataFields
    >>> fields = ModelDataFields()
    >>> fields.new_field_location('node', 12)
    >>> fields.new_field_location('cell', 2)

    Create some new value arrays for each of the data fields.

    >>> fields.ones('node')
    array([ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.])
    >>> fields.zeros('cell')
    array([ 0.,  0.])

    Create new value arrays and add them to the data fields. Because the data
    fields are in different groups (node and cell), they can have the same
    name.

    >>> fields.add_ones('node', 'topographic_elevation')
    array([ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.])
    >>> fields.at_node['topographic_elevation']
    array([ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.])

    >>> fields.add_ones('cell', 'topographic_elevation')
    array([ 1.,  1.])
    >>> fields.at_cell['topographic_elevation']
    array([ 1.,  1.])

    Each group acts as a `dict` so, for instance, to get the variables names
    in a group use the `keys` method,

    >>> fields.at_cell.keys()
    ['topographic_elevation']
    """

    def __init__(self, **kwds):
        self._groups = dict()
        super(ModelDataFields, self).__init__(**kwds)

    @property
    def groups(self):
        """List of group names.

        Returns
        -------
        set
            Set of quantity names.
        """
        return set(self._groups.keys())

    def has_group(self, group):
        """Check if a group exists.

        Parameters
        ----------
        group: str
            Name of the group.

        Returns
        -------
        boolean
            True if the field contains *group*, otherwise False.

        Examples
        --------
        Check if the field has the groups named *node* or *cell*.

        >>> from landlab.field import ModelDataFields
        >>> fields = ModelDataFields()
        >>> fields.new_field_location('node', 12)
        >>> fields.has_group('node')
        True
        >>> fields.has_group('cell')
        False
        """
        return group in self._groups

    def has_field(self, group, field):
        """Check if a field is in a group.

        Parameters
        ----------
        group: str
            Name of the group.
        field: str
            Name of the field.

        Returns
        -------
        boolean
            ``True`` if the group contains the field, otherwise ``False``.

        Examples
        --------
        Check if the field named ``topographic_elevation`` is contained
        in a group.

        >>> from landlab.field import ModelDataFields
        >>> fields = ModelDataFields()
        >>> fields.new_field_location('node', 12)
        >>> _ = fields.add_ones('node', 'topographic_elevation')
        >>> fields.has_field('node', 'topographic_elevation')
        True
        >>> fields.has_field('cell', 'topographic_elevation')
        False
        """
        try:
            return field in self[group]
        except KeyError:
            return False

    def keys(self, group):
        """List of field names in a group.

        Returns a list of the field names as a list of strings.

        Parameters
        ----------
        group : str
            Group name.

        Returns
        -------
        list
            List of field names.

        Examples
        --------
        >>> from landlab.field import ModelDataFields
        >>> fields = ModelDataFields()
        >>> fields.new_field_location('node', 4)
        >>> fields.keys('node')
        []
        >>> _ = fields.add_empty('node', 'topographic_elevation')
        >>> fields.keys('node')
        ['topographic_elevation']
        """
        return self[group].keys()

    def size(self, group):
        """Size of the arrays stored in a group.

        Parameters
        ----------
        group : str
            Group name.

        Returns
        -------
        int
            Array size.

        Examples
        --------
        >>> from landlab.field import ModelDataFields
        >>> fields = ModelDataFields()
        >>> fields.new_field_location('node', 4)
        >>> fields.size('node')
        4
        """
        return self[group].size

    def new_field_location(self, group, size):
        """Add a new quantity to a field.

        Create an empty group into which new fields can be added. The new group
        is created but no memory allocated yet. The dictionary of the new group
        can be through a new *at_* attribute of the class instance.

        Parameters
        ----------
        group: str
            Name of the new group to add to the field.
        size: int
            Number of elements in the new quantity.

        Raises
        ------
        ValueError
            If the field already contains the group.

        Examples
        --------
        Create a collection of fields and add two groups, *node* and *cell*,
        to it.

        >>> from landlab.field import ModelDataFields
        >>> fields = ModelDataFields()
        >>> fields.new_field_location('node', 12)
        >>> fields.new_field_location('cell', 2)

        The group names in the collection are retrieved with the *groups*
        attribute as a `set`.

        >>> names = list(fields.groups)
        >>> names.sort()
        >>> names
        ['cell', 'node']

        Access the new (empty) groups with the *at_* attributes.

        >>> fields.at_cell, fields.at_node
        ({}, {})
        """
        if self.has_group(group):
            raise ValueError('ModelDataFields already contains %s' % group)
        else:
            self._groups[group] = ScalarDataFields(size)
            setattr(self, 'at_' + group, self[group])

    def field_values(self, group, field):
        """Get values of a field.

        Given a *group* and a *field*, return a reference to the associated
        data array.

        Parameters
        ----------
        group: str
            Name of the group.
        field: str
            Name of the field withing *group*.

        Returns
        -------
        array
            The values of the field.

        Raises
        ------
        GroupError
            If *group* does not exits
        FieldError
            If *field* does not exits

        Examples
        --------
        Create a group of fields called *node*.

        >>> from landlab.field import ModelDataFields
        >>> fields = ModelDataFields()
        >>> fields.new_field_location('node', 4)

        Add a field, initialized to ones, called *topographic_elevation*
        to the *node* group. The *field_values* method returns a reference
        to the field's data.

        >>> _ = fields.add_ones('node', 'topographic_elevation')
        >>> fields.field_values('node', 'topographic_elevation')
        array([ 1.,  1.,  1.,  1.])

        Raise FieldError if *field* does not exist in *group*.

        >>> fields.field_values('node', 'planet_surface__temperature') # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        FieldError: planet_surface__temperature

        If *group* does not exists, Raise GroupError.

        >>> fields.field_values('cell', 'topographic_elevation') # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        GroupError: cell
        """
        return self[group][field]

    def field_units(self, group, field):
        """Get units for a field.

        Returns the unit string associated with the data array in *group* and
        *field*.

        Parameters
        ----------
        group: str
            Name of the group.
        field: str
            Name of the field withing *group*.

        Returns
        -------
        str
            The units of the field.

        Raises
        ------
        KeyError
            If either *field* or *group* does not exist.

        """
        return self[group].units[field]

    def empty(self, group, **kwds):
        """Uninitialized array whose size is that of the field.

        Return a new array of the data field size, without initializing
        entries. Keyword arguments are the same as that for the equivalent
        numpy function.

        Parameters
        ----------
        group : str
            Name of the group.

        See Also
        --------
        numpy.empty : See for a description of optional keywords.
        landlab.field.ModelDataFields.ones : Equivalent method that
            initializes the data to 1.
        landlab.field.ModelDataFields.zeros : Equivalent method that
            initializes the data to 0.

        Examples
        --------
        >>> from landlab.field import ModelDataFields
        >>> field = ModelDataFields()
        >>> field.new_field_location('node', 4)
        >>> field.empty('node') # doctest: +SKIP
        array([  2.31584178e+077,  -2.68156175e+154,   9.88131292e-324,
        ... 2.78134232e-309]) # Uninitialized memory

        Note that a new field is *not* added to the collection of fields.

        >>> field.keys('node')
        []
        """
        return self[group].empty(**kwds)

    def ones(self, group, **kwds):
        """Array, initialized to 1, whose size is that of the field.

        Return a new array of the data field size, filled with ones. Keyword
        arguments are the same as that for the equivalent numpy function.

        Parameters
        ----------
        group : str
            Name of the group.

        See Also
        --------
        numpy.ones : See for a description of optional keywords.
        landlab.field.ModelDataFields.empty : Equivalent method that
            does not initialize the new array.
        landlab.field.ModelDataFields.zeros : Equivalent method that
            initializes the data to 0.

        Examples
        --------
        >>> from landlab.field import ModelDataFields
        >>> field = ModelDataFields()
        >>> field.new_field_location('node', 4)
        >>> field.ones('node')
        array([ 1.,  1.,  1.,  1.])
        >>> field.ones('node', dtype=int)
        array([1, 1, 1, 1])

        Note that a new field is *not* added to the collection of fields.

        >>> field.keys('node')
        []
        """
        return self[group].ones(**kwds)

    def zeros(self, group, **kwds):
        """Array, initialized to 0, whose size is that of the field.

        Parameters
        ----------
        group : str
            Name of the group.

        Return a new array of the data field size, filled with zeros. Keyword
        arguments are the same as that for the equivalent numpy function.

        See Also
        --------
        numpy.zeros : See for a description of optional keywords.
        landlab.field.ModelDataFields.empty : Equivalent method that does not
            initialize the new array.
        landlab.field.ModelDataFields.ones : Equivalent
            method that initializes the data to 1.

        Examples
        --------
        >>> from landlab.field import ModelDataFields
        >>> field = ModelDataFields()
        >>> field.new_field_location('node', 4)
        >>> field.zeros('node')
        array([ 0.,  0.,  0.,  0.])

        Note that a new field is *not* added to the collection of fields.

        >>> field.keys('node')
        []
        """
        return self[group].zeros(**kwds)

    def add_empty(self, group, name, **kwds):
        """Create and add an uninitialized array of values to the field.

        Create a new array of the data field size, without initializing
        entries, and add it to the field as *name*. The *units* keyword gives
        the units of the new fields as a string. Remaining keyword arguments
        are the same as that for the equivalent numpy function.

        Parameters
        ----------
        group : str
            Name of the group.
        name : str
            Name of the new field to add.
        units : str, optional
            Optionally specify the units of the field.

        Returns
        -------
        array :
            A reference to the newly-created array.

        See Also
        --------
        numpy.empty : See for a description of optional keywords.
        landlab.field.ModelDataFields.empty : Equivalent method that
            does not initialize the new array.
        landlab.field.ModelDataFields.zeros : Equivalent method that
            initializes the data to 0.
        """
        units = kwds.pop('units', None)
        return self.add_field(group, name, ModelDataFields.empty(self, group, **kwds), units=units)

    def add_ones(self, group, name, units=None, **kwds):
        """Create and add an array of values, initialized to 1, to the field.

        Create a new array of the data field size, filled with ones, and
        add it to the field as *name*. The *units* keyword gives the units of
        the new fields as a string. Remaining keyword arguments are the same
        as that for the equivalent numpy function.

        Parameters
        ----------
        group : str
            Name of the group.
        name : str
            Name of the new field to add.
        units : str, optional
            Optionally specify the units of the field.

        Returns
        -------
        array :
            A reference to the newly-created array.

        See Also
        --------
        numpy.ones : See for a description of optional keywords.
        andlab.field.ModelDataFields.add_empty : Equivalent method that
            does not initialize the new array.
        andlab.field.ModelDataFields.add_zeros : Equivalent method that
            initializes the data to 0.

        Examples
        --------
        Add a new, named field to a collection of fields.

        >>> from landlab.field import ModelDataFields
        >>> field = ModelDataFields()
        >>> field.new_field_location('node', 4)
        >>> field.add_ones('node', 'topographic_elevation')
        array([ 1.,  1.,  1.,  1.])
        >>> field.keys('node')
        ['topographic_elevation']
        >>> field['node']['topographic_elevation']
        array([ 1.,  1.,  1.,  1.])
        >>> field.at_node['topographic_elevation']
        array([ 1.,  1.,  1.,  1.])
        """
        units = kwds.pop('units', None)
        return self.add_field(group, name, ModelDataFields.ones(self, group, **kwds), units=units)

    def add_zeros(self, group, name, units=None, **kwds):
        """Create and add an array of values, initialized to 0, to the field.

        Create a new array of the data field size, filled with zeros, and
        add it to the field as *name*. The *units* keyword gives the units of
        the new fields as a string. Remaining keyword arguments are the same
        as that for the equivalent numpy function.

        Parameters
        ----------
        group : str
            Name of the group.
        name : str
            Name of the new field to add.
        units : str, optional
            Optionally specify the units of the field.

        Returns
        -------
        array :
            A reference to the newly-created array.

        See also
        --------
        numpy.zeros : See for a description of optional keywords.
        landlab.field.ScalarDataFields.add_empty : Equivalent method that
            does not initialize the new array.
        landlab.field.ScalarDataFields.add_ones : Equivalent method that
            initializes the data to 1.
        """
        units = kwds.pop('units', None)
        return self.add_field(group, name, ModelDataFields.zeros(self, group, **kwds), units=units)

    def add_field(self, group, name, value_array, **kwds):
        """add_field(group, name, value_array, units='-', copy=False, noclobber=False)
        Add an array of values to the field.

        Add an array of data values to a collection of fields and associate it
        with the key, *name*. Use the *copy* keyword to, optionally, add a
        copy of the provided array.

        Parameters
        ----------
        group : str
            Name of the group.
        name : str
            Name of the new field to add.
        value_array : numpy.array
            Array of values to add to the field.
        units : str, optional
            Optionally specify the units of the field.
        copy : boolean, optional
            If True, add a *copy* of the array to the field. Otherwise save add
            a reference to the array.
        noclobber : boolean, optional
            Raise an exception if adding to an already existing field.

        Returns
        -------
        numpy.array
            The data array added to the field. Depending on the *copy*
            keyword, this could be a copy of *value_array* or *value_array*
            itself.

        Raises
        ------
        ValueError :
            If *value_array* has a size different from the field.

        Examples
        --------
        >>> import numpy as np
        >>> from landlab.field import ModelDataFields
        >>> field = ModelDataFields()
        >>> field.new_field_location('node', 4)
        >>> values = np.ones(4, dtype=int)
        >>> field.add_field('node', 'topographic_elevation', values)
        array([1, 1, 1, 1])

        A new field is added to the collection of fields. The saved value
        array is the same as the one initially created.

        >>> field.at_node['topographic_elevation'] is values
        True

        If you want to save a copy of the array, use the *copy* keyword. In
        addition, adding values to an existing field will remove the reference
        to the previously saved array. The *noclobber* keyword changes this
        behavior to raise an exception in such a case.

        >>> field.add_field('node', 'topographic_elevation', values, copy=True)
        array([1, 1, 1, 1])
        >>> field.at_node['topographic_elevation'] is values
        False
        >>> field.add_field('node', 'topographic_elevation', values, noclobber=True) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        FieldError: topographic_elevation
        """
        return self[group].add_field(name, value_array, **kwds)

    def set_units(self, group, name, units):
        """Set the units for a field of values.

        Parameters
        ----------
        group : str
            Name of the group.
        name: str
            Name of the field.
        units: str
            Units for the field

        Raises
        ------
        KeyError
            If the named field does not exist.
        """
        self[group].set_units(name, units)

    def __getitem__(self, group):
        try:
            return self._groups[group]
        except KeyError:
            raise GroupError(group)