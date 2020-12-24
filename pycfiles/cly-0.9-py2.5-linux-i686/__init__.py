# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cly/__init__.py
# Compiled at: 2007-05-25 01:36:35
"""CLY is a Python module for simplifying the creation of interactive shells.
Kind of like the builtin ``cmd`` module on steroids.

It has the following features:

  - Tab completion of all commands.

  - Contextual help.

  - Extensible grammar - you can define your own commands with full dynamic
    completion, contextual help, and so on.

  - Simple. Grammars are constructed from objects using a convenient
    ''function-call'' syntax.

  - Flexible command grouping and ordering.

  - Grammar parser, including completion and help enumeration, can be used
    independently of the readline-based shell. This allows CLY's parser to
    be used in other environments (think "web-based shell" ;))

  - Lots of other cool stuff.
"""
__docformat__ = 'restructuredtext en'
__author__ = 'Alec Thomas <alec@swapoff.org>'
try:
    __version__ = __import__('pkg_resources').get_distribution('cly').version
except ImportError:
    pass

from cly.parser import *
from cly.builder import *
from cly.interactive import *