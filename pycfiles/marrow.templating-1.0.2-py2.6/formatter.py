# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/template/formatter.py
# Compiled at: 2012-05-23 13:18:32
from __future__ import unicode_literals, absolute_import
from string import Formatter
from marrow.templating.core import Engine
__all__ = [
 b'FormatterEngine']
renderer = Formatter()

class FormatterEngine(Engine):
    """A basic string.Formatter string templating language.
    
    This templating engine is associated with the '.formatter' filename extension
    and defaults to the 'text/plain' mimetype.
    
    See:
    
        http://www.python.org/doc/2.6/library/string.html#string-formatting
    
    Simple (string-based) usage:
    
        >>> from marrow.templating.core import Engines
        >>> render = Engines()
        >>> render('formatter:', dict(name="world"), string="Hello {name}!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from marrow.templating.core import Engines
        >>> render = Engines()
        >>> render('formatter:./tests/templates/hello3.txt', dict(name="world"))
        ('text/plain', 'Hello world!')
    
    """

    def render(self, template, data, **options):
        """Implemented by a sub-class, this returns the 2-tuple of mimetype and unicode content."""
        return (
         options.get(b'content_type', b'text/plain'),
         renderer.vformat(template, data if not isinstance(data, dict) else tuple(), data if isinstance(data, dict) else dict()))