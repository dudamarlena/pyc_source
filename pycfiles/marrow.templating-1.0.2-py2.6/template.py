# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/template/template.py
# Compiled at: 2012-05-23 13:18:32
from __future__ import unicode_literals, absolute_import
from string import Template
__all__ = [
 b'render']

def render(data, template=None, string=None, safe=True, content_type=b'text/plain'):
    """A basic string.Template string templating language.
    
    See:
    
        http://www.python.org/doc/2.5/lib/node40.html
    
    Simple (string-based) usage:
    
        >>> from marrow.templating.core import Engines
        >>> render = Engines()
        >>> render('template:', dict(name="world"), string="Hello $name!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from marrow.templating.core import Engines
        >>> render = Engines()
        >>> render('template:./tests/templates/hello2.txt', dict(name="world"))
        ('text/plain', 'Hello world!')
    
    """
    content = string
    if template:
        with open(template) as (f):
            content = f.read()
    renderer = Template(content)
    if safe:
        return (content_type, renderer.safe_substitute(data))
    return (content_type, renderer.substitute(data))