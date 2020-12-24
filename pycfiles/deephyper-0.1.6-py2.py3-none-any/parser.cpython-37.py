# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/parser.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 734 bytes
import inspect
from inspect import signature

def add_arguments_from_signature(parser, obj):
    """Add arguments to parser base on obj default keyword parameters.

    Args:
        parser (ArgumentParser)): the argument parser to which we want to add arguments.
        obj (type): the class from which we want to extract default parameters for the constructor.
    """
    sig = signature(obj)
    for p_name, p in sig.parameters.items():
        if p.kind == inspect._POSITIONAL_OR_KEYWORD and p.default is not inspect._empty:
            parser.add_argument(f"--{p_name.replace('_', '-')}",
              default=(p.default),
              help=f"Defaults to '{str(p.default)}'.")