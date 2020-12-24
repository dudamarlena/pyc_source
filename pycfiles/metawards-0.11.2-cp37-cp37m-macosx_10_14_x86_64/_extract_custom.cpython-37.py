# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/extractors/_extract_custom.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 7155 bytes
from typing import Union as _Union
from typing import List as _List
from utils._get_functions import MetaFunction, accepts_stage
__all__ = [
 'extract_custom',
 'build_custom_extractor']

def build_custom_extractor(custom_function: _Union[(str, MetaFunction)], parent_name='__main__') -> MetaFunction:
    """Build and return a custom extractor from the passed
       function. This will wrap 'extract_custom' around
       the function to double-check that the custom
       function is doing everything correctly

       Parameters
       ----------
       custom_function: MetaFunction or str
         This can either be a function, which will be wrapped and
         returned, or it can be a string. If it is a string then
         we will attempt to locate or import the function associated
         with that string. The search order is;

         1. Is this 'metawards.extractors.custom_function'?
         2. Is this 'custom_function' that is already imported'?
         3. Is this a file name in the current path, if yes then
            find the function in that file (either the first function
            called 'extractXXX' or the specified function if
            custom_function is in the form module::function)

        parent_name: str
          This should be the __name__ of the calling function, e.g.
          call this function as build_custom_extractor(func, __name__)

        Returns
        -------
        extractor: MetaFunction
          The wrapped extractor that is suitable for using in the extract
          function.
    """
    print(custom_function)
    if isinstance(custom_function, str):
        print(f"Importing a custom extractor from {custom_function}")
        import metawards.extractors
        try:
            func = getattr(metawards.extractors, custom_function)
            return build_custom_extractor(func)
        except Exception:
            pass

        import sys
        try:
            func = getattr(sys.modules[__name__], custom_function)
            return build_custom_extractor(func)
        except Exception:
            pass

        try:
            func = getattr(sys.modules[parent_name], custom_function)
            return build_custom_extractor(func)
        except Exception:
            pass

        try:
            func = getattr(sys.modules['__main__'], custom_function)
            return build_custom_extractor(func)
        except Exception:
            pass

        if custom_function.find('::') != -1:
            parts = custom_function.split('::')
            func_name = parts[(-1)]
            func_module = '::'.join(parts[0:-1])
        else:
            func_name = None
            func_module = custom_function
        from utils._import_module import import_module
        module = import_module(func_module)
        if module is None:
            print(f"Cannot find the extractor '{custom_function}'.Please make sure this is spelled correctly and any python modules/files needed are in the PYTHONPATH or current directory")
            raise ImportError(f"Could not import the extractor '{custom_function}'")
        elif func_name is None:
            import inspect
            func = None
            for name, value in inspect.getmembers(module):
                if name.startswith('extract') and hasattr(value, '__call__'):
                    func = value

            if func is not None:
                return build_custom_extractor(func)
            print(f"Could not find any function in the module {custom_function} that has a name that starts with 'extract'. Please manually specify the name using the '{custom_function}::your_function syntax")
            raise ImportError(f"Could not import the extractor {custom_function}")
        else:
            if hasattr(module, func_name):
                return build_custom_extractor(getattr(module, func_name))
            print(f"Could not find the function {func_name} in the module {func_module}. Check that the spelling is correct and that the right version of the module is being loaded.")
            raise ImportError(f"Could not import the extractor {custom_function}")
    if not hasattr(custom_function, '__call__'):
        print(f"Cannot build an extractor for {custom_function} as it is missing a __call__ function, i.e. it is not a function.")
        raise ValueError(f"You can only build custom extractors for actual functions... {custom_function}")
    print(f"Building a custom extractor for {custom_function}")
    return lambda **kwargs: extract_custom(custom_function=custom_function, **kwargs)


def extract_custom(custom_function: MetaFunction, stage: str, **kwargs) -> _List[MetaFunction]:
    """This returns the default list of 'output_XXX' functions that
       are called in sequence for each iteration of the model run.
       This provides a custom extractor that uses
       'custom_function' passed from the user. This makes
       sure that if 'stage' is not handled by the custom function,
       then the "extract_default" functions for that stage
       are correctly called for all stages except "analyse"

       Parameters
       ----------
       custom_function: MetaFunction
         A custom user-supplied function that returns the
         functions that the user would like to be called for
         each step.
       stage: str
         The stage of the day/model

       Returns
       -------
       funcs: List[MetaFunction]
         The list of functions that will be called in sequence
    """
    kwargs['stage'] = stage
    if custom_function is None:
        from ._extract_default import extract_default
        return extract_default(**kwargs)
    if stage == 'analyse' or accepts_stage(custom_function):
        return custom_function(**kwargs)
    from ._extract_default import extract_default
    return extract_default(**kwargs)