# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_internal/cli/base_command.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 7948 bytes
"""Base Command class, and related routines"""
from __future__ import absolute_import, print_function
import logging, logging.config, optparse, os, platform, sys, traceback
from pip._internal.cli import cmdoptions
from pip._internal.cli.command_context import CommandContextMixIn
from pip._internal.cli.parser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pip._internal.cli.status_codes import ERROR, PREVIOUS_BUILD_DIR_ERROR, SUCCESS, UNKNOWN_ERROR, VIRTUALENV_NOT_FOUND
from pip._internal.exceptions import BadCommand, CommandError, InstallationError, PreviousBuildDirError, UninstallationError
from pip._internal.utils.deprecation import deprecated
from pip._internal.utils.filesystem import check_path_owner
from pip._internal.utils.logging import BrokenStdoutLoggingError, setup_logging
from pip._internal.utils.misc import get_prog, normalize_path
from pip._internal.utils.temp_dir import global_tempdir_manager
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

 L. 113         0  LOAD_FAST                'self'
                2  LOAD_ATTR                enter_context
                4  LOAD_GLOBAL              global_tempdir_manager
                6  CALL_FUNCTION_0       0  '0 positional arguments'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  POP_TOP          

 L. 115        12  LOAD_FAST                'self'
               14  LOAD_ATTR                parse_args
               16  LOAD_FAST                'args'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'options'
               24  STORE_FAST               'args'

 L. 118        26  LOAD_FAST                'options'
               28  LOAD_ATTR                verbose
               30  LOAD_FAST                'options'
               32  LOAD_ATTR                quiet
               34  BINARY_SUBTRACT  
               36  LOAD_FAST                'self'
               38  STORE_ATTR               verbosity

 L. 120        40  LOAD_GLOBAL              setup_logging

 L. 121        42  LOAD_FAST                'self'
               44  LOAD_ATTR                verbosity

 L. 122        46  LOAD_FAST                'options'
               48  LOAD_ATTR                no_color

 L. 123        50  LOAD_FAST                'options'
               52  LOAD_ATTR                log
               54  LOAD_CONST               ('verbosity', 'no_color', 'user_log_file')
               56  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               58  STORE_FAST               'level_number'

 L. 127        60  LOAD_GLOBAL              sys
               62  LOAD_ATTR                version_info
               64  LOAD_CONST               None
               66  LOAD_CONST               2
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  LOAD_CONST               (2, 7)
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   124  'to 124'

 L. 128        78  LOAD_FAST                'options'
               80  LOAD_ATTR                no_python_version_warning
               82  UNARY_NOT        
               84  POP_JUMP_IF_FALSE   124  'to 124'

 L. 131        86  LOAD_STR                 'A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support'
               88  STORE_FAST               'message'

 L. 135        90  LOAD_GLOBAL              platform
               92  LOAD_ATTR                python_implementation
               94  CALL_FUNCTION_0       0  '0 positional arguments'
               96  LOAD_STR                 'CPython'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   110  'to 110'

 L. 137       102  LOAD_STR                 'Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. '

 L. 140       104  LOAD_FAST                'message'
              106  BINARY_ADD       
              108  STORE_FAST               'message'
            110_0  COME_FROM           100  '100'

 L. 141       110  LOAD_GLOBAL              deprecated
              112  LOAD_FAST                'message'
              114  LOAD_CONST               None
              116  LOAD_CONST               None
              118  LOAD_CONST               ('replacement', 'gone_in')
              120  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              122  POP_TOP          
            124_0  COME_FROM            84  '84'
            124_1  COME_FROM            76  '76'

 L. 143       124  LOAD_FAST                'options'
              126  LOAD_ATTR                skip_requirements_regex
              128  POP_JUMP_IF_FALSE   146  'to 146'

 L. 144       130  LOAD_GLOBAL              deprecated

 L. 145       132  LOAD_STR                 '--skip-requirements-regex is unsupported and will be removed'

 L. 147       134  LOAD_STR                 'manage requirements/constraints files explicitly, possibly generating them from metadata'

 L. 150       136  LOAD_STR                 '20.1'

 L. 151       138  LOAD_CONST               7297
              140  LOAD_CONST               ('replacement', 'gone_in', 'issue')
              142  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              144  POP_TOP          
            146_0  COME_FROM           128  '128'

 L. 158       146  LOAD_FAST                'options'
              148  LOAD_ATTR                no_input
              150  POP_JUMP_IF_FALSE   162  'to 162'

 L. 159       152  LOAD_STR                 '1'
              154  LOAD_GLOBAL              os
              156  LOAD_ATTR                environ
              158  LOAD_STR                 'PIP_NO_INPUT'
              160  STORE_SUBSCR     
            162_0  COME_FROM           150  '150'

 L. 161       162  LOAD_FAST                'options'
              164  LOAD_ATTR                exists_action
              166  POP_JUMP_IF_FALSE   186  'to 186'

 L. 162       168  LOAD_STR                 ' '
              170  LOAD_ATTR                join
              172  LOAD_FAST                'options'
              174  LOAD_ATTR                exists_action
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  LOAD_GLOBAL              os
              180  LOAD_ATTR                environ
              182  LOAD_STR                 'PIP_EXISTS_ACTION'
              184  STORE_SUBSCR     
            186_0  COME_FROM           166  '166'

 L. 164       186  LOAD_FAST                'options'
              188  LOAD_ATTR                require_venv
              190  POP_JUMP_IF_FALSE   226  'to 226'
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                ignore_require_venv
              196  UNARY_NOT        
              198  POP_JUMP_IF_FALSE   226  'to 226'

 L. 166       200  LOAD_GLOBAL              running_under_virtualenv
              202  CALL_FUNCTION_0       0  '0 positional arguments'
              204  POP_JUMP_IF_TRUE    226  'to 226'

 L. 167       206  LOAD_GLOBAL              logger
              208  LOAD_ATTR                critical

 L. 168       210  LOAD_STR                 'Could not find an activated virtualenv (required).'
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  POP_TOP          

 L. 170       216  LOAD_GLOBAL              sys
              218  LOAD_ATTR                exit
              220  LOAD_GLOBAL              VIRTUALENV_NOT_FOUND
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  POP_TOP          
            226_0  COME_FROM           204  '204'
            226_1  COME_FROM           198  '198'
            226_2  COME_FROM           190  '190'

 L. 172       226  LOAD_FAST                'options'
              228  LOAD_ATTR                cache_dir
              230  POP_JUMP_IF_FALSE   278  'to 278'

 L. 173       234  LOAD_GLOBAL              normalize_path
              236  LOAD_FAST                'options'
              238  LOAD_ATTR                cache_dir
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  LOAD_FAST                'options'
              244  STORE_ATTR               cache_dir

 L. 174       246  LOAD_GLOBAL              check_path_owner
              248  LOAD_FAST                'options'
              250  LOAD_ATTR                cache_dir
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  POP_JUMP_IF_TRUE    278  'to 278'

 L. 175       258  LOAD_GLOBAL              logger
              260  LOAD_ATTR                warning

 L. 176       262  LOAD_STR                 "The directory '%s' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag."

 L. 181       264  LOAD_FAST                'options'
              266  LOAD_ATTR                cache_dir
              268  CALL_FUNCTION_2       2  '2 positional arguments'
              270  POP_TOP          

 L. 183       272  LOAD_CONST               None
              274  LOAD_FAST                'options'
              276  STORE_ATTR               cache_dir
            278_0  COME_FROM           254  '254'
            278_1  COME_FROM           230  '230'

 L. 185       278  SETUP_FINALLY       648  'to 648'
              282  SETUP_EXCEPT        318  'to 318'

 L. 186       284  LOAD_FAST                'self'
              286  LOAD_ATTR                run
              288  LOAD_FAST                'options'
              290  LOAD_FAST                'args'
              292  CALL_FUNCTION_2       2  '2 positional arguments'
              294  STORE_FAST               'status'

 L. 189       296  LOAD_GLOBAL              isinstance
              298  LOAD_FAST                'status'
              300  LOAD_GLOBAL              int
              302  CALL_FUNCTION_2       2  '2 positional arguments'
              304  POP_JUMP_IF_FALSE   312  'to 312'

 L. 190       308  LOAD_FAST                'status'
              310  RETURN_END_IF    
            312_0  COME_FROM           304  '304'
              312  POP_BLOCK        
              314  JUMP_FORWARD        644  'to 644'
            318_0  COME_FROM_EXCEPT    282  '282'

 L. 191       318  DUP_TOP          
              320  LOAD_GLOBAL              PreviousBuildDirError
              322  COMPARE_OP               exception-match
              324  POP_JUMP_IF_FALSE   380  'to 380'
              328  POP_TOP          
              330  STORE_FAST               'exc'
              332  POP_TOP          
              334  SETUP_FINALLY       368  'to 368'

 L. 192       336  LOAD_GLOBAL              logger
              338  LOAD_ATTR                critical
              340  LOAD_GLOBAL              str
              342  LOAD_FAST                'exc'
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  POP_TOP          

 L. 193       350  LOAD_GLOBAL              logger
              352  LOAD_ATTR                debug
              354  LOAD_STR                 'Exception information:'
              356  LOAD_CONST               True
              358  LOAD_CONST               ('exc_info',)
              360  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              362  POP_TOP          

 L. 195       364  LOAD_GLOBAL              PREVIOUS_BUILD_DIR_ERROR
              366  RETURN_VALUE     
            368_0  COME_FROM_FINALLY   334  '334'
              368  LOAD_CONST               None
              370  STORE_FAST               'exc'
              372  DELETE_FAST              'exc'
              374  END_FINALLY      
              376  JUMP_FORWARD        644  'to 644'
              380  ELSE                     '644'

 L. 196       380  DUP_TOP          
              382  LOAD_GLOBAL              InstallationError
              384  LOAD_GLOBAL              UninstallationError
              386  LOAD_GLOBAL              BadCommand
              388  BUILD_TUPLE_3         3 
              390  COMPARE_OP               exception-match
              392  POP_JUMP_IF_FALSE   446  'to 446'
              396  POP_TOP          
              398  STORE_FAST               'exc'
              400  POP_TOP          
              402  SETUP_FINALLY       436  'to 436'

 L. 197       404  LOAD_GLOBAL              logger
              406  LOAD_ATTR                critical
              408  LOAD_GLOBAL              str
              410  LOAD_FAST                'exc'
              412  CALL_FUNCTION_1       1  '1 positional argument'
              414  CALL_FUNCTION_1       1  '1 positional argument'
              416  POP_TOP          

 L. 198       418  LOAD_GLOBAL              logger
              420  LOAD_ATTR                debug
              422  LOAD_STR                 'Exception information:'
              424  LOAD_CONST               True
              426  LOAD_CONST               ('exc_info',)
              428  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              430  POP_TOP          

 L. 200       432  LOAD_GLOBAL              ERROR
              434  RETURN_VALUE     
            436_0  COME_FROM_FINALLY   402  '402'
              436  LOAD_CONST               None
              438  STORE_FAST               'exc'
              440  DELETE_FAST              'exc'
              442  END_FINALLY      
              444  JUMP_FORWARD        644  'to 644'

 L. 201       446  DUP_TOP          
              448  LOAD_GLOBAL              CommandError
              450  COMPARE_OP               exception-match
              452  POP_JUMP_IF_FALSE   504  'to 504'
              456  POP_TOP          
              458  STORE_FAST               'exc'
              460  POP_TOP          
              462  SETUP_FINALLY       494  'to 494'

 L. 202       464  LOAD_GLOBAL              logger
              466  LOAD_ATTR                critical
              468  LOAD_STR                 '%s'
              470  LOAD_FAST                'exc'
              472  CALL_FUNCTION_2       2  '2 positional arguments'
              474  POP_TOP          

 L. 203       476  LOAD_GLOBAL              logger
              478  LOAD_ATTR                debug
              480  LOAD_STR                 'Exception information:'
              482  LOAD_CONST               True
              484  LOAD_CONST               ('exc_info',)
              486  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              488  POP_TOP          

 L. 205       490  LOAD_GLOBAL              ERROR
              492  RETURN_VALUE     
            494_0  COME_FROM_FINALLY   462  '462'
              494  LOAD_CONST               None
              496  STORE_FAST               'exc'
              498  DELETE_FAST              'exc'
              500  END_FINALLY      
              502  JUMP_FORWARD        644  'to 644'

 L. 206       504  DUP_TOP          
              506  LOAD_GLOBAL              BrokenStdoutLoggingError
              508  COMPARE_OP               exception-match
              510  POP_JUMP_IF_FALSE   564  'to 564'
              514  POP_TOP          
              516  POP_TOP          
              518  POP_TOP          

 L. 209       520  LOAD_GLOBAL              print
              522  LOAD_STR                 'ERROR: Pipe to stdout was broken'
              524  LOAD_GLOBAL              sys
              526  LOAD_ATTR                stderr
              528  LOAD_CONST               ('file',)
              530  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              532  POP_TOP          

 L. 210       534  LOAD_FAST                'level_number'
              536  LOAD_GLOBAL              logging
              538  LOAD_ATTR                DEBUG
              540  COMPARE_OP               <=
              542  POP_JUMP_IF_FALSE   560  'to 560'

 L. 211       546  LOAD_GLOBAL              traceback
              548  LOAD_ATTR                print_exc
              550  LOAD_GLOBAL              sys
              552  LOAD_ATTR                stderr
              554  LOAD_CONST               ('file',)
              556  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              558  POP_TOP          
            560_0  COME_FROM           542  '542'

 L. 213       560  LOAD_GLOBAL              ERROR
              562  RETURN_VALUE     
            564_0  COME_FROM           510  '510'

 L. 214       564  DUP_TOP          
              566  LOAD_GLOBAL              KeyboardInterrupt
              568  COMPARE_OP               exception-match
              570  POP_JUMP_IF_FALSE   608  'to 608'
              574  POP_TOP          
              576  POP_TOP          
              578  POP_TOP          

 L. 215       580  LOAD_GLOBAL              logger
              582  LOAD_ATTR                critical
              584  LOAD_STR                 'Operation cancelled by user'
              586  CALL_FUNCTION_1       1  '1 positional argument'
              588  POP_TOP          

 L. 216       590  LOAD_GLOBAL              logger
              592  LOAD_ATTR                debug
              594  LOAD_STR                 'Exception information:'
              596  LOAD_CONST               True
              598  LOAD_CONST               ('exc_info',)
              600  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              602  POP_TOP          

 L. 218       604  LOAD_GLOBAL              ERROR
              606  RETURN_VALUE     
            608_0  COME_FROM           570  '570'

 L. 219       608  DUP_TOP          
              610  LOAD_GLOBAL              BaseException
              612  COMPARE_OP               exception-match
              614  POP_JUMP_IF_FALSE   642  'to 642'
              618  POP_TOP          
              620  POP_TOP          
              622  POP_TOP          

 L. 220       624  LOAD_GLOBAL              logger
              626  LOAD_ATTR                critical
              628  LOAD_STR                 'Exception:'
              630  LOAD_CONST               True
              632  LOAD_CONST               ('exc_info',)
              634  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              636  POP_TOP          

 L. 222       638  LOAD_GLOBAL              UNKNOWN_ERROR
              640  RETURN_VALUE     
            642_0  COME_FROM           614  '614'
              642  END_FINALLY      
            644_0  COME_FROM           502  '502'
            644_1  COME_FROM           444  '444'
            644_2  COME_FROM           376  '376'
            644_3  COME_FROM           314  '314'
              644  POP_BLOCK        
              646  LOAD_CONST               None
            648_0  COME_FROM_FINALLY   278  '278'

 L. 224       648  LOAD_FAST                'self'
              650  LOAD_ATTR                handle_pip_version_check
              652  LOAD_FAST                'options'
              654  CALL_FUNCTION_1       1  '1 positional argument'
              656  POP_TOP          
              658  END_FINALLY      

 L. 226       660  LOAD_GLOBAL              SUCCESS
              662  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ELSE' instruction at offset 380