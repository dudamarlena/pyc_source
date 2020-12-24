# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/template/formatter.py
# Compiled at: 2010-03-18 14:57:33
from __future__ import with_statement
from string import Formatter
from alacarte.template.engine import Engine
__all__ = [
 'FormatterEngine']
renderer = Formatter()

class FormatterEngine(Engine):
    """A basic string.Formatter string templating language.
    
    This templating engine is associated with the '.formatter' filename extension
    and defaults to the 'text/plain' mimetype.
    
    See:
    
        http://www.python.org/doc/2.6/library/string.html#string-formatting
    
    Simple (string-based) usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('formatter:', dict(name="world"), string="Hello {name}!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('formatter:./tests/templates/hello3.txt', dict(name="world"))
        ('text/plain', 'Hello world!')
    
    """
    mapping = {'formatter': 'text/plain', 
       None: 'text/plain'}

    def render(self, template, data, **options):
        """Implemented by a sub-class, this returns the 2-tuple of mimetype and unicode content."""
        return (
         self.mapping[None],
         renderer.vformat(template, data if not isinstance(data, dict) else tuple(), data if isinstance(data, dict) else dict()))