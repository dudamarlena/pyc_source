# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/constants.py
# Compiled at: 2019-07-17 15:07:37
# Size of source mod 2**32: 542 bytes
"""Constants and definitions"""
QUOTES = [
 '"', "'"]
REDIRECTION_PIPE = '|'
REDIRECTION_OUTPUT = '>'
REDIRECTION_APPEND = '>>'
REDIRECTION_CHARS = [REDIRECTION_PIPE, REDIRECTION_OUTPUT]
REDIRECTION_TOKENS = [REDIRECTION_PIPE, REDIRECTION_OUTPUT, REDIRECTION_APPEND]
COMMENT_CHAR = '#'
MULTILINE_TERMINATOR = ';'
LINE_FEED = '\n'
DEFAULT_SHORTCUTS = {'?':'help', 
 '!':'shell',  '@':'run_script',  '@@':'_relative_run_script'}