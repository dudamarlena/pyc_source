# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/color_print.py
# Compiled at: 2019-08-16 00:20:51
# Size of source mod 2**32: 964 bytes
"""
provide colorized output
"""
from __future__ import print_function, unicode_literals
import sys
from prompt_tool_kit.shortcuts import print_tokens, style_from_dict, Token

def _print_token_factory(col):
    """Internal helper to provide color names."""

    def _helper(msg):
        style = style_from_dict({Token.Color: col})
        tokens = [
         (
          Token.Color, msg)]
        print_tokens(tokens, style=style)

    def _helper_no_terminal(msg):
        print(msg)

    if sys.stdout.isatty():
        return _helper
    else:
        return _helper_no_terminal


yellow = _print_token_factory('#dfaf00')
blue = _print_token_factory('#0087ff')
gray = _print_token_factory('#6c6c6c')