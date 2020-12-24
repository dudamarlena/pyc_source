# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/utils/decorators.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 14417 bytes
import numpy as np, inspect
from astropy.utils.decorators import wraps
from astropy.units.core import UnitsError, add_enabled_equivalencies
__all__ = [
 'ranged_quantity_input']

class RangedQuantityInput(object):

    @classmethod
    def as_decorator(cls, func=None, **kwargs):
        r"""
        A decorator for validating the units of arguments to functions.

        This decorator was adapted from Astropy's
        `~astropy.units.quantity_input`,
        but adds range checking and the possibilities to strip
        the units before feeding into the decorated function.
        It also allows to apply a new unit to the returned value
        (`~astropy.units.quantity_input` only does this in conjuction
        with type annotations).

        A `~astropy.units.UnitsError` will be raised if the unit
        attribute of the argument is not equivalent to the unit
        specified to the decorator or in the annotation. If the
        argument has no unit attribute, i.e. it is not a Quantity
        object, a `ValueError` will be raised.

        Where an equivalency is specified in the decorator, the
        function will be executed with that equivalency in force.

        Parameters
        ----------
        func : function
            The function to decorate.
        **kwargs : any number of key word arguments
            The function argument names and ranges that are to be checked
            for the decorated function. Must have the form
            `param=(min, max, unit)`, e.g.::

                @ranged_quantity_input(a=(0, 1, u.m), b=(0, None, u.s))
                def func(a, b):
                    return a ** 2, 1 / b

            will check that input `a` has unit of meters (or equivalent)
            and is in the range between zero and one meters; and that
            `b` is at least zero seconds.
        equivalencies : list of functions
            Equivalencies functions to apply (see `Astropy docs
            <http://docs.astropy.org/en/stable/units/equivalencies.html>`__).
        strip_input_units : bool, optional
            Whether to strip units from parameters. Only applied
            to parameters that are "registered" in the decorator,
            see examples. (default: False)
        output_unit : `~astropy.units.Unit` or tuple of `~astropy.units.Unit`, optional
            Add units to the return value(s) of the decorated function.
            Note that internally the given units are *multiplied* with
            the return values, which means you should only use this
            if you have stripped the units from the input (or otherwise
            made sure that the return values are unit-less).
        allow_none : bool, optional
            Allow to use `None` as default value; see examples.

        Returns
        -------
        ranged_quantity_input : function decorator
            Function decorator to check units and value ranges.

        Notes
        -----

        The checking of arguments inside variable arguments to a
        function is not supported (i.e. \*arg or \**kwargs).

        Examples
        --------

        In the most basic form, `~pycraf.utils.ranged_quantity_input`
        behaves like `~astropy.units.quantity_input`, but adds
        range checking::

            >>> import astropy.units as u
            >>> from pycraf.utils import ranged_quantity_input

            >>> @ranged_quantity_input(a=(0, 1, u.m))
            ... def func(a):
            ...     return a ** 2

            >>> func(0.5 * u.m)  # doctest: +FLOAT_CMP
            <Quantity 0.25 m2>

            >>> func(2 * u.m)
            Traceback (most recent call last):
            ...
            ValueError: Argument 'a' to function 'func' out of range
            (allowed 0 to 1 m).

        It is possible to disable range checking, for the lower, upper,
        or both bounds, e.g.::

            >>> @ranged_quantity_input(a=(0, None, u.m))
            ... def func(a):
            ...     return a ** 2

            >>> func(2 * u.m)  # doctest: +FLOAT_CMP
            <Quantity 4.0 m2>

        Often one wants to add units support to third-party functions,
        which expect simple types::

            >>> # this is defined somewhere else
            >>> def _func(a):
            ...     assert isinstance(a, float), 'No Way!'
            ...     return a ** 2

            >>> _func(0.5 * u.m)
            Traceback (most recent call last):
            ...
            AssertionError: No Way!

        We can do the following to the rescue::

            >>> @ranged_quantity_input(a=(0, 1, u.m), strip_input_units=True)
            ... def func(a):
            ...     return _func(a)

            >>> # which is the same as
            >>> # func = ranged_quantity_input(
            >>> #    a=(0, 1, u.m), strip_input_units=True
            >>> #    )(_func)

            >>> func(0.5 * u.m)  # doctest: +FLOAT_CMP
            0.25

        However, by doing this there are still no units for the output.
        We can fix this with the `output_unit` option::

            >>> @ranged_quantity_input(
            ...     a=(0, 1, u.m),
            ...     strip_input_units=True,
            ...     output_unit=u.m ** 2
            ...     )
            ... def func(a):
            ...     return _func(a)

            >>> func(0.5 * u.m)  # doctest: +FLOAT_CMP
            <Quantity 0.25 m2>

        If you have several return values (tuple), just provide a tuple
        of output units.

        The decorator also works flawlessly with default values::

            >>> @ranged_quantity_input(a=(0, 1, u.m))
            ... def func(a=0.5 * u.m):
            ...     return a ** 2

            >>> func()  # doctest: +FLOAT_CMP
            <Quantity 0.25 m2>

        However, sometimes one wants to use `None` as default, which will
        fail, because `None` has no unit::

            >>> @ranged_quantity_input(a=(0, 1, u.m))
            ... def func(a=None):
            ...     return a ** 2

            >>> func()
            Traceback (most recent call last):
            ...
            TypeError: Argument 'a' to function 'func' has no 'unit'
            attribute. You may want to pass in an astropy Quantity instead.

        One can use the `allow_none` option, to deal with such cases::

            >>> @ranged_quantity_input(a=(0, 1, u.m), allow_none=True)
            ... def func(a=None):
            ...     if a is None:
            ...         a = 0.5
            ...     return a ** 2

            >>> func()  # doctest: +FLOAT_CMP
            0.25

        and of course, the unit check still works,  if a something other
        than `None` is provided::

            >>> func(1 * u.s)
            Traceback (most recent call last):
            ...
            astropy.units.core.UnitsError: Argument 'a' to function
            'func' must be in units convertible to 'm'.

        """
        self = cls(**kwargs)
        if func is not None and not kwargs:
            return self(func)
        else:
            return self

    def __init__(self, func=None, **kwargs):
        self.kwargs = dict(kwargs)
        self.equivalencies = kwargs.pop('equivalencies', [])
        self.strip_input_units = kwargs.pop('strip_input_units', False)
        self.output_unit = kwargs.pop('output_unit', None)
        self.allow_none = kwargs.pop('allow_none', False)
        self.decorator_kwargs = kwargs

    def __call__(self, wrapped_function):
        wrapped_signature = inspect.signature(wrapped_function)

        @wraps(wrapped_function)
        def wrapper(*func_args, **func_kwargs):
            bound_args = wrapped_signature.bind(*func_args, **func_kwargs)
            for param in wrapped_signature.parameters.values():
                if param.kind in (inspect.Parameter.VAR_KEYWORD,
                 inspect.Parameter.VAR_POSITIONAL):
                    pass
                else:
                    if param.name not in bound_args.arguments and param.default is not param.empty:
                        bound_args.arguments[param.name] = param.default
                    arg = bound_args.arguments[param.name]
                    if param.name in self.decorator_kwargs:
                        target_min, target_max, target_unit = self.decorator_kwargs[param.name]
                    else:
                        continue
                    if target_unit is not inspect.Parameter.empty:
                        pass
                    if arg is None and self.allow_none:
                        pass
                    else:
                        try:
                            equivalent = arg.unit.is_equivalent(target_unit, equivalencies=self.equivalencies)
                            if not equivalent:
                                raise UnitsError("Argument '{0}' to function '{1}' must be in units convertible to '{2}'.".format(param.name, wrapped_function.__name__, target_unit.to_string()))
                        except AttributeError:
                            if hasattr(arg, 'unit'):
                                error_msg = "a 'unit' attribute without an 'is_equivalent' method"
                            else:
                                error_msg = "no 'unit' attribute"
                            raise TypeError("Argument '{0}' to function '{1}' has {2}. You may want to pass in an astropy Quantity instead.".format(param.name, wrapped_function.__name__, error_msg))

                        if target_min is not None:
                            quantity = bound_args.arguments[param.name]
                            value = quantity.to(target_unit).value
                            if np.any(value < target_min):
                                raise ValueError("Argument '{0}' to function '{1}' out of range (allowed {2} to {3} {4}).".format(param.name, wrapped_function.__name__, target_min, target_max, target_unit))
                            if target_max is not None:
                                quantity = bound_args.arguments[param.name]
                                value = quantity.to(target_unit).value
                                if np.any(value > target_max):
                                    raise ValueError("Argument '{0}' to function '{1}' out of range (allowed {2} to {3} {4}).".format(param.name, wrapped_function.__name__, target_min, target_max, target_unit))
                                if self.strip_input_units:
                                    bound_args.arguments[param.name] = bound_args.arguments[param.name].to(target_unit).value

            with add_enabled_equivalencies(self.equivalencies):
                result = wrapped_function(*bound_args.args, **bound_args.kwargs)
            if self.output_unit is not None:
                try:
                    if hasattr(result, '_fields'):
                        cls = result.__class__
                        return cls(*((r if u is None else r * u) for r, u in zip(result, self.output_unit)))
                    else:
                        return tuple((r if u is None else r * u) for r, u in zip(result, self.output_unit))
                except TypeError:
                    if self.output_unit is None:
                        return result
                    else:
                        return result * self.output_unit

            else:
                return result

        return wrapper


ranged_quantity_input = RangedQuantityInput.as_decorator