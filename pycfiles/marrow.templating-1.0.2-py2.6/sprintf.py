# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/template/sprintf.py
# Compiled at: 2012-05-23 13:18:32
from __future__ import unicode_literals, absolute_import
from marrow.templating.core import Engine
__all__ = [
 b'SprintfEngine']

class SprintfEngine(Engine):
    """A basic sprintf-based string templating language.
    
    Simple (string-based) usage:
    
        >>> from marrow.templating.core import Engines
        >>> render = Engines()
        >>> render('sprintf:', dict(hello="world"), string="Hello %(hello)s!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from marrow.templating.core import Engines
        >>> render = Engines()
        >>> render('sprintf:./tests/templates/hello.txt', dict(hello="world"))
        ('text/plain', 'Hello world!')
    
    """

    def render(self, template, data, **options):
        return (
         options.get(b'content_type', b'text/plain'), template % data)