# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/disassemble.py
# Compiled at: 2018-03-08 08:43:13
# Size of source mod 2**32: 7912 bytes
import inspect, os, sys
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import disassemble as Mdis, file as Mfile
from xdis.load import load_module
from trepan.processor.cmd_addrlist import parse_addr_list_cmd
DEBUG_BYTECODE_SUFFIXES = [
 '.pyc']
OPTIMIZED_BYTECODE_SUFFIXES = ['.pyo']
_PYCACHE = '__pycache__'

def cache_from_source(path, debug_override=None):
    """Given the path to a .py file, return the path to its .pyc/.pyo file.

    The .py file does not need to exist; this simply returns the path to the
    .pyc/.pyo file calculated as if the .py file were imported.  The extension
    will be .pyc unless sys.flags.optimize is non-zero, then it will be .pyo.

    If debug_override is not None, then it must be a boolean and is used in
    place of sys.flags.optimize.

    If sys.implementation.cache_tag is None then NotImplementedError is raised.

    """
    debug = not sys.flags.optimize if debug_override is None else debug_override
    if debug:
        suffixes = DEBUG_BYTECODE_SUFFIXES
    else:
        suffixes = OPTIMIZED_BYTECODE_SUFFIXES
    head, tail = os.path.split(path)
    base_filename, sep, _ = tail.partition('.')
    if not hasattr(sys, 'implementation'):
        raise NotImplementedError('No sys.implementation')
    tag = sys.implementation.cache_tag
    if tag is None:
        raise NotImplementedError('sys.implementation.cache_tag is None')
    filename = ''.join([base_filename, sep, tag, suffixes[0]])
    return os.path.join(head, _PYCACHE, filename)


class DisassembleCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = "**disassemble** [*thing*]\n\n**disassemble** [*address-range*]\n\nDisassembles bytecode. See `help syntax range` for what can go in a list range.\n\nWithout arguments, print lines starting from where the last list left off\nsince the last entry to the debugger. We start off at the location indicated\nby the current stack.\n\nin addition you can also use:\n\n  - a '.' for the location of the current frame\n\n  - a '-' for the lines before the last list\n\n  - a '+' for the lines after the last list\n\nWith a class, method, function, pyc-file, code or string argument\ndisassemble that.\n\nExamples:\n--------\n::\n\n   disassemble    # Possibly lots of stuff disassembled\n   disassemble .  # Disassemble lines starting at current stopping point.\n   disassemble +                    # Same as above\n   disassemble os.path              # Disassemble all of os.path\n   disassemble os.path.normcase()   # Disaassemble just method os.path.normcase\n   disassemble 3                    # Disassemble starting from line 3\n   disassemble 3, 10                # Disassemble lines 3 to 10\n   disassemble *0, *10              # Disassemble offset 0-10\n   disassemble myprog.pyc           # Disassemble file myprog.pyc\n\nSee also:\n---------\n\n`help syntax arange`, `deparse`, `list`, `info pc`.\n"
    aliases = ('disasm', )
    category = 'data'
    min_args = 0
    max_args = 2
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Disassemble Python bytecode'

    def run(self, args):
        proc = self.proc
        dbg_obj = self.core.debugger
        listsize = dbg_obj.settings['listsize'] * 4
        curframe = proc.curframe
        opts = {'highlight': self.settings['highlight'],  'start_line': 1, 
         'end_line': None, 
         'start_offset': None, 
         'end_offset': None, 
         'relative_pos': False}
        do_parse = True
        if len(args) == 2:
            try:
                obj = self.proc.eval(args[1])
                opts['start_offset'] = 0
                is_offset = True
                start = 0
                last = dbg_obj.settings['listsize'] * 4
                last_is_offset = False
                if inspect.ismethod(obj) or inspect.isfunction(obj) or inspect.isgeneratorfunction(obj) or inspect.isgenerator(obj) or inspect.isframe(obj) or inspect.iscode(obj):
                    do_parse = False
            except:
                pass

        if do_parse:
            bytecode_file, start, is_offset, last, last_is_offset, obj = parse_addr_list_cmd(proc, args, listsize)
            if bytecode_file is None:
                return
        if is_offset:
            opts['start_offset'] = start
        else:
            opts['start_line'] = start
        if last_is_offset:
            opts['end_offset'] = last
        else:
            opts['end_line'] = last
        if not (obj or bytecode_file.endswith('.pyo') or bytecode_file.endswith('pyc')):
            bytecode_file = cache_from_source(bytecode_file)
            if bytecode_file and Mfile.readable(bytecode_file):
                self.msg('Reading %s ...' % bytecode_file)
                version, timestamp, magic_int, obj, is_pypy, source_size = load_module(bytecode_file)
            else:
                if not curframe:
                    self.errmsg('No frame selected.')
                    return
                try:
                    obj = self.proc.eval(args[1])
                    opts['start_line'] = -1
                except:
                    self.errmsg(("Object '%s' is not something we can" + ' disassemble.') % args[1])
                    return

        self.object, proc.list_offset = Mdis.dis(self.msg, self.msg_nocr, self.section, self.errmsg, obj, **opts)
        return False


if __name__ == '__main__':

    def doit(cmd, args):
        proc = cmd.proc
        proc.current_command = ' '.join(args)
        cmd.run(args)


    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    import inspect
    cp.curframe = inspect.currentframe()
    command = DisassembleCommand(cp)
    prefix = '--------------------' + ' disassemble '
    __file__ = './disassemble.py'
    bytecode_file = cache_from_source(__file__)
    print(bytecode_file)
    if bytecode_file:
        doit(command, ['disassemble', bytecode_file + ':22,28'])
    doit(command, ['disassemble', '3,', '10'])