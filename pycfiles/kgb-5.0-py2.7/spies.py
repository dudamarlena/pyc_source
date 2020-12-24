# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kgb/spies.py
# Compiled at: 2020-04-10 23:22:42
from __future__ import absolute_import, unicode_literals
import copy, inspect, types
from kgb.errors import ExistingSpyError, IncompatibleFunctionError, InternalKGBError
from kgb.pycompat import iteritems, iterkeys, pyver, text_type
from kgb.signature import FunctionSig, _UNSET_ARG
from kgb.utils import is_attr_defined_on_ancestor

class SpyCall(object):
    """Records arguments made to a spied function call.

    SpyCalls are created and stored by a FunctionSpy every time it is
    called. They're accessible through the FunctionSpy's ``calls`` attribute.
    """

    def __init__(self, spy, args, kwargs):
        """Initialize the call.

        Args:
            spy (FunctionSpy):
                The function spy that the call was made on.

            args (tuple):
                A tuple of positional arguments from the spy. These correspond
                to positional arguments in the function's signature.

            kwargs (dict):
                A dictionary of keyword arguments from the spy. These
                correspond to keyword arguments in the function's signature.
        """
        self.spy = spy
        self.args = args
        self.kwargs = kwargs
        self.return_value = None
        self.exception = None
        return

    def called_with(self, *args, **kwargs):
        """Return whether this call was made with the given arguments.

        Not every argument and keyword argument made in the call must be
        provided to this method. These can be a subset of the positional and
        keyword arguments in the call, but cannot contain any arguments not
        made in the call.

        Args:
            *args (tuple):
                The positional arguments made in the call, or a subset of
                those arguments (starting with the first argument).

            **kwargs (dict):
                The keyword arguments made in the call, or a subset of those
                arguments.

        Returns:
            bool:
            ``True`` if the call's arguments match the provided arguments.
            ``False`` if they do not.
        """
        if len(args) > len(self.args):
            return False
        if self.args[:len(args)] != args:
            return False
        pos_args = self.spy._sig.arg_names
        if self.spy.func_type in (FunctionSpy.TYPE_BOUND_METHOD,
         FunctionSpy.TYPE_UNBOUND_METHOD):
            pos_args = pos_args[1:]
        all_args = dict(zip(pos_args, self.args))
        all_args.update(self.kwargs)
        for key, value in iteritems(kwargs):
            if key not in all_args or all_args[key] != value:
                return False

        return True

    def returned(self, value):
        """Return whether this call returned the given value.

        Args:
            value (object):
                The expected returned value from the call.

        Returns:
            bool:
            ``True`` if this call returned the given value. ``False`` if it
            did not.
        """
        return self.return_value == value

    def raised(self, exception_cls):
        """Return whether this call raised this exception.

        Args:
            exception_cls (type):
                The expected type of exception raised by the call.

        Returns:
            bool:
            ``True`` if this call raised the given exception type.
            ``False`` if it did not.
        """
        return self.exception is None and exception_cls is None or type(self.exception) is exception_cls

    def raised_with_message(self, exception_cls, message):
        """Return whether this call raised this exception and message.

        Args:
            exception_cls (type):
                The expected type of exception raised by the call.

            message (unicode):
                The expected message from the exception.

        Returns:
            bool:
            ``True`` if this call raised the given exception type and message.
            ``False`` if it did not.
        """
        return self.exception is not None and self.raised(exception_cls) and text_type(self.exception) == message

    def __repr__(self):
        return b'<SpyCall(args=%r, kwargs=%r, returned=%r, raised=%r>' % (
         self.args, self.kwargs, self.return_value, self.exception)


class FunctionSpy(object):
    """A spy infiltrating a function.

    A FunctionSpy takes the place of another function. It will record any
    calls made to the function for later inspection.

    By default, a FunctionSpy will allow the call to go through to the
    original function. This can be disabled by passing call_original=False
    when initiating the spy. If disabled, the original function will never be
    called.

    This can also be passed a call_fake parameter pointing to another
    function to call instead of the original. If passed, this will take
    precedence over call_original.
    """
    TYPE_FUNCTION = FunctionSig.TYPE_FUNCTION
    TYPE_BOUND_METHOD = FunctionSig.TYPE_BOUND_METHOD
    TYPE_UNBOUND_METHOD = FunctionSig.TYPE_UNBOUND_METHOD
    _PROXY_METHODS = [
     b'call_original', b'called_with', b'last_called_with',
     b'raised', b'last_raised', b'returned', b'last_returned',
     b'raised_with_message', b'last_raised_with_message',
     b'reset_calls', b'unspy']
    _FUNC_ATTR_DEFAULTS = {b'calls': [], b'called': False, 
       b'last_call': None}
    _spy_map = {}

    def __init__(self, agency, func, call_fake=None, call_original=True, owner=_UNSET_ARG):
        """Initialize the spy.

        This will begin spying on the provided function or method, injecting
        new code into the function to help record how it was called and
        what it returned, and adding methods and state onto the function
        for callers to access in order to get those results.

        Version Added:
            5.0:
            Added support for specifying an instance in ``owner`` when spying
            on bound methods using decorators that return plain functions.

        Args:
            agency (kgb.agency.SpyAgency):
                The spy agency that manages this spy.

            func (callable):
                The function or method to spy on.

            call_fake (callable, optional):
                The optional function to call when this function is invoked.

            call_original (bool, optional):
                Whether to call the original function when the spy is
                invoked. If ``False``, no function will be called.

                This is ignored if ``call_fake`` is provided.

            owner (type or object, optional):
                The owner of the function or method.

                If spying on an unbound method, this **must** be set to the
                class that owns it.

                If spying on a bound method that identifies as a plain
                function (which may happen if the method is decorated and
                dynamically returns a new function on access), this should
                be the instance of the object you're spying on.
        """
        self.init_frame = inspect.currentframe()
        if hasattr(func, b'spy'):
            raise ExistingSpyError(func)
        if not callable(func) or not hasattr(func, FunctionSig.FUNC_NAME_ATTR) or not (hasattr(func, FunctionSig.METHOD_SELF_ATTR) or hasattr(func, FunctionSig.FUNC_GLOBALS_ATTR)):
            raise ValueError(b'%r cannot be spied on. It does not appear to be a valid function or method.' % func)
        sig = FunctionSig(func=func, owner=owner)
        self._sig = sig
        if owner is not _UNSET_ARG and owner is not self.owner:
            if self.func_type == self.TYPE_FUNCTION:
                raise ValueError(b'This function has no owner, but an owner was passed to spy_on().')
            elif not hasattr(owner, self.func_name):
                raise ValueError(b'The owner passed does not contain the spied method.')
            elif self.func_type == self.TYPE_BOUND_METHOD or pyver[0] == 2 and self.func_type == self.TYPE_UNBOUND_METHOD:
                raise ValueError(b'The owner passed does not match the actual owner of the bound method.')
        if sig.is_slippery and self.func_type == self.TYPE_UNBOUND_METHOD:
            raise ValueError(b'Unable to spies on unbound slippery methods (those that return a new function on each attribute access). Please spy on an instance instead.')
        if call_fake is not None:
            if not callable(call_fake):
                raise ValueError(b'%r cannot be used for call_fake. It does not appear to be a valid function or method.' % call_fake)
            call_fake_sig = FunctionSig(call_fake)
            if not sig.is_compatible_with(call_fake_sig):
                raise IncompatibleFunctionError(func=func, func_sig=sig, incompatible_func=call_fake, incompatible_func_sig=call_fake_sig)
        self.agency = agency
        self.orig_func = func
        self._real_func = sig.real_func
        self._call_orig_func = self._clone_function(self.orig_func)
        if self._get_owner_needs_patching():
            self._owner_func_attr_value = self.owner.__dict__.get(self.func_name)
            self._patch_owner()
        else:
            self._owner_func_attr_value = self.orig_func
        if call_fake:
            self.func = call_fake
        elif call_original:
            self.func = self.orig_func
        else:
            self.func = None
        self._build_proxy_func(func)
        if self.func is self.orig_func:
            self.func = self._clone_function(self.func, code=self._old_code)
        return

    @property
    def func_type(self):
        """The type of function being spied on.

        This will be one of :py:attr:`TYPE_FUNCTION`,
        :py:attr:`TYPE_UNBOUND_METHOD`, or :py:attr:`TYPE_BOUND_METHOD`.

        Type:
            int
        """
        return self._sig.func_type

    @property
    def func_name(self):
        """The name of the function being spied on.

        Type:
            str
        """
        return self._sig.func_name

    @property
    def owner(self):
        """The owner of the method, if a bound or unbound method.

        This will be ``None`` if there is no owner.

        Type:
            type
        """
        return self._sig.owner

    @property
    def called(self):
        """Whether or not the spy was ever called."""
        try:
            return self._real_func.called
        except AttributeError:
            return False

    @property
    def calls(self):
        """The list of calls made to the function.

        Each is an instance of :py:class:`SpyCall`.
        """
        try:
            return self._real_func.calls
        except AttributeError:
            return []

    @property
    def last_call(self):
        """The last call made to this function.

        If a spy hasn't been called yet, this will be ``None``.
        """
        try:
            return self._real_func.last_call
        except AttributeError:
            return

        return

    def unspy(self, unregister=True):
        """Remove the spy from the function, restoring the original.

        The spy will, by default, be removed from the registry's
        list of spies. This can be disabled by passing ``unregister=False``,
        but don't do that. That's for internal use.

        Args:
            unregister (bool, optional):
                Whether to unregister the spy from the associated agency.
        """
        real_func = self._real_func
        owner = self.owner
        assert hasattr(real_func, b'spy')
        del FunctionSpy._spy_map[id(self)]
        del real_func.spy
        for attr_name in iterkeys(self._FUNC_ATTR_DEFAULTS):
            delattr(real_func, attr_name)

        for func_name in self._PROXY_METHODS:
            delattr(real_func, func_name)

        setattr(real_func, FunctionSig.FUNC_CODE_ATTR, self._old_code)
        if owner is not None:
            self._set_method(owner, self.func_name, self._owner_func_attr_value)
        if unregister:
            self.agency.spies.remove(self)
        return

    def call_original(self, *args, **kwargs):
        """Call the original function being spied on.

        The function will behave as normal, and will not trigger any spied
        behavior or call tracking.

        Args:
            *args (tuple):
                The positional arguments to pass to the function.

            **kwargs (dict):
                The keyword arguments to pass to the function.

        Returns:
            object:
            The return value of the function.

        Raises:
            Exception:
                Any exceptions raised by the function.
        """
        if self.func_type == self.TYPE_BOUND_METHOD:
            return self._call_orig_func(self.owner, *args, **kwargs)
        else:
            if self.func_type == self.TYPE_UNBOUND_METHOD:
                if not args or not isinstance(args[0], self.owner):
                    raise TypeError(b'The first argument to %s.call_original() must be an instance of %s.%s, since this is an unbound method.' % (
                     self._call_orig_func.__name__,
                     self.owner.__module__,
                     self.owner.__name__))
            return self._call_orig_func(*args, **kwargs)

    def called_with(self, *args, **kwargs):
        """Return whether the spy was ever called with the given arguments.

        This will check each and every recorded call to see if the arguments
        and keyword arguments match up. If at least one call does match, this
        will return ``True``.

        Not every argument and keyword argument made in the call must be
        provided to this method. These can be a subset of the positional and
        keyword arguments in the call, but cannot contain any arguments not
        made in the call.

        Args:
            *args (tuple):
                The positional arguments made in the call, or a subset of
                those arguments (starting with the first argument).

            **kwargs (dict):
                The keyword arguments made in the call, or a subset of those
                arguments.

        Returns:
            bool:
            ``True`` if there's at least one call matching these arguments.
            ``False`` if no call matches.
        """
        return any(call.called_with(*args, **kwargs) for call in self.calls)

    def last_called_with(self, *args, **kwargs):
        """Return whether the spy was last called with the given arguments.

        Not every argument and keyword argument made in the call must be
        provided to this method. These can be a subset of the positional and
        keyword arguments in the call, but cannot contain any arguments not
        made in the call.

        Args:
            *args (tuple):
                The positional arguments made in the call, or a subset of
                those arguments (starting with the first argument).

            **kwargs (dict):
                The keyword arguments made in the call, or a subset of those
                arguments.

        Returns:
            bool:
            ``True`` if the last call's arguments match the provided arguments.
            ``False`` if they do not.
        """
        call = self.last_call
        return call is not None and call.called_with(*args, **kwargs)

    def returned(self, value):
        """Return whether the spy was ever called and returned the given value.

        This will check each and every recorded call to see if any of them
        returned the given value.  If at least one call did, this will return
        ``True``.

        Args:
            value (object):
                The expected returned value from the call.

        Returns:
            bool:
            ``True`` if there's at least one call that returned this value.
            ``False`` if no call returned the value.
        """
        return any(call.returned(value) for call in self.calls)

    def last_returned(self, value):
        """Return whether the spy's last call returned the given value.

        Args:
            value (object):
                The expected returned value from the call.

        Returns:
            bool:
            ``True`` if the last call returned this value. ``False`` if it
            did not.
        """
        call = self.last_call
        return call is not None and call.returned(value)

    def raised(self, exception_cls):
        """Return whether the spy was ever called and raised this exception.

        This will check each and every recorded call to see if any of them
        raised an exception of a given type. If at least one call does match,
        this will return ``True``.

        Args:
            exception_cls (type):
                The expected type of exception raised by a call.

        Returns:
            bool:
            ``True`` if there's at least one call raising the given exception
            type. ``False`` if no call matches.
        """
        return any(call.raised(exception_cls) for call in self.calls)

    def last_raised(self, exception_cls):
        """Return whether the spy's last call raised this exception.

        Args:
            exception_cls (type):
                The expected type of exception raised by a call.

        Returns:
            bool:
            ``True`` if the last call raised the given exception type.
            ``False`` if it did not.
        """
        call = self.last_call
        return call is not None and call.raised(exception_cls)

    def raised_with_message(self, exception_cls, message):
        """Return whether the spy's calls ever raised this exception/message.

        This will check each and every recorded call to see if any of them
        raised an exception of a given type with the given message. If at least
        one call does match, this will return ``True``.

        Args:
            exception_cls (type):
                The expected type of exception raised by a call.

            message (unicode):
                The expected message from the exception.

        Returns:
            bool:
            ``True`` if there's at least one call raising the given exception
            type and message. ``False`` if no call matches.
        """
        return any(call.raised_with_message(exception_cls, message) for call in self.calls)

    def last_raised_with_message(self, exception_cls, message):
        """Return whether the spy's last call raised this exception/message.

        Args:
            exception_cls (type):
                The expected type of exception raised by a call.

            message (unicode):
                The expected message from the exception.

        Returns:
            bool:
            ``True`` if the last call raised the given exception type and
            message. ``False`` if it did not.
        """
        call = self.last_call
        return call is not None and call.raised_with_message(exception_cls, message)

    def reset_calls(self):
        """Reset the list of calls recorded by this spy."""
        self._real_func.calls = []
        self._real_func.called = False
        self._real_func.last_call = None
        return

    def __call__(self, *args, **kwargs):
        """Call the original function or fake function for the spy.

        This will be called automatically when calling the spied function,
        recording the call and the results from the call.

        Args:
            *args (tuple):
                Positional arguments passed to the function.

            **kwargs (dict):
                All dictionary arguments either passed to the function or
                default values for unspecified keyword arguments in the
                function signature.

        Returns:
            object:
            The result of the function call.
        """
        record_args = args
        if self.func_type in (self.TYPE_BOUND_METHOD,
         self.TYPE_UNBOUND_METHOD):
            record_args = record_args[1:]
        sig = self._sig
        real_func = self._real_func
        func = self.func
        call = SpyCall(self, record_args, kwargs)
        real_func.calls.append(call)
        real_func.called = True
        real_func.last_call = call
        if func is None:
            result = None
        else:
            try:
                if sig.has_getter:
                    result = sig.defined_func.__get__(self.owner)
                    if sig.is_slippery:
                        result = result(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
            except Exception as e:
                call.exception = e
                raise

            call.return_value = result
        return result

    def __repr__(self):
        """Return a string representation of the spy.

        This is mainly used for debugging information. It will show some
        details on the spied function and call log.

        Returns:
            unicode:
            The resulting string representation.
        """
        func_type = self.func_type
        if func_type == self.TYPE_FUNCTION:
            func_type_str = b'function'
            qualname = self.func_name
        else:
            owner = self.owner
            if func_type == self.TYPE_BOUND_METHOD:
                owner_cls = self.owner.__class__
                if owner_cls is type:
                    class_name = owner.__name__
                    func_type_str = b'classmethod'
                else:
                    class_name = owner_cls.__name__
                    func_type_str = b'bound method'
            elif func_type == self.TYPE_UNBOUND_METHOD:
                class_name = owner.__name__
                func_type_str = b'unbound method'
            qualname = b'%s.%s of %r' % (class_name, self.func_name, owner)
        call_count = len(self.calls)
        if call_count == 1:
            calls_str = b'call'
        else:
            calls_str = b'calls'
        return b'<Spy for %s %s (%d %s)>' % (func_type_str, qualname,
         len(self.calls), calls_str)

    def _get_owner_needs_patching(self):
        """Return whether the owner (if any) needs to be patched.

        Owners need patching if they're an instance, if the function is
        slippery, or if the function is defined on an ancestor of the class
        and not the class itself.

        See :py:meth:`_patch_owner` for what patching entails.

        Returns:
            bool:
            ``True`` if the owner needs patching. ``False`` if it does not.
        """
        owner = self.owner
        return owner is not None and (not inspect.isclass(owner) or self._sig.is_slippery or is_attr_defined_on_ancestor(owner, self.func_name))

    def _patch_owner(self):
        """Patch the owner.

        This will create a new method in place of an existing one on the
        owner, in order to ensure that the owner has its own unique copy
        for spying purposes.

        Patching the owner will avoid collisions between spies in the event
        that the method being spied on is defined by a parent of the owner,
        rather than the owner itself.

        See :py:meth:`_get_owner_needs_patching` the conditions under which
        patching will occur.
        """
        real_func = self._clone_function(self._real_func)
        owner = self.owner
        if self.func_type == self.TYPE_BOUND_METHOD:
            method_type_args = [
             real_func, owner]
            if pyver[0] >= 3:
                method_type_args.append(owner)
            self._set_method(owner, self.func_name, types.MethodType(real_func, self.owner))
        else:
            self._set_method(owner, self.func_name, real_func)
        self._real_func = real_func

    def _build_proxy_func(self, func):
        """Build the proxy function used to forward calls to this spy.

        This will construct a new function compatible with the signature of
        the provided function, which will call this spy whenever it's called.
        The bytecode of the provided function will be set to that of the
        generated proxy function. See the comment within this function for
        details on how this works.

        Args:
            func (callable):
                The function to proxy.
        """
        sig = self._sig
        exec_locals = {}
        func_code_str = b'def forwarding_call(%(params)s):\n    from kgb.spies import FunctionSpy as _kgb_cls\n    _kgb_l = locals()\n    return _kgb_cls._spy_map[%(spy_id)s](%(call_args)s)\n' % {b'params': sig.format_arg_spec(), 
           b'call_args': sig.format_forward_call_args(), 
           b'spy_id': id(self)}
        try:
            eval(compile(func_code_str, b'<string>', b'exec'), globals(), exec_locals)
        except Exception as e:
            raise InternalKGBError(b'Unable to compile a spy function for %(func)r: %(error)s\n\n%(code)s' % {b'code': func_code_str, 
               b'error': e, 
               b'func': func})

        forwarding_call = exec_locals[b'forwarding_call']
        assert forwarding_call is not None
        old_code = getattr(func, FunctionSig.FUNC_CODE_ATTR)
        temp_code = getattr(forwarding_call, FunctionSig.FUNC_CODE_ATTR)
        self._old_code = old_code
        code_args = [
         temp_code.co_argcount]
        if pyver[0] >= 3:
            if pyver[1] >= 8:
                code_args.append(temp_code.co_posonlyargcount)
            code_args.append(temp_code.co_kwonlyargcount)
        code_args += [
         temp_code.co_nlocals,
         temp_code.co_stacksize,
         temp_code.co_flags,
         temp_code.co_code,
         temp_code.co_consts,
         temp_code.co_names,
         temp_code.co_varnames,
         temp_code.co_filename,
         old_code.co_name,
         temp_code.co_firstlineno,
         temp_code.co_lnotab,
         old_code.co_freevars,
         old_code.co_cellvars]
        real_func = self._real_func
        new_code = types.CodeType(*code_args)
        setattr(real_func, FunctionSig.FUNC_CODE_ATTR, new_code)
        assert old_code != new_code
        FunctionSpy._spy_map[id(self)] = self
        real_func.spy = self
        real_func.__dict__.update(copy.deepcopy(self._FUNC_ATTR_DEFAULTS))
        for proxy_func_name in self._PROXY_METHODS:
            assert not hasattr(real_func, proxy_func_name)
            setattr(real_func, proxy_func_name, getattr(self, proxy_func_name))

        return

    def _clone_function(self, func, code=None):
        """Clone a function, optionally providing new bytecode.

        This will create a new function that contains all the state of the
        original (including annotations and any default argument values).

        Args:
            func (types.FunctionType):
                The function to clone.

            code (types.CodeType, optional):
                The new bytecode for the function. If not specified, the
                original function's bytecode will be used.

        Returns:
            types.FunctionType:
            The new function.
        """
        cloned_func = types.FunctionType(code or getattr(func, FunctionSig.FUNC_CODE_ATTR), getattr(func, FunctionSig.FUNC_GLOBALS_ATTR), getattr(func, FunctionSig.FUNC_NAME_ATTR), getattr(func, FunctionSig.FUNC_DEFAULTS_ATTR), getattr(func, FunctionSig.FUNC_CLOSURE_ATTR))
        if pyver[0] >= 3:
            for attr in ('__annotations__', '__kwdefaults__'):
                setattr(cloned_func, attr, copy.deepcopy(getattr(func, attr)))

        return cloned_func

    def _set_method(self, owner, name, method):
        """Set a new method on an object.

        This will set the method (or delete the attribute for one if setting
        ``None``).

        If setting on a class, this will use a standard
        :py:func:`setattr`/:py:func:`delattr`.

        If setting on an instance, this will use a standard
        :py:meth:`object.__setattr__`/:py:meth:`object.__delattr__` (in order
        to avoid triggering a subclass-defined version of
        :py:meth:`~object.__setattr__`/:py:meth:`~object.__delattr__`, which
        might lose or override our spy).

        Args:
            owner (type or object):
                The class or instance to set the method on.

            name (unicode):
                The name of the attribute to set for the method.

            method (types.MethodType):
                The method to set (or ``None`` to delete).
        """
        if inspect.isclass(owner):
            if method is None:
                delattr(owner, name)
            else:
                setattr(owner, name, method)
        elif method is None:
            try:
                object.__delattr__(owner, name)
            except TypeError as e:
                if str(e) == b"can't apply this __delattr__ to instance object":
                    del owner.__dict__[name]

        else:
            try:
                object.__setattr__(owner, name, method)
            except TypeError as e:
                if str(e) == b"can't apply this __setattr__ to instance object":
                    owner.__dict__[name] = method

        return