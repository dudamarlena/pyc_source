# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/template/sprintf.py
# Compiled at: 2010-03-18 14:57:33
from __future__ import with_statement
from alacarte.template.engine import Engine
__all__ = [
 'SprintfEngine']

class SprintfEngine(Engine):
    """A basic sprintf-based string templating language.
    
    Simple (string-based) usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('sprintf:', dict(hello="world"), string="Hello %(hello)s!")
        ('text/plain', 'Hello world!')
    
    File-based usage:
    
        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('sprintf:./tests/templates/hello.txt', dict(hello="world"))
        ('text/plain', 'Hello world!')
    
    """
    mapping = {'sprintf': 'text/plain', 
       None: 'text/plain'}

    def render(self, template, data, **options):
        return (
         self.mapping[None], template % data)