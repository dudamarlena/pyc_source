# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/ansi_escapes.py
# Compiled at: 2014-10-30 12:25:10
# Size of source mod 2**32: 2487 bytes
"""
Provides ANSI escape sequences for coloring/formatting output in ANSI terminals.
"""
import os, re
colors = {'black': '\x1b[30m', 
 'red': '\x1b[31m', 
 'green': '\x1b[32m', 
 'yellow': '\x1b[33m', 
 'blue': '\x1b[34m', 
 'magenta': '\x1b[35m', 
 'cyan': '\x1b[36m', 
 'white': '\x1b[37m', 
 'grey': '\x1b[90m', 
 'bold': '\x1b[1m'}
aliases = {'undefined': 'yellow', 
 'pending': 'yellow', 
 'executing': 'grey', 
 'failed': 'red', 
 'passed': 'green', 
 'outline': 'cyan', 
 'skipped': 'cyan', 
 'comments': 'grey', 
 'tag': 'cyan'}
escapes = {'reset': '\x1b[0m', 
 'up': '\x1b[1A'}
if 'GHERKIN_COLORS' in os.environ:
    new_aliases = [p.split('=') for p in os.environ['GHERKIN_COLORS'].split(':')]
    aliases.update(dict(new_aliases))
for alias in aliases:
    escapes[alias] = ''.join([colors[c] for c in aliases[alias].split(',')])
    arg_alias = alias + '_arg'
    arg_seq = aliases.get(arg_alias, aliases[alias] + ',bold')
    escapes[arg_alias] = ''.join([colors[c] for c in arg_seq.split(',')])

def up(n):
    return '\x1b[%dA' % n


_ANSI_ESCAPE_PATTERN = re.compile('\x1b\\[\\d+[mA]', re.UNICODE)

def strip_escapes(text):
    """
    Removes ANSI escape sequences from text (if any are contained).

    :param text: Text that may or may not contain ANSI escape sequences.
    :return: Text without ANSI escape sequences.
    """
    return _ANSI_ESCAPE_PATTERN.sub('', text)


def use_ansi_escape_colorbold_composites():
    """
    Patch for "sphinxcontrib-ansi" to process the following ANSI escapes
    correctly (set-color set-bold sequences):

        ESC[{color}mESC[1m  => ESC[{color};1m

    Reapply aliases to ANSI escapes mapping.
    """
    global escapes
    color_codes = {}
    for color_name, color_escape in colors.items():
        color_code = color_escape.replace('\x1b[', '').replace('m', '')
        color_codes[color_name] = color_code

    for alias in aliases:
        parts = [color_codes[c] for c in aliases[alias].split(',')]
        composite_escape = '\x1b[{0}m'.format(';'.join(parts))
        escapes[alias] = composite_escape
        arg_alias = alias + '_arg'
        arg_seq = aliases.get(arg_alias, aliases[alias] + ',bold')
        parts = [color_codes[c] for c in arg_seq.split(',')]
        composite_escape = '\x1b[{0}m'.format(';'.join(parts))
        escapes[arg_alias] = composite_escape