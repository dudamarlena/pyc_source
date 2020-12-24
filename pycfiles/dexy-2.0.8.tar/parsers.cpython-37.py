# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/parsers.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 990 bytes
from dexy.utils import defaults
from dexy.commands.utils import dummy_wrapper
from dexy.parser import AbstractSyntaxTree
from dexy.parser import Parser

def parsers_command():
    wrapper = dummy_wrapper()
    ast = AbstractSyntaxTree(wrapper)
    processed_aliases = set()
    for alias in sorted(Parser.plugins):
        if alias in processed_aliases:
            continue
        parser = Parser.create_instance(alias, ast, wrapper)
        for alias in parser.aliases:
            processed_aliases.add(alias)

        print('%s Parser' % parser.__class__.__name__)
        print('')
        print(parser.setting('help'))
        print('')
        print('aliases:')
        for alias in parser.aliases:
            print('  %s' % alias)

        print('')

    print('Default parsers are: ' + defaults['parsers'])
    print('')
    print('Dexy will only look for config files to parse in the root directory')
    print('of your project unless --recurse is specified.')
    print('')