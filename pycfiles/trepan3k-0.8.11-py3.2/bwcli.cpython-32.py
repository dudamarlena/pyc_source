# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/bwcli.py
# Compiled at: 2015-04-06 04:10:26
""" The hairy command-line interface to the debugger.
"""
import os, os.path, sys
from optparse import OptionParser
from trepan import clifns as Mclifns
from trepan import debugger as Mdebugger, exception as Mexcept, misc as Mmisc
from trepan import file as Mfile
from trepan.interfaces import bullwinkle as Mbullwinkle
__title__ = 'trepan'
from trepan.VERSION import VERSION as __version__

def process_options(debugger_name, pkg_version, sys_argv, option_list=None):
    """Handle debugger options. Set `option_list' if you are writing
    another main program and want to extend the existing set of debugger
    options.

    The options dicionary from opt_parser is return. sys_argv is
    also updated."""
    usage_str = '%prog [debugger-options] [python-script [script-options...]]\n\n       Runs the extended python debugger'
    optparser = OptionParser(usage=usage_str, option_list=option_list, version='%%prog version %s' % pkg_version)
    optparser.add_option('-F', '--fntrace', dest='fntrace', action='store_true', default=False, help='Show functions before executing them. ' + 'This option also sets --batch')
    optparser.add_option('--basename', dest='basename', action='store_true', default=False, help='Filenames strip off basename, (e.g. for regression tests)')
    optparser.add_option('--different', dest='different', action='store_true', default=True, help='Consecutive stops should have different positions')
    optparser.disable_interspersed_args()
    sys.argv = list(sys_argv)
    opts, sys.argv = optparser.parse_args()
    dbg_opts = {}
    return (
     opts, dbg_opts, sys.argv)


def _postprocess_options(dbg, opts):
    """ Handle options (`opts') that feed into the debugger (`dbg')"""
    print_events = []
    if opts.fntrace:
        print_events = [
         'c_call', 'c_return', 'call', 'return']
    if len(print_events):
        dbg.settings['printset'] = frozenset(print_events)
    for setting in ('basename', 'different'):
        dbg.settings[setting] = getattr(opts, setting)

    dbg.settings['highlight'] = 'plain'
    Mdebugger.debugger_obj = dbg


def main--- This code section failed: ---

 L.  98         0  LOAD_GLOBAL              list
                3  LOAD_FAST                'sys_argv'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  STORE_FAST               'orig_sys_argv'

 L.  99        12  LOAD_GLOBAL              process_options
               15  LOAD_GLOBAL              __title__
               18  LOAD_GLOBAL              __version__

 L. 100        21  LOAD_FAST                'sys_argv'
               24  CALL_FUNCTION_3       3  '3 positional, 0 named'
               27  UNPACK_SEQUENCE_3     3 
               30  STORE_FAST               'opts'
               33  STORE_FAST               'dbg_opts'
               36  STORE_FAST               'sys_argv'

 L. 101        39  LOAD_FAST                'sys_argv'
               42  LOAD_FAST                'dbg_opts'
               45  LOAD_STR                 'orig_sys_argv'
               48  STORE_SUBSCR     

 L. 102        49  LOAD_GLOBAL              Mbullwinkle
               52  LOAD_ATTR                BWInterface
               55  CALL_FUNCTION_0       0  '0 positional, 0 named'
               58  LOAD_FAST                'dbg_opts'
               61  LOAD_STR                 'interface'
               64  STORE_SUBSCR     

 L. 103        65  LOAD_STR                 'bullwinkle'
               68  LOAD_FAST                'dbg_opts'
               71  LOAD_STR                 'processor'
               74  STORE_SUBSCR     

 L. 105        75  LOAD_FAST                'dbg'
               78  LOAD_CONST               None
               81  COMPARE_OP               is
               84  POP_JUMP_IF_FALSE   121  'to 121'

 L. 106        87  LOAD_GLOBAL              Mdebugger
               90  LOAD_ATTR                Trepan
               93  LOAD_FAST                'dbg_opts'
               96  CALL_FUNCTION_1       1  '1 positional, 0 named'
               99  STORE_FAST               'dbg'

 L. 107       102  LOAD_FAST                'dbg'
              105  LOAD_ATTR                core
              108  LOAD_ATTR                add_ignore
              111  LOAD_GLOBAL              main
              114  CALL_FUNCTION_1       1  '1 positional, 0 named'
              117  POP_TOP          

 L. 108       118  JUMP_FORWARD        121  'to 121'
            121_0  COME_FROM           118  '118'

 L. 109       121  LOAD_GLOBAL              _postprocess_options
              124  LOAD_FAST                'dbg'
              127  LOAD_FAST                'opts'
              130  CALL_FUNCTION_2       2  '2 positional, 0 named'
              133  POP_TOP          

 L. 114       134  LOAD_GLOBAL              len
              137  LOAD_FAST                'sys_argv'
              140  CALL_FUNCTION_1       1  '1 positional, 0 named'
              143  LOAD_CONST               0
              146  COMPARE_OP               ==
              149  POP_JUMP_IF_FALSE   161  'to 161'

 L. 117       152  LOAD_CONST               None
              155  STORE_FAST               'mainpyfile'
              158  JUMP_FORWARD        430  'to 430'
              161  ELSE                     '430'

 L. 119       161  LOAD_FAST                'sys_argv'
              164  LOAD_CONST               0
              167  BINARY_SUBSCR    
              168  STORE_FAST               'mainpyfile'

 L. 120       171  LOAD_GLOBAL              os
              174  LOAD_ATTR                path
              177  LOAD_ATTR                isfile
              180  LOAD_FAST                'mainpyfile'
              183  CALL_FUNCTION_1       1  '1 positional, 0 named'
              186  POP_JUMP_IF_TRUE    313  'to 313'

 L. 121       189  LOAD_GLOBAL              Mclifns
              192  LOAD_ATTR                whence_file
              195  LOAD_FAST                'mainpyfile'
              198  CALL_FUNCTION_1       1  '1 positional, 0 named'
              201  STORE_FAST               'mainpyfile'

 L. 122       204  LOAD_GLOBAL              Mfile
              207  LOAD_ATTR                readable
              210  LOAD_FAST                'mainpyfile'
              213  CALL_FUNCTION_1       1  '1 positional, 0 named'
              216  STORE_FAST               'is_readable'

 L. 123       219  LOAD_FAST                'is_readable'
              222  LOAD_CONST               None
              225  COMPARE_OP               is
              228  POP_JUMP_IF_FALSE   267  'to 267'

 L. 124       231  LOAD_GLOBAL              print
              234  LOAD_STR                 "%s: Python script file '%s' does not exist"

 L. 125       237  LOAD_GLOBAL              __title__
              240  LOAD_FAST                'mainpyfile'
              243  BUILD_TUPLE_2         2 
              246  BINARY_MODULO    
              247  CALL_FUNCTION_1       1  '1 positional, 0 named'
              250  POP_TOP          

 L. 126       251  LOAD_GLOBAL              sys
              254  LOAD_ATTR                exit
              257  LOAD_CONST               1
              260  CALL_FUNCTION_1       1  '1 positional, 0 named'
              263  POP_TOP          
              264  JUMP_ABSOLUTE       313  'to 313'
              267  ELSE                     '310'

 L. 127       267  LOAD_FAST                'is_readable'
              270  POP_JUMP_IF_TRUE    313  'to 313'

 L. 128       273  LOAD_GLOBAL              print
              276  LOAD_STR                 "%s: Can't read Python script file '%s'"

 L. 129       279  LOAD_GLOBAL              __title__
              282  LOAD_FAST                'mainpyfile'
              285  BUILD_TUPLE_2         2 
              288  BINARY_MODULO    
              289  CALL_FUNCTION_1       1  '1 positional, 0 named'
              292  POP_TOP          

 L. 130       293  LOAD_GLOBAL              sys
              296  LOAD_ATTR                exit
              299  LOAD_CONST               1
              302  CALL_FUNCTION_1       1  '1 positional, 0 named'
              305  POP_TOP          

 L. 131       306  LOAD_CONST               None
              309  RETURN_END_IF    
              310  JUMP_FORWARD        313  'to 313'
            313_0  COME_FROM           310  '310'

 L. 135       313  LOAD_GLOBAL              Mfile
              316  LOAD_ATTR                file_pyc2py
              319  LOAD_FAST                'mainpyfile'
              322  CALL_FUNCTION_1       1  '1 positional, 0 named'
              325  STORE_FAST               'mainpyfile_noopt'

 L. 136       328  LOAD_FAST                'mainpyfile'
              331  LOAD_FAST                'mainpyfile_noopt'
              334  COMPARE_OP               !=
              337  POP_JUMP_IF_FALSE   398  'to 398'

 L. 137       340  LOAD_GLOBAL              Mfile
              343  LOAD_ATTR                readable
              346  LOAD_FAST                'mainpyfile_noopt'
              349  CALL_FUNCTION_1       1  '1 positional, 0 named'
            352_0  COME_FROM           337  '337'
              352  POP_JUMP_IF_FALSE   398  'to 398'

 L. 138       355  LOAD_GLOBAL              print
              358  LOAD_STR                 "%s: Compiled Python script given and we can't use that."

 L. 139       361  LOAD_GLOBAL              __title__
              364  BINARY_MODULO    
              365  CALL_FUNCTION_1       1  '1 positional, 0 named'
              368  POP_TOP          

 L. 140       369  LOAD_GLOBAL              print
              372  LOAD_STR                 '%s: Substituting non-compiled name: %s'

 L. 141       375  LOAD_GLOBAL              __title__
              378  LOAD_FAST                'mainpyfile_noopt'
              381  BUILD_TUPLE_2         2 
              384  BINARY_MODULO    
              385  CALL_FUNCTION_1       1  '1 positional, 0 named'
              388  POP_TOP          

 L. 142       389  LOAD_FAST                'mainpyfile_noopt'
              392  STORE_FAST               'mainpyfile'

 L. 143       395  JUMP_FORWARD        398  'to 398'
            398_0  COME_FROM           395  '395'

 L. 147       398  LOAD_GLOBAL              os
              401  LOAD_ATTR                path
              404  LOAD_ATTR                dirname
              407  LOAD_FAST                'mainpyfile'
              410  CALL_FUNCTION_1       1  '1 positional, 0 named'
              413  DUP_TOP          
              414  LOAD_GLOBAL              sys
              417  LOAD_ATTR                path
              420  LOAD_CONST               0
              423  STORE_SUBSCR     
              424  LOAD_FAST                'dbg'
              427  STORE_ATTR               main_dirname
            430_0  COME_FROM           158  '158'

 L. 151       430  LOAD_CONST               False
              433  LOAD_FAST                'dbg'
              436  STORE_ATTR               sig_received

 L. 158       439  SETUP_LOOP          766  'to 766'

 L. 163       442  SETUP_EXCEPT        568  'to 568'

 L. 164       445  LOAD_FAST                'dbg'
              448  LOAD_ATTR                program_sys_argv
              451  POP_JUMP_IF_FALSE   488  'to 488'
              454  LOAD_FAST                'mainpyfile'
            457_0  COME_FROM           451  '451'
              457  POP_JUMP_IF_FALSE   488  'to 488'

 L. 165       460  LOAD_FAST                'dbg'
              463  LOAD_ATTR                run_script
              466  LOAD_FAST                'mainpyfile'
              469  CALL_FUNCTION_1       1  '1 positional, 0 named'
              472  STORE_FAST               'normal_termination'

 L. 166       475  LOAD_FAST                'normal_termination'
              478  POP_JUMP_IF_TRUE    516  'to 516'

 L. 166       481  BREAK_LOOP       
              482  JUMP_ABSOLUTE       516  'to 516'
              485  JUMP_FORWARD        516  'to 516'
              488  ELSE                     '516'

 L. 168       488  LOAD_STR                 'No program'
              491  LOAD_FAST                'dbg'
              494  LOAD_ATTR                core
              497  STORE_ATTR               execution_status

 L. 169       500  LOAD_FAST                'dbg'
              503  LOAD_ATTR                core
              506  LOAD_ATTR                processor
              509  LOAD_ATTR                process_commands
              512  CALL_FUNCTION_0       0  '0 positional, 0 named'
              515  POP_TOP          
            516_0  COME_FROM           485  '485'

 L. 172       516  LOAD_STR                 'Terminated'
              519  LOAD_FAST                'dbg'
              522  LOAD_ATTR                core
              525  STORE_ATTR               execution_status

 L. 173       528  LOAD_FAST                'dbg'
              531  LOAD_ATTR                intf
              534  LOAD_CONST               -1
              537  BINARY_SUBSCR    
              538  LOAD_ATTR                msg
              541  LOAD_STR                 'The program finished - quit or restart'
              544  CALL_FUNCTION_1       1  '1 positional, 0 named'
              547  POP_TOP          

 L. 174       548  LOAD_FAST                'dbg'
              551  LOAD_ATTR                core
              554  LOAD_ATTR                processor
              557  LOAD_ATTR                process_commands
              560  CALL_FUNCTION_0       0  '0 positional, 0 named'
              563  POP_TOP          
              564  POP_BLOCK        
              565  JUMP_BACK           442  'to 442'
            568_0  COME_FROM_EXCEPT    442  '442'

 L. 175       568  DUP_TOP          
              569  LOAD_GLOBAL              Mexcept
              572  LOAD_ATTR                DebuggerQuit
              575  COMPARE_OP               exception-match
              578  POP_JUMP_IF_FALSE   589  'to 589'
              581  POP_TOP          
              582  POP_TOP          
              583  POP_TOP          

 L. 176       584  BREAK_LOOP       
              585  POP_EXCEPT       
              586  JUMP_BACK           442  'to 442'

 L. 177       589  DUP_TOP          
              590  LOAD_GLOBAL              Mexcept
              593  LOAD_ATTR                DebuggerRestart
              596  COMPARE_OP               exception-match
              599  POP_JUMP_IF_FALSE   744  'to 744'
              602  POP_TOP          
              603  POP_TOP          
              604  POP_TOP          

 L. 178       605  LOAD_STR                 'Restart requested'
              608  LOAD_FAST                'dbg'
              611  LOAD_ATTR                core
              614  STORE_ATTR               execution_status

 L. 179       617  LOAD_FAST                'dbg'
              620  LOAD_ATTR                program_sys_argv
              623  POP_JUMP_IF_FALSE   739  'to 739'

 L. 180       626  LOAD_GLOBAL              list
              629  LOAD_FAST                'dbg'
              632  LOAD_ATTR                program_sys_argv
              635  CALL_FUNCTION_1       1  '1 positional, 0 named'
              638  LOAD_GLOBAL              sys
              641  STORE_ATTR               argv

 L. 181       644  LOAD_STR                 'Restarting %s with arguments:'

 L. 182       647  LOAD_FAST                'dbg'
              650  LOAD_ATTR                core
              653  LOAD_ATTR                filename
              656  LOAD_FAST                'mainpyfile'
              659  CALL_FUNCTION_1       1  '1 positional, 0 named'
              662  BINARY_MODULO    
              663  STORE_FAST               'part1'

 L. 183       666  LOAD_STR                 ' '
              669  LOAD_ATTR                join
              672  LOAD_FAST                'dbg'
              675  LOAD_ATTR                program_sys_argv
              678  LOAD_CONST               1
              681  LOAD_CONST               None
              684  BUILD_SLICE_2         2 
              687  BINARY_SUBSCR    
              688  CALL_FUNCTION_1       1  '1 positional, 0 named'
              691  STORE_FAST               'args'

 L. 184       694  LOAD_FAST                'dbg'
              697  LOAD_ATTR                intf
              700  LOAD_CONST               -1
              703  BINARY_SUBSCR    
              704  LOAD_ATTR                msg
              707  LOAD_GLOBAL              Mmisc
              710  LOAD_ATTR                wrapped_lines
              713  LOAD_FAST                'part1'
              716  LOAD_FAST                'args'

 L. 185       719  LOAD_FAST                'dbg'
              722  LOAD_ATTR                settings
              725  LOAD_STR                 'width'
              728  BINARY_SUBSCR    
              729  CALL_FUNCTION_3       3  '3 positional, 0 named'
              732  CALL_FUNCTION_1       1  '1 positional, 0 named'
              735  POP_TOP          
              736  JUMP_FORWARD        740  'to 740'
              739  ELSE                     '740'

 L. 186       739  BREAK_LOOP       
            740_0  COME_FROM           736  '736'
              740  POP_EXCEPT       
              741  JUMP_BACK           442  'to 442'

 L. 187       744  DUP_TOP          
              745  LOAD_GLOBAL              SystemExit
              748  COMPARE_OP               exception-match
              751  POP_JUMP_IF_FALSE   762  'to 762'
              754  POP_TOP          
              755  POP_TOP          
              756  POP_TOP          

 L. 189       757  BREAK_LOOP       
              758  POP_EXCEPT       
              759  JUMP_BACK           442  'to 442'
              762  END_FINALLY      

 L. 190       763  CONTINUE            442  'to 442'
            766_0  COME_FROM_LOOP      439  '439'

 L. 193       766  LOAD_FAST                'orig_sys_argv'
              769  LOAD_GLOBAL              sys
              772  STORE_ATTR               argv

 L. 194       775  LOAD_CONST               None
              778  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 766


if __name__ == '__main__':
    main()
# global __title__ ## Warning: Unused global