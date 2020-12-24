# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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