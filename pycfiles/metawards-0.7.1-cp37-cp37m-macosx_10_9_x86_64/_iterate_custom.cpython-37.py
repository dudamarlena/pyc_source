# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/iterators/_iterate_custom.py
# Compiled at: 2020-04-17 13:53:44
# Size of source mod 2**32: 8153 bytes
__all__ = ['iterate_custom',
 'build_custom_iterator']
from ._iterate_core import iterate_core
from ._iterate_default import iterator_needs_setup

def build_custom_iterator(custom_function, parent_name='__main__'):
    """Build and return a custom iterator from the passed
       function. This will wrap 'iterate_custom' around
       the function to double-check that the custom
       function is doing everything correctly

       Parameters
       ----------
       custom_function
         This can either be a function, which will be wrapped and
         returned, or it can be a string. If it is a string then
         we will attempt to locate or import the function associated
         with that string. The search order is;

         1. Is this 'metawards.iterators.custom_function'?
         2. Is this 'custom_function' that is already imported'?
         3. Is this a file name in the current path, if yes then
            find the function in that file (either the first function
            called 'iterateXXX' or the specified function if
            custom_function is in the form module::function)

        parent_name: str
          This should be the __name__ of the calling function, e.g.
          call this function as build_custom_iterator(func, __name__)

        Returns
        -------
        iterator
          The wrapped iterator that is suitable for using in the iterate
          function.
    """
    if isinstance(custom_function, str):
        print(f"Importing a custom iterator from {custom_function}")
        import metawards.iterators
        try:
            func = getattr(metawards.iterators, custom_function)
            return build_custom_iterator(func)
        except Exception:
            pass

        import sys
        try:
            func = getattr(sys.modules[__name__], custom_function)
            return build_custom_iterator(func)
        except Exception:
            pass

        try:
            func = getattr(sys.modules[parent_name], custom_function)
            return build_custom_iterator(func)
        except Exception:
            pass

        try:
            func = getattr(sys.modules['__main__'], custom_function)
            return build_custom_iterator(func)
        except Exception:
            pass

        if custom_function.find('::') != -1:
            parts = custom_function.split('::')
            func_name = parts[(-1)]
            func_module = '::'.join(parts[0:-1])
        else:
            func_name = None
            func_module = custom_function
        try:
            import importlib
            module = importlib.import_module(func_module)
        except Exception:
            module = None

        if module is None:
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(func_module, f"{func_module}.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"Loaded iterator from {func_module}.py")
            except Exception:
                module = None

        if module is None:
            print(f"Cannot find the iterator '{custom_function}'.Please make sure this is spelled correctly and any python modules/files needed are in the PYTHONPATH or current directory")
            raise ImportError(f"Could not import the iterator '{custom_function}'")
        if func_name is None:
            import inspect
            for name, value in inspect.getmembers(module):
                if name.startswith('iterate') and hasattr(value, '__call__'):
                    return build_custom_iterator(getattr(module, name))

            print(f"Could not find any function in the module {custom_function} that has a name that starts with 'iterate'. Please manually specify the name using the '{custom_function}::your_function syntax")
            raise ImportError(f"Could not import the iterator {custom_function}")
        else:
            if hasattr(module, func_name):
                return build_custom_iterator(getattr(module, func_name))
            print(f"Could not find the function {func_name} in the module {func_module}. Check that the spelling is correct and that the right version of the module is being loaded.")
            raise ImportError(f"Could not import the iterator {custom_function}")
    if not hasattr(custom_function, '__call__'):
        print(f"Cannot build an iterator for {custom_function} as it is missing a __call__ function, i.e. it is not a function.")
        raise ValueError(f"You can only build custom iterators for actual functions... {custom_function}")
    print(f"Building a custom iterator for {custom_function}")
    return lambda **kwargs: iterate_custom(custom_function=custom_function, **kwargs)


def iterate_custom(custom_function, setup=False, **kwargs):
    """This returns the default list of 'advance_XXX' functions that
       are called in sequence for each iteration of the model run.
       This iterator provides a custom iterator that uses
       'custom_function' passed from the user. This iterator makes
       sure that 'setup' is called correctly and that the functions
       needed by 'iterate_core' are called first.

       Parameters
       ----------
       custom_function
         A custom user-supplied function that returns the
         functions that the user would like to be called for
         each step.
       setup: bool
         Whether or not to return the functions used to setup the
         space and input for the advance_XXX functions returned by
         this iterator. This is called once at the start of a run
         to return the functions that must be called to setup the
         model

       Returns
       -------
       funcs: List[function]
         The list of functions that ```iterate``` will call in sequence
    """
    kwargs['setup'] = setup
    if setup:
        core_funcs = iterate_core(**kwargs)
        if iterator_needs_setup(custom_function):
            custom_funcs = custom_function(**kwargs)
        else:
            custom_funcs = None
    else:
        core_funcs = iterate_core(**kwargs)
        custom_funcs = custom_function(**kwargs)
    if core_funcs is None or len(core_funcs) == 0:
        if custom_funcs is None:
            return []
        return custom_funcs
    else:
        if custom_funcs is None or len(custom_funcs) == 0:
            return core_funcs
        for i in range(len(core_funcs) - 1, -1, -1):
            if core_funcs[i] not in custom_funcs:
                custom_funcs.insert(0, core_funcs[i])

        return custom_funcs