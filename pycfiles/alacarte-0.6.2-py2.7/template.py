# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/template/template.py
# Compiled at: 2010-03-18 05:47:02
from __future__ import with_statement
from string import Template
__all__ = [
 'render']

def render(data, template=None, string=None, safe=True, content_type='text/plain'):
    """A basic string.Template string templating language.
    
    See:
    
        http://www.python.org/doc/2.5/lib/node40.html
    
    Simple (string-based) usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('template:', dict(name="world"), string="Hello $name!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from alacarte.core import Engines
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