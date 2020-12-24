# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/main/helpers.py
# Compiled at: 2020-05-10 13:25:41
# Size of source mod 2**32: 7223 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from gridtest.main.generate import import_module, get_function_typing
from gridtest.main.grids import intersect_args
from io import StringIO
import re, sys, time, os

class Capturing(list):
    __doc__ = 'capture output from stdout and stderr into capture object'

    def __enter__(self):
        self.set_stdout()
        self.set_stderr()
        return self

    def set_stdout(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio_out = StringIO()

    def set_stderr(self):
        from io import StringIO
        self._stderr = sys.stderr
        sys.stderr = self._stringio_err = StringIO()

    def __exit__(self, *args):
        self.append({'out':self._stringio_out.getvalue().splitlines(), 
         'err':self._stringio_err.getvalue().splitlines()})
        del self._stringio_out
        sys.stdout = self._stdout
        sys.stderr = self._stderr


def print_interactive(**kwargs):
    """A helper function to print locals that are relevant to test_basic for 
       the user.
    """
    print('\n\nGridtest interactive mode! Press Control+D to cycle to next test.')
    print('\n\x1b[1mVariables\x1b[0m')
    print(f"   func: {kwargs['func']}")
    print(f" module: {kwargs['module']}")
    print(f"   args: {kwargs['args']}")
    print(f"returns: {kwargs['returns']}")
    print('\n\x1b[1mHow to test\x1b[0m')
    print('passed, error = test_types(func, args, returns)')
    print('result = func(**args)\n')


def test_basic(funcname, module, filename, func=None, args=None, returns=None, interactive=False, metrics=None):
    """test basic is a worker version of the task.test_basic function.
       If a function is not provided, funcname, module, and filename are
       required to retrieve it. A function can only be provided directly
       if it is pickle serializable (multiprocessing would require this).
       It works equivalently but is not attached to a class, and returns
       a list of values for [passed, result, out, err, raises]

       Arguments:
         - funcname (str) : the name of the function to import
         - module (str) : the base module to get the function from
         - func (Function) : if running serial, function can be directly provided
         - args (dict) : dictionary of arguments
         - returns (type) : a returns type to test for
         - interactive (bool) : run in interactive mode (giving user shell)
         - metrics (list) : one or more metrics (decorators) to run.
    """
    metrics = metrics or []
    if not func:
        sys.path.insert(0, os.path.dirname(filename))
        func = get_function(module=module,
          funcname=funcname,
          args=args,
          filename=filename)
    originalfunc = func
    passed = False
    result = None
    raises = None
    out = []
    err = []
    for metric in metrics:
        if not metric.startswith('@'):
            continue
        metric = re.sub('^[@]', '', metric)
        try:
            gt = import_module('gridtest.decorators')
            decorator = getattr(gt, metric)
            func = decorator(func)
        except:
            try:
                metric_module = metric.split('.')[0]
                mm = import_module(metric_module)
                for piece in metric.split('.')[1:]:
                    decorator = getattr(mm, piece)

                func = decorator(func)
            except:
                out.append(f"Warning, unable to import decorator @{metric}")

    if interactive:
        print_interactive(**locals())
        try:
            import IPython
            IPython.embed()
        except:
            import code
            code.interact(local=(locals()))

    if not func:
        err = [
         f"Cannot find function {funcname}"]
    else:
        args = intersect_args(originalfunc, args)
        passed, error = test_types(originalfunc, args, returns)
        err += error
        if not passed:
            raises = 'TypeError'
        else:
            try:
                with Capturing() as (output):
                    result = func(**args)
                if output:
                    std = output.pop(0)
                    out += std.get('out')
                    err += std.get('err')
                passed = True
            except Exception as e:
                try:
                    raises = type(e).__name__
                    message = str(e)
                    if message:
                        err.append(message)
                finally:
                    e = None
                    del e

            return [
             passed, result, out, err, raises]


def get_function(module, funcname, args, filename):
    """given a module name, function name, argument, and filename, derive
       a function, optionally deriving an instance first that it might
       belong to
    """
    sys.path.insert(0, os.path.dirname(filename))
    module = import_module(module)
    if 'self' in args:
        instance = getattr(module, funcname.split('.')[0])
        instanceargs = {}
        if 'self' in args:
            instanceargs = intersect_args(instance, args['self'])
        instance = instance(**instanceargs)
        for piece in funcname.split('.')[1:]:
            func = getattr(instance, piece)
            instance = func

        del args['self']
    else:
        for piece in funcname.split('.'):
            func = getattr(module, piece)
            module = func

    return func


def test_types(func, args=None, returns=None):
    """Given a loaded function, get it's types and ensure that they are
       correct. Returns a boolean to indicate correct/ passing (True)
    """
    args = args or {}
    err = []
    types = get_function_typing(func)
    for argname, argtype in types.items():
        if argname in args:
            value = args[argname]
            isinstance(value, argtype) or err.append('TypeError %s (%s) is %s, should be %s' % (
             argname, value, type(value), argtype))
            return (
             False, err)

    if 'return' in types:
        if returns:
            if not isinstance(returns, types['return']):
                err.append('TypeError return value %s should be %s' % (returns, types['return']))
                return (
                 False, err)
    return (
     True, err)