# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/extlib/resolver.py
# Compiled at: 2007-01-10 11:06:43
"""resolver - resolve specially formated statements to Python objects 

Copyright (C) 2006 Luke Arno - http://lukearno.com/

This program is free software; you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 2 of the License, or (at your 
option) any later version.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to:

The Free Software Foundation, Inc., 
51 Franklin Street, Fifth Floor, 
Boston, MA  02110-1301, USA.

Luke Arno can be found at http://lukearno.com/

"""

def resolve(statement):
    """Resolve a specially formated statement to a Python object.
    
    dot.path.to.import:TheRest().is_evaled.('in', 'that', 'context')
    
    == The following two lines would be equivalent: ==
    
    {{{
    
    x = resolve('foo.bar:baz')
    from foo.bar import baz as x

    }}}

    == Everything to the right of the colon is evaled so: ==

    {{{
    
    x = resolve("module:FooApp('blarg').prop")

    # ...is like...

    from module import FooApp
    x = FooApp('blarg').prop
    
    }}}
    
    You can even do this:
    
    {{{
    
    resolve("pak.mod:foo('resolve('pak.mod:bar')')")
    
    }}}
    
    == If you just want to eval an expression: ==

    {{{

    plus_two = resolve(":lambda x: x + 2")

    }}
    """
    if ':' in statement:
        (import_path, evalable) = statement.strip().split(':', 1)
    else:
        import_path = statement
        evalable = None
    if not import_path:
        return eval(evalable)
    descend = import_path.split('.')[1:]
    res = __import__(import_path)
    for d in descend:
        res = getattr(res, d)

    if evalable:
        return eval('res.%s' % evalable)
    else:
        return res
    return