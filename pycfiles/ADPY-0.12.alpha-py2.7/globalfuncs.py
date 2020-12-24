# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ADPY/ADFUN/globalfuncs.py
# Compiled at: 2013-11-25 05:46:29
""" 
    Copyright 2013 Oliver Schnabel
    
    This file is part of ADPY.
    ADPY is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    ADPY is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ADPY.  If not, see <http://www.gnu.org/licenses/>.
"""
import math, numpy, string
numpy_function_names = [
 'exp', 'log', 'log10', 'sqrt', 'pow',
 'sin', 'cos', 'tan',
 'arcsin', 'arccos', 'arctan',
 'sinh', 'cosh', 'tanh',
 'sign']
function_template = string.Template('\ndef $function_name(*args, **kwargs):\n    """\n    generic implementation of $function_name\n\n    this function calls, depending on the input arguments,\n    either\n\n    * numpy.$function_name\n    * numpy.linalg.$function_name\n    * args[i].__class__\n\n    """\n    case,arg = 0,0\n    for na,a in enumerate(args):\n        if hasattr(a.__class__, \'$function_name\'):\n            case = 1\n            arg  = na\n            break\n\n    if case==1:\n        return getattr(args[arg].__class__, \'$function_name\')(*args, **kwargs)\n\n    elif case==0:\n        return $namespace.__getattribute__(\'$function_name\')(*args, **kwargs)\n\n    else:\n        return $namespace.__getattribute__(\'$function_name\')(*args, **kwargs)\n')
for function_name in numpy_function_names:
    exec function_template.substitute(function_name=function_name, namespace='numpy')