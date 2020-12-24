# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/cli/base_command.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 6504 bytes
"""Base Command class, and related routines"""
from __future__ import absolute_import, print_function
import logging, logging.config, optparse, os, platform, sys, traceback
from pip._internal.cli import cmdoptions
from pip._internal.cli.command_context import CommandContextMixIn
from pip._internal.cli.parser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pip._internal.cli.status_codes import ERROR, PREVIOUS_BUILD_DIR_ERROR, SUCCESS, UNKNOWN_ERROR, VIRTUALENV_NOT_FOUND
from pip._internal.exceptions import BadCommand, CommandError, InstallationError, PreviousBuildDirError, UninstallationError
from pip._internal.utils.deprecation import deprecated
from pip._internal.utils.logging import BrokenStdoutLoggingError, setup_logging
from pip._internal.utils.misc import get_prog
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.virtualenv import running_under_virtualenv
if MYPY_CHECK_RUNNING:
    from typing import List, Tuple, Any
    from optparse import Values
__all__ = [
 'Command']
logger = logging.getLogger(__name__)

class Command(CommandContextMixIn):
    usage = None
    ignore_require_venv = False

    def __init__(self, name, summary, isolated=False):
        super(Command, self).__init__()
        parser_kw = {'usage':self.usage, 
         'prog':'%s %s' % (get_prog(), name), 
         'formatter':UpdatingDefaultsHelpFormatter(), 
         'add_help_option':False, 
         'name':name, 
         'description':self.__doc__, 
         'isolated':isolated}
        self.name = name
        self.summary = summary
        self.parser = ConfigOptionParser(**parser_kw)
        optgroup_name = '%s Options' % self.name.capitalize()
        self.cmd_opts = optparse.OptionGroup(self.parser, optgroup_name)
        gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, self.parser)
        self.parser.add_option_group(gen_opts)

    def handle_pip_version_check(self, options):
        """
        This is a no-op so that commands by default do not do the pip version
        check.
        """
        assert not hasattr(options, 'no_index')

    def run(self, options, args):
        raise NotImplementedError

    def parse_args(self, args):
        return self.parser.parse_args(args)

    def main(self, args):
        try:
            with self.main_context():
                return self._main(args)
        finally:
            logging.shutdown()

    def _main--- This code section failed: ---

 L. 109         0  LOAD_FAST                'self'
                2  LOAD_ATTR                parse_args
                4  LOAD_FAST                'args'
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'options'
               12  STORE_FAST               'args'

 L. 112        14  LOAD_FAST                'options'
               16  LOAD_ATTR                verbose
               18  LOAD_FAST                'options'
               20  LOAD_ATTR                quiet
               22  BINARY_SUBTRACT  
               24  LOAD_FAST                'self'
               26  STORE_ATTR               verbosity

 L. 114        28  LOAD_GLOBAL              setup_logging

 L. 115        30  LOAD_FAST                'self'
               32  LOAD_ATTR                verbosity

 L. 116        34  LOAD_FAST                'options'
               36  LOAD_ATTR                no_color

 L. 117        38  LOAD_FAST                'options'
               40  LOAD_ATTR                log
               42  LOAD_CONST               ('verbosity', 'no_color', 'user_log_file')
               44  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               46  STORE_FAST               'level_number'

 L. 120        48  LOAD_GLOBAL              sys
               50  LOAD_ATTR                version_info
               52  LOAD_CONST               None
               54  LOAD_CONST               2
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  LOAD_CONST               (2, 7)
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE   104  'to 104'

 L. 122        66  LOAD_STR                 'A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support'
               68  STORE_FAST               'message'

 L. 126        70  LOAD_GLOBAL              platform
               72  LOAD_ATTR                python_implementation
               74  CALL_FUNCTION_0       0  '0 positional arguments'
               76  LOAD_STR                 'CPython'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 128        82  LOAD_STR                 "Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date. "

 L. 131        84  LOAD_FAST                'message'
               86  BINARY_ADD       
               88  STORE_FAST               'message'
             90_0  COME_FROM            80  '80'

 L. 132        90  LOAD_GLOBAL              deprecated
               92  LOAD_FAST                'message'
               94  LOAD_CONST               None
               96  LOAD_CONST               None
               98  LOAD_CONST               ('replacement', 'gone_in')
              100  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              102  POP_TOP          
            104_0  COME_FROM            64  '64'

 L. 138       104  LOAD_FAST                'options'
              106  LOAD_ATTR                no_input
              108  POP_JUMP_IF_FALSE   120  'to 120'

 L. 139       110  LOAD_STR                 '1'
              112  LOAD_GLOBAL              os
              114  LOAD_ATTR                environ
              116  LOAD_STR                 'PIP_NO_INPUT'
              118  STORE_SUBSCR     
            120_0  COME_FROM           108  '108'

 L. 141       120  LOAD_FAST                'options'
              122  LOAD_ATTR                exists_action
              124  POP_JUMP_IF_FALSE   144  'to 144'

 L. 142       126  LOAD_STR                 ' '
              128  LOAD_ATTR                join
              130  LOAD_FAST                'options'
              132  LOAD_ATTR                exists_action
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  LOAD_GLOBAL              os
              138  LOAD_ATTR                environ
              140  LOAD_STR                 'PIP_EXISTS_ACTION'
              142  STORE_SUBSCR     
            144_0  COME_FROM           124  '124'

 L. 144       144  LOAD_FAST                'options'
              146  LOAD_ATTR                require_venv
              148  POP_JUMP_IF_FALSE   184  'to 184'
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                ignore_require_venv
              154  UNARY_NOT        
              156  POP_JUMP_IF_FALSE   184  'to 184'

 L. 146       158  LOAD_GLOBAL              running_under_virtualenv
              160  CALL_FUNCTION_0       0  '0 positional arguments'
              162  POP_JUMP_IF_TRUE    184  'to 184'

 L. 147       164  LOAD_GLOBAL              logger
              166  LOAD_ATTR                critical

 L. 148       168  LOAD_STR                 'Could not find an activated virtualenv (required).'
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  POP_TOP          

 L. 150       174  LOAD_GLOBAL              sys
              176  LOAD_ATTR                exit
              178  LOAD_GLOBAL              VIRTUALENV_NOT_FOUND
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  POP_TOP          
            184_0  COME_FROM           162  '162'
            184_1  COME_FROM           156  '156'
            184_2  COME_FROM           148  '148'

 L. 152       184  SETUP_FINALLY       552  'to 552'
              188  SETUP_EXCEPT        222  'to 222'

 L. 153       190  LOAD_FAST                'self'
              192  LOAD_ATTR                run
              194  LOAD_FAST                'options'
              196  LOAD_FAST                'args'
              198  CALL_FUNCTION_2       2  '2 positional arguments'
              200  STORE_FAST               'status'

 L. 156       202  LOAD_GLOBAL              isinstance
              204  LOAD_FAST                'status'
              206  LOAD_GLOBAL              int
              208  CALL_FUNCTION_2       2  '2 positional arguments'
              210  POP_JUMP_IF_FALSE   216  'to 216'

 L. 157       212  LOAD_FAST                'status'
              214  RETURN_END_IF    
            216_0  COME_FROM           210  '210'
              216  POP_BLOCK        
              218  JUMP_FORWARD        548  'to 548'
            222_0  COME_FROM_EXCEPT    188  '188'

 L. 158       222  DUP_TOP          
              224  LOAD_GLOBAL              PreviousBuildDirError
              226  COMPARE_OP               exception-match
              228  POP_JUMP_IF_FALSE   284  'to 284'
              232  POP_TOP          
              234  STORE_FAST               'exc'
              236  POP_TOP          
              238  SETUP_FINALLY       272  'to 272'

 L. 159       240  LOAD_GLOBAL              logger
              242  LOAD_ATTR                critical
              244  LOAD_GLOBAL              str
              246  LOAD_FAST                'exc'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  POP_TOP          

 L. 160       254  LOAD_GLOBAL              logger
              256  LOAD_ATTR                debug
              258  LOAD_STR                 'Exception information:'
              260  LOAD_CONST               True
              262  LOAD_CONST               ('exc_info',)
              264  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              266  POP_TOP          

 L. 162       268  LOAD_GLOBAL              PREVIOUS_BUILD_DIR_ERROR
              270  RETURN_VALUE     
            272_0  COME_FROM_FINALLY   238  '238'
              272  LOAD_CONST               None
              274  STORE_FAST               'exc'
              276  DELETE_FAST              'exc'
              278  END_FINALLY      
              280  JUMP_FORWARD        548  'to 548'
              284  ELSE                     '548'

 L. 163       284  DUP_TOP          
              286  LOAD_GLOBAL              InstallationError
              288  LOAD_GLOBAL              UninstallationError
              290  LOAD_GLOBAL              BadCommand
              292  BUILD_TUPLE_3         3 
              294  COMPARE_OP               exception-match
              296  POP_JUMP_IF_FALSE   350  'to 350'
              300  POP_TOP          
              302  STORE_FAST               'exc'
              304  POP_TOP          
              306  SETUP_FINALLY       340  'to 340'

 L. 164       308  LOAD_GLOBAL              logger
              310  LOAD_ATTR                critical
              312  LOAD_GLOBAL              str
              314  LOAD_FAST                'exc'
              316  CALL_FUNCTION_1       1  '1 positional argument'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  POP_TOP          

 L. 165       322  LOAD_GLOBAL              logger
              324  LOAD_ATTR                debug
              326  LOAD_STR                 'Exception information:'
              328  LOAD_CONST               True
              330  LOAD_CONST               ('exc_info',)
              332  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              334  POP_TOP          

 L. 167       336  LOAD_GLOBAL              ERROR
              338  RETURN_VALUE     
            340_0  COME_FROM_FINALLY   306  '306'
              340  LOAD_CONST               None
              342  STORE_FAST               'exc'
              344  DELETE_FAST              'exc'
              346  END_FINALLY      
              348  JUMP_FORWARD        548  'to 548'

 L. 168       350  DUP_TOP          
              352  LOAD_GLOBAL              CommandError
              354  COMPARE_OP               exception-match
              356  POP_JUMP_IF_FALSE   408  'to 408'
              360  POP_TOP          
              362  STORE_FAST               'exc'
              364  POP_TOP          
              366  SETUP_FINALLY       398  'to 398'

 L. 169       368  LOAD_GLOBAL              logger
              370  LOAD_ATTR                critical
              372  LOAD_STR                 '%s'
              374  LOAD_FAST                'exc'
              376  CALL_FUNCTION_2       2  '2 positional arguments'
              378  POP_TOP          

 L. 170       380  LOAD_GLOBAL              logger
              382  LOAD_ATTR                debug
              384  LOAD_STR                 'Exception information:'
              386  LOAD_CONST               True
              388  LOAD_CONST               ('exc_info',)
              390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              392  POP_TOP          

 L. 172       394  LOAD_GLOBAL              ERROR
              396  RETURN_VALUE     
            398_0  COME_FROM_FINALLY   366  '366'
              398  LOAD_CONST               None
              400  STORE_FAST               'exc'
              402  DELETE_FAST              'exc'
              404  END_FINALLY      
              406  JUMP_FORWARD        548  'to 548'

 L. 173       408  DUP_TOP          
              410  LOAD_GLOBAL              BrokenStdoutLoggingError
              412  COMPARE_OP               exception-match
              414  POP_JUMP_IF_FALSE   468  'to 468'
              418  POP_TOP          
              420  POP_TOP          
              422  POP_TOP          

 L. 176       424  LOAD_GLOBAL              print
              426  LOAD_STR                 'ERROR: Pipe to stdout was broken'
              428  LOAD_GLOBAL              sys
              430  LOAD_ATTR                stderr
              432  LOAD_CONST               ('file',)
              434  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              436  POP_TOP          

 L. 177       438  LOAD_FAST                'level_number'
              440  LOAD_GLOBAL              logging
              442  LOAD_ATTR                DEBUG
              444  COMPARE_OP               <=
              446  POP_JUMP_IF_FALSE   464  'to 464'

 L. 178       450  LOAD_GLOBAL              traceback
              452  LOAD_ATTR                print_exc
              454  LOAD_GLOBAL              sys
              456  LOAD_ATTR                stderr
              458  LOAD_CONST               ('file',)
              460  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              462  POP_TOP          
            464_0  COME_FROM           446  '446'

 L. 180       464  LOAD_GLOBAL              ERROR
              466  RETURN_VALUE     
            468_0  COME_FROM           414  '414'

 L. 181       468  DUP_TOP          
              470  LOAD_GLOBAL              KeyboardInterrupt
              472  COMPARE_OP               exception-match
              474  POP_JUMP_IF_FALSE   512  'to 512'
              478  POP_TOP          
              480  POP_TOP          
              482  POP_TOP          

 L. 182       484  LOAD_GLOBAL              logger
              486  LOAD_ATTR                critical
              488  LOAD_STR                 'Operation cancelled by user'
              490  CALL_FUNCTION_1       1  '1 positional argument'
              492  POP_TOP          

 L. 183       494  LOAD_GLOBAL              logger
              496  LOAD_ATTR                debug
              498  LOAD_STR                 'Exception information:'
              500  LOAD_CONST               True
              502  LOAD_CONST               ('exc_info',)
              504  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              506  POP_TOP          

 L. 185       508  LOAD_GLOBAL              ERROR
              510  RETURN_VALUE     
            512_0  COME_FROM           474  '474'

 L. 186       512  DUP_TOP          
              514  LOAD_GLOBAL              BaseException
              516  COMPARE_OP               exception-match
              518  POP_JUMP_IF_FALSE   546  'to 546'
              522  POP_TOP          
              524  POP_TOP          
              526  POP_TOP          

 L. 187       528  LOAD_GLOBAL              logger
              530  LOAD_ATTR                critical
              532  LOAD_STR                 'Exception:'
              534  LOAD_CONST               True
              536  LOAD_CONST               ('exc_info',)
              538  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              540  POP_TOP          

 L. 189       542  LOAD_GLOBAL              UNKNOWN_ERROR
              544  RETURN_VALUE     
            546_0  COME_FROM           518  '518'
              546  END_FINALLY      
            548_0  COME_FROM           406  '406'
            548_1  COME_FROM           348  '348'
            548_2  COME_FROM           280  '280'
            548_3  COME_FROM           218  '218'
              548  POP_BLOCK        
              550  LOAD_CONST               None
            552_0  COME_FROM_FINALLY   184  '184'

 L. 191       552  LOAD_FAST                'self'
              554  LOAD_ATTR                handle_pip_version_check
              556  LOAD_FAST                'options'
              558  CALL_FUNCTION_1       1  '1 positional argument'
              560  POP_TOP          
              562  END_FINALLY      

 L. 193       564  LOAD_GLOBAL              SUCCESS
              566  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ELSE' instruction at offset 284