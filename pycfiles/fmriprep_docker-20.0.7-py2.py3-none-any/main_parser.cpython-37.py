# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/cli/main_parser.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 2843 bytes
"""A single place for constructing and exposing the main parser
"""
import os, sys
from pip._internal.cli import cmdoptions
from pip._internal.cli.parser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pip._internal.commands import commands_dict, get_similar_commands
from pip._internal.exceptions import CommandError
from pip._internal.utils.misc import get_pip_version, get_prog
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Tuple, List
__all__ = ['create_main_parser', 'parse_command']

def create_main_parser():
    """Creates and returns the main parser for pip's CLI
    """
    parser_kw = {'usage':'\n%prog <command> [options]', 
     'add_help_option':False, 
     'formatter':UpdatingDefaultsHelpFormatter(), 
     'name':'global', 
     'prog':get_prog()}
    parser = ConfigOptionParser(**parser_kw)
    parser.disable_interspersed_args()
    parser.version = get_pip_version()
    gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, parser)
    parser.add_option_group(gen_opts)
    parser.main = True
    description = [
     ''] + [('{name:27} {command_info.summary}'.format)(**locals()) for name, command_info in commands_dict.items()]
    parser.description = '\n'.join(description)
    return parser


def parse_command--- This code section failed: ---

 L.  61         0  LOAD_GLOBAL              create_main_parser
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'parser'

 L.  70         6  LOAD_FAST                'parser'
                8  LOAD_METHOD              parse_args
               10  LOAD_FAST                'args'
               12  CALL_METHOD_1         1  '1 positional argument'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'general_options'
               18  STORE_FAST               'args_else'

 L.  73        20  LOAD_FAST                'general_options'
               22  LOAD_ATTR                version
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L.  74        26  LOAD_GLOBAL              sys
               28  LOAD_ATTR                stdout
               30  LOAD_METHOD              write
               32  LOAD_FAST                'parser'
               34  LOAD_ATTR                version
               36  CALL_METHOD_1         1  '1 positional argument'
               38  POP_TOP          

 L.  75        40  LOAD_GLOBAL              sys
               42  LOAD_ATTR                stdout
               44  LOAD_METHOD              write
               46  LOAD_GLOBAL              os
               48  LOAD_ATTR                linesep
               50  CALL_METHOD_1         1  '1 positional argument'
               52  POP_TOP          

 L.  76        54  LOAD_GLOBAL              sys
               56  LOAD_METHOD              exit
               58  CALL_METHOD_0         0  '0 positional arguments'
               60  POP_TOP          
             62_0  COME_FROM            24  '24'

 L.  79        62  LOAD_FAST                'args_else'
               64  POP_JUMP_IF_FALSE    90  'to 90'
               66  LOAD_FAST                'args_else'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  LOAD_STR                 'help'
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   106  'to 106'
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'args_else'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  LOAD_CONST               1
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   106  'to 106'
             90_0  COME_FROM            64  '64'

 L.  80        90  LOAD_FAST                'parser'
               92  LOAD_METHOD              print_help
               94  CALL_METHOD_0         0  '0 positional arguments'
               96  POP_TOP          

 L.  81        98  LOAD_GLOBAL              sys
              100  LOAD_METHOD              exit
              102  CALL_METHOD_0         0  '0 positional arguments'
              104  POP_TOP          
            106_0  COME_FROM            88  '88'
            106_1  COME_FROM            76  '76'

 L.  84       106  LOAD_FAST                'args_else'
              108  LOAD_CONST               0
              110  BINARY_SUBSCR    
              112  STORE_FAST               'cmd_name'

 L.  86       114  LOAD_FAST                'cmd_name'
              116  LOAD_GLOBAL              commands_dict
              118  COMPARE_OP               not-in
              120  POP_JUMP_IF_FALSE   176  'to 176'

 L.  87       122  LOAD_GLOBAL              get_similar_commands
              124  LOAD_FAST                'cmd_name'
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  STORE_FAST               'guess'

 L.  89       130  LOAD_STR                 'unknown command "{}"'
              132  LOAD_METHOD              format
              134  LOAD_FAST                'cmd_name'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  BUILD_LIST_1          1 
              140  STORE_FAST               'msg'

 L.  90       142  LOAD_FAST                'guess'
              144  POP_JUMP_IF_FALSE   162  'to 162'

 L.  91       146  LOAD_FAST                'msg'
              148  LOAD_METHOD              append
              150  LOAD_STR                 'maybe you meant "{}"'
              152  LOAD_METHOD              format
              154  LOAD_FAST                'guess'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          
            162_0  COME_FROM           144  '144'

 L.  93       162  LOAD_GLOBAL              CommandError
              164  LOAD_STR                 ' - '
              166  LOAD_METHOD              join
              168  LOAD_FAST                'msg'
              170  CALL_METHOD_1         1  '1 positional argument'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  RAISE_VARARGS_1       1  'exception instance'
            176_0  COME_FROM           120  '120'

 L.  96       176  LOAD_FAST                'args'
              178  LOAD_CONST               None
              180  LOAD_CONST               None
              182  BUILD_SLICE_2         2 
              184  BINARY_SUBSCR    
              186  STORE_FAST               'cmd_args'

 L.  97       188  LOAD_FAST                'cmd_args'
              190  LOAD_METHOD              remove
              192  LOAD_FAST                'cmd_name'
              194  CALL_METHOD_1         1  '1 positional argument'
              196  POP_TOP          

 L.  99       198  LOAD_FAST                'cmd_name'
              200  LOAD_FAST                'cmd_args'
              202  BUILD_TUPLE_2         2 
              204  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 204