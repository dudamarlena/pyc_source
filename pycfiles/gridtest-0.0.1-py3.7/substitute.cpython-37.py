# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridtest/main/substitute.py
# Compiled at: 2020-04-28 18:39:39
# Size of source mod 2**32: 4448 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from gridtest.main.generate import import_module
from gridtest.defaults import GRIDTEST_FUNCS
import os, re, sys

def substitute_args(value, params=None):
    """Given a value, determine if it has variable argument substitutions
       in the format of {{ args.<name> }} and if so, if the argument is present
       return the value with the substitution.
    """
    params = params or {}
    if not isinstance(value, str):
        return value
    for template in re.findall('{{.+}}', value):
        varname = re.sub('({|}| )', '', template)
        if varname not in params:
            value = re.sub(template, '', value)
        else:
            value = re.sub(template, str(params[varname]), str(value))

    return value


def substitute_func(value, funcs=None):
    """Given a value, determine if it contains a function substitution,
       and if it's one an important function (e.g., one from gridtest.helpers)
       return the value with the function applied. 

       Arguments:
         - value (str) : the value to do the substitution for.
         - funcs (dict) : lookup dictionary of functions to be used

       Notes: 
         A function should be in the format: {% tempfile.mkdtemp %} 
         (global import) or a function in gridtest.func in the format 
         {% tmp_path %}. If arguments are supplied, they should be in 
         the format {% tmp_path arg1=1 arg2=2 %}
    """
    if not isinstance(value, str):
        return value
    for template in re.findall('{%.+%}', value):
        varname = re.sub('({%|%})', '', template)
        params = [x.strip() for x in varname.split(' ') if x]
        modulename = params.pop(0).rsplit('.', 1)[0]
        funcpath = modulename[1:]
        func = None
        if modulename in GRIDTEST_FUNCS:
            funcpath = modulename
            modulename = 'gridtest.func'
        else:
            if funcs:
                if modulename in funcs:
                    func = funcs.get(modulename)
                else:
                    funcpath = funcpath[0]
            elif not funcpath:
                if not func:
                    sys.exit(f"A function name must be provided for {varname}")
        if not func:
            try:
                module = import_module(modulename)
                func = getattr(module, funcpath)
            except:
                sys.exit(f"Cannot import module {modulename}")

            if not func:
                sys.exit(f"Cannot import function {funcpath} from module {modulename}")
            kwargs = {}
            params = {x.split('=')[0]:x.split('=')[1] for x in params}
            for paramname, paramvalue in params.items():
                if paramvalue == 'None':
                    paramvalue = None
                else:
                    if paramvalue == 'True':
                        paramvalue = True
                    else:
                        if paramvalue == 'False':
                            paramvalue = False
                        else:
                            if re.search('^[0-9]+$', paramvalue):
                                paramvalue = int(paramvalue)
                            else:
                                if re.search('^[0-9]+[.]([0-9]+)?$', paramvalue):
                                    paramvalue = float(paramvalue)
                                else:
                                    if re.search('^(".+")$', paramvalue):
                                        paramvalue = paramvalue.strip('"')
                                    else:
                                        if re.search("^('.+')$", paramvalue):
                                            paramvalue = paramvalue.strip("'")
                                        kwargs[paramname] = paramvalue

            new_value = func(**kwargs)
            value = re.sub(template, value, new_value)

    return value