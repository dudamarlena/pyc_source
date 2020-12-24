# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cly/__init__.py
# Compiled at: 2007-05-25 01:36:35
__doc__ = 'CLY is a Python module for simplifying the creation of interactive shells.\nKind of like the builtin ``cmd`` module on steroids.\n\nIt has the following features:\n\n  - Tab completion of all commands.\n\n  - Contextual help.\n\n  - Extensible grammar - you can define your own commands with full dynamic\n    completion, contextual help, and so on.\n\n  - Simple. Grammars are constructed from objects using a convenient\n    \'\'function-call\'\' syntax.\n\n  - Flexible command grouping and ordering.\n\n  - Grammar parser, including completion and help enumeration, can be used\n    independently of the readline-based shell. This allows CLY\'s parser to\n    be used in other environments (think "web-based shell" ;))\n\n  - Lots of other cool stuff.\n'
__docformat__ = 'restructuredtext en'
__author__ = 'Alec Thomas <alec@swapoff.org>'
try:
    __version__ = __import__('pkg_resources').get_distribution('cly').version
except ImportError:
    pass

from cly.parser import *
from cly.builder import *
from cly.interactive import *