# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apacheconfig/__init__.py
# Compiled at: 2020-01-09 16:01:59
__version__ = '0.3.2'
from contextlib import contextmanager
from apacheconfig import flavors
from apacheconfig.error import ApacheConfigError
from apacheconfig.lexer import make_lexer
from apacheconfig.loader import ApacheConfigLoader
from apacheconfig.parser import make_parser
from apacheconfig.wloader import ApacheConfigWritableLoader

@contextmanager
def make_loader(writable=False, **options):
    ApacheConfigLexer = make_lexer(**options)
    ApacheConfigParser = make_parser(**options)
    if writable:
        options['preservewhitespace'] = True
        yield ApacheConfigWritableLoader(ApacheConfigParser(ApacheConfigLexer(), start='contents'), **options)
    else:
        yield ApacheConfigLoader(ApacheConfigParser(ApacheConfigLexer()), **options)


__all__ = [
 'make_lexer', 'make_parser', 'make_loader',
 'ApacheConfigLoader', 'ApacheConfigError']