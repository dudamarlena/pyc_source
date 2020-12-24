# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/main/grids.py
# Compiled at: 2020-05-12 15:34:00
# Size of source mod 2**32: 7519 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from gridtest.main.generate import import_module
from gridtest.main.expand import expand_args
from gridtest.logger import bot
from copy import deepcopy
import itertools, inspect, re, sys, os

class Grid:

    def __init__(self, name, params, filename='', refs=None):
        """A Grid is a defined parameterization over a set of arguments, for
           any use case (testing, measuring metrics from models, etc.)

           Arguments:
             - name (str) : the name of the grid, an identifier
             - params (dict) : the args and functions
             - filename (str) : if relevant, a filename to import modules from

           If argument sets are reasonably sized, you should be able to 
           set yield_args to False and interact with self.paramsets. Otherwise,
           you can instantiate the Grid and iterate through it at the same time.
        """
        self.name = name
        self.params = params
        self.args = expand_args(params.get('args', {}))
        self.functions = params.get('functions', {})
        self.refs = refs or {}
        self.cache = params.get('cache', False)
        self.filename = filename
        self.count = self.params.get('count', 1)
        self.unwrap_functions()
        self.argsets = []
        if self.cache:
            self.argsets = list(self)

    def __iter__(self):
        """Given input variables, parse into parameter sets. If a variable
           is not provided as a list, we put into list. If a list is desired
           as the variable, it would be provided as a list of lists.
        """
        self.generate_references()
        try:
            keys, values = zip(*self.args.items())
        except:
            keys = []
            values = []

        values = [[v] if not isinstance(v, list) else v for v in values]
        for count in range(self.count):
            for v in (itertools.product)(*values):
                args = dict(zip(keys, v))
                for varname, funcname in self.functions.items():
                    args[varname] = self.apply_function(funcname, args)

                yield args

    def unwrap_functions(self):
        """Given that a function is to be unwrapped, this means that we 
           evaluate it first to generate a list that is used to updated args.
        """
        try:
            keys, values = zip(*self.args.items())
        except:
            keys = []
            values = []

        values = [[v] if not isinstance(v, list) else v for v in values]
        to_remove = set()
        for varname, funcname in self.functions.items():
            if isinstance(funcname, dict) and 'unwrap' in funcname:
                unwrapped = []
                for v in (itertools.product)(*values):
                    args = dict(zip(keys, v))
                    result = self.apply_function(funcname, args)
                    result = [[v] if not isinstance(v, (list, tuple)) else v for v in result]
                    unwrapped += result
                    to_remove.add(varname)

                self.args[varname] = unwrapped

        for varname in to_remove:
            del self.functions[varname]

    def generate_references(self):
        """Given a loaded set of references from other grids (self.refs)
           load them into the current args space.
        """
        for name, ref in self.params.get('ref', {}).items():
            grid, ref = ref.split('.', 1)
            if grid in self.refs and ref in self.refs[grid].args:
                self.args[name] = self.refs[grid].args[ref]

    def apply_function(self, funcname, args):
        """Given a function (a name, or a dictionary to derive name and other
           options from) run some set of input variables (that are taken by
           the function) through it to derive a result. The result returned
           is used to set another variable. If a count is defined, we
           run the function (count) times and return a list. Otherwise, we
           run it once.

           Arguments:
            - funcname (str or dict) : the function name or definition
            - args (dict) : lookup of arguments for the function
        """
        count = 1
        args = deepcopy(args or {})
        if isinstance(funcname, dict):
            if 'count' in funcname:
                count = funcname['count']
            if 'args' in funcname:
                for oldkey, newkey in funcname['args'].items():
                    if oldkey in args:
                        args[newkey] = args[oldkey]

            if 'func' not in funcname:
                bot.exit(f"{funcname} is missing func key with function name.")
            funcname = funcname['func']
        func = funcname if not isinstance(funcname, str) else self.get_function(funcname)
        funcargs = intersect_args(func, args)
        if count == 1:
            return func(**funcargs)
        return [func(**funcargs) for c in range(count)]

    def get_function(self, funcname):
        """Given a function name, return it. Exit on error if not found.
        """
        sys.path.insert(0, os.path.dirname(self.filename))
        module = '.'.join(funcname.split('.')[:-1])
        funcname = funcname.split('.')[(-1)]
        try:
            module = import_module(module)
            func = getattr(module, funcname)
            if func is None:
                bot.exit(f"Cannot find {funcname}.")
        except:
            bot.exit(f"Cannot import grid function {funcname}")

        return func

    def __repr__(self):
        return '[grid|%s]' % self.name

    def __str__(self):
        return '[grid|%s]' % self.name


def intersect_args(func, args):
    """Given a loaded function and a dictionary of args, return the
       overlapping set (those that are allowed to be given to the 
       function
    """
    argspec = inspect.getfullargspec(func)
    allowed_args = set(argspec.args).intersection(set(args))
    kwargs = {}
    for allowed_arg in allowed_args:
        if allowed_arg in args:
            kwargs[allowed_arg] = args[allowed_arg]

    return kwargs