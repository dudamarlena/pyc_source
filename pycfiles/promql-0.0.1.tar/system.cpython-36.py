# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/contrib/completers/system.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 1918 bytes
from __future__ import unicode_literals
from prompt_tool_kit.contrib.regular_languages.completion import GrammarCompleter
from prompt_tool_kit.contrib.regular_languages.compiler import compile
from .filesystem import PathCompleter, ExecutableCompleter
__all__ = ('SystemCompleter', )

class SystemCompleter(GrammarCompleter):
    """SystemCompleter"""

    def __init__(self):
        g = compile('\n                # First we have an executable.\n                (?P<executable>[^\\s]+)\n\n                # Ignore literals in between.\n                (\n                    \\s+\n                    ("[^"]*" | \'[^\']*\' | [^\'"]+ )\n                )*\n\n                \\s+\n\n                # Filename as parameters.\n                (\n                    (?P<filename>[^\\s]+) |\n                    "(?P<double_quoted_filename>[^\\s]+)" |\n                    \'(?P<single_quoted_filename>[^\\s]+)\'\n                )\n            ',
          escape_funcs={'double_quoted_filename':lambda string: string.replace('"', '\\"'), 
         'single_quoted_filename':lambda string: string.replace("'", "\\'")},
          unescape_funcs={'double_quoted_filename':lambda string: string.replace('\\"', '"'), 
         'single_quoted_filename':lambda string: string.replace("\\'", "'")})
        super(SystemCompleter, self).__init__(g, {'executable':ExecutableCompleter(), 
         'filename':PathCompleter(only_directories=False, expanduser=True), 
         'double_quoted_filename':PathCompleter(only_directories=False, expanduser=True), 
         'single_quoted_filename':PathCompleter(only_directories=False, expanduser=True)})