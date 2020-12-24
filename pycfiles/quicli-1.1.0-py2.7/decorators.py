# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/quicli/decorators.py
# Compiled at: 2011-09-04 00:58:03
from .guts import ParserAssembler

def run(*args, **kwargs):
    """Marks a function as the main entry point and optionally modifies the underlying ArgumentParser object"""
    run_on_import = False
    __internal_frame__ = True
    generated_wrapper = None

    def wrapper():

        def wrapper(func):
            __internal_frame__ = True
            setattr(func, '_quicli_parser', (args, kwargs))
            ParserAssembler._assemble(run_on_import, func)
            return func

        return wrapper

    if len(args) == 1 and len(kwargs) == 0 and hasattr(args[0], '__call__'):
        func = args[0]
        args = list(args)[1:]
        return wrapper()(func)
    else:
        if not len(args) and not len(kwargs):
            ParserAssembler._assemble(run_on_import)
        else:
            if len(args):
                run_on_import = args[0]
            if 'run_on_import' in kwargs:
                run_on_import = kwargs['run_on_import']
            return wrapper()
        return


def main(*args, **kwargs):
    """Marks a function as the main entry point"""
    __internal_frame__ = True

    def wrapper():

        def wrapper(func):
            __internal_frame__ = True
            setattr(func, '_quicli_parser', (args, kwargs))
            return func

        return wrapper

    if len(args) == 1 and len(kwargs) == 0 and hasattr(args[0], '__call__'):
        func = args[0]
        args = list(args)[1:]
        return wrapper()(func)
    else:
        return wrapper()


def sub(*args, **kwargs):
    """Marks a function as a sub entry point"""

    def wrapper():

        def wrapper(func):
            setattr(func, '_quicli_subparser', (args, kwargs))
            return func

        return wrapper

    if len(args) == 1 and len(kwargs) == 0 and hasattr(args[0], '__call__'):
        func = args[0]
        args = list(args)[1:]
        return wrapper()(func)
    else:
        return wrapper()


def argument(*args, **kwargs):
    """Modifies an argument's definition
    
    Accepts as parameters anything acceptable for ArgumentParser.add_argument,
    plus the validation parameters "test" and "error".
    """
    if not args or len(args) and not isinstance(args[0], str):
        raise TypeError('the @argument decorator requires its first argument to be the name of an argument of the wrapped function')

    def wrapper(func):
        if not hasattr(func, '_quicli_arguments'):
            setattr(func, '_quicli_arguments', [])
        func._quicli_arguments.append((args, kwargs))
        return func

    return wrapper