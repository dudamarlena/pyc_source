# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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