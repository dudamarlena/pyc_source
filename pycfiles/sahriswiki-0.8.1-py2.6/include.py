# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sahriswiki/macros/include.py
# Compiled at: 2010-07-22 05:56:37
"""Include macro

Macro for inclusion of other wiki pages
"""
from genshi.builder import tag
from genshi.output import HTMLSerializer
serializer = HTMLSerializer()

def include(macro, environ, data, *args, **kwargs):
    """Include the contents of another wiki page.
    
    This macro allows you to include the contents of another wiki page,
    optinoally allowing you to include it parsed (//the default//) or
    unparsed (//parse=False//). If the specified page does not exist,
    then "Page Not Found" will be displayed.

    **Arguments:**
    * name=None (//the name of the page to include//)
    * parse=True (//whether to parse the page//)
    * source=False (//whether to display the genereated HTML / source//)

    **Example(s):**
    {{{
    <<include "SandBox">>
    }}}

    <<include "SandBox">>

    {{{
    <<include "SandBox", parse=False>>
    }}}

    <<include "SandBox", parse=False>>
    """
    name = kwargs.get('name', args and args[0] or None)
    if name is None:
        return
    else:
        parse = kwargs.get('parse', True)
        source = kwargs.get('source', False)
        contents = environ.include(name, parse, data=data)
        if source:
            return tag.pre(('').join(serializer(contents)))
        return contents
        return