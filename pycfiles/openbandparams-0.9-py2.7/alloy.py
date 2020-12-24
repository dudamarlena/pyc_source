# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/alloy.py
# Compiled at: 2015-11-05 19:16:51
from .parameter import Parameter, MethodParameter
__all__ = [
 'Alloy']

class Alloy(object):

    def __init__(self, name, elements, parameters=None):
        self.name = name
        self.elements = elements
        self._parameters = {}
        self._aliases = {}
        if parameters is not None:
            for parameter in parameters:
                self.set_parameter(parameter)

        return

    def __eq__(self, other):
        return (type(self) == type(other) and self.name == other.name and self.elements == other.elements,
         self._parameters == other._parameters)

    def __getattribute__(self, name):
        if name in ('_parameters', '_aliases'):
            return super(Alloy, self).__getattribute__(name)
        else:
            if name in self._parameters:
                return self._parameters[name]
            if name in self._aliases:
                return self._parameters[self._aliases[name]]
            try:
                item = super(Alloy, self).__getattribute__(name)
            except AttributeError as e:
                msg = e.message.replace('object', ("object '{}'").format(self.name))
                raise AttributeError(msg)

            if isinstance(item, MethodParameter):
                return item.bind(alloy=self)
            return item

    def __str__(self):
        return self.name

    def latex(self):
        """
        Returns a LaTeX representation of the alloy.
        """
        raise NotImplementedError()

    def element_fraction(self, element):
        """
        Returns the atomic fraction of the given ``element``.
        """
        raise NotImplementedError()

    def _add_parameter(self, parameter):
        """
        Force adds a `Parameter` object to the instance.
        """
        if isinstance(parameter, MethodParameter):
            parameter = parameter.bind(alloy=self)
        self._parameters[parameter.name] = parameter
        for alias in parameter.aliases:
            self._aliases[alias] = parameter

    def add_parameter(self, parameter, overload=False):
        """
        Adds a `Parameter` object to the instance.
        
        If a `Parameter` with the same name or alias has already been added
        and `overload` is False (the default), a `ValueError` is thrown.
        
        If a class member or method with the same name or alias is already
        defined, a `ValueError` is thrown, regardless of the value of overload.
        """
        if not isinstance(parameter, Parameter):
            raise TypeError('`parameter` must be an instance of `Parameter`')
        if hasattr(self, parameter.name):
            item = getattr(self, parameter.name)
            if not isinstance(item, Parameter):
                raise ValueError(('"{}" is already a class member or method.').format(parameter.name))
            elif not overload:
                raise ValueError(('Parameter "{}" has already been added and overload is False.').format(parameter.name))
        if parameter.name in self._parameters and not overload:
            raise ValueError(('Parameter "{}" has already been added and overload is False.').format(parameter.name))
        for alias in parameter.aliases:
            if alias in self._aliases and not overload:
                raise ValueError(('Alias "{}" has already been added and overload is False.').format(parameter.name))

        self._add_parameter(parameter)

    def set_parameter(self, parameter):
        """
        Same as calling ``add_parameter`` with ``overload=True``
        """
        self.add_parameter(parameter, overload=True)

    def has_parameter(self, name):
        """
        Returns True if the named parameter is present, or False, otherwise.
        """
        return self.get_parameter(name, default=None) is not None

    def get_parameter(self, name, default=None):
        """
        Returns the named parameter if present, or the value of `default`,
        otherwise.
        """
        if hasattr(self, name):
            item = getattr(self, name)
            if isinstance(item, Parameter):
                return item
        return default

    def get_unique_parameters(self):
        """
        Returns a list of the unique parameters (no duplicates).
        """
        parameters = self._parameters.values()
        for name in dir(self):
            item = getattr(self, name)
            if isinstance(item, Parameter):
                if item.name not in self._parameters:
                    parameters.append(item)

        return parameters