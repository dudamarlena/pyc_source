# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/deparse.py
# Compiled at: 2019-03-07 16:54:44
import os
from getopt import getopt, GetoptError
from uncompyle6.semantics.fragments import code_deparse
from trepan.lib.deparse import deparse_and_cache, deparse_offset
from pyficache import highlight_string, getlines
from trepan.processor.command import base_cmd as Mbase_cmd

class DeparseCommand(Mbase_cmd.DebuggerCommand):
    """**deparse** [options] [ . ]

Options:
------

    -p | --parent        show parent node
    -A | --tree | --AST  show abstract syntax tree (AST)
    -o | --offset [num]  show deparse of offset NUM
    -h | --help          give this help

deparse around where the program is currently stopped. If no offset is given,
we use the current frame offset. If `-p` is given, include parent information.

If an '.' argument is given, deparse the entire function or main
program you are in.

Output is colorized the same as source listing. Use `set highlight plain` to turn
that off.

Examples:
--------

    deparse             # deparse current location
    deparse --parent    # deparse current location enclosing context
    deparse .           # deparse current function or main
    deparse --offset 6  # deparse starting at offset 6
    deparse --offsets   # show all exect deparsing offsets
    deparse --AST       # deparse and show AST

See also:
---------

`disassemble`, `list`, and `set highlight`
"""
    category = 'data'
    min_args = 0
    max_args = 10
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Deparse source via uncompyle6'

    def print_text(self, text):
        if self.settings['highlight'] == 'plain':
            self.msg(text)
            return
        opts = {'bg': self.settings['highlight']}
        if 'style' in self.settings:
            opts['style'] = self.settings['style']
        self.msg(highlight_string(text, opts).strip('\n'))

    def run(self, args):
        co = self.proc.curframe.f_code
        name = co.co_name
        try:
            opts, args = getopt(args[1:], 'hpPAto:O', [
             'help', 'parent', 'pretty', 'AST',
             'tree', 'offset=', 'offsets'])
        except GetoptError as err:
            print(str(err))
            return

        show_parent = False
        show_ast = False
        offset = None
        show_offsets = False
        for o, a in opts:
            if o in ('-h', '--help'):
                self.proc.commands['help'].run(['help', 'deparse'])
                return
            if o in ('-O', '--offsets'):
                show_offsets = True
            elif o in ('-p', '--parent'):
                show_parent = True
            elif o in ('-A', '--tree', '--AST'):
                show_ast = True
            elif o in ('-o', '--offset'):
                offset = a
            else:
                self.errmsg("unhandled option '%s'" % o)

        nodeInfo = None
        if len(args) >= 1 and args[0] == '.':
            temp_filename, name_for_code = deparse_and_cache(co, self.errmsg)
            return temp_filename or None
        else:
            self.print_text(''.join(getlines(temp_filename)))
            return
        if show_offsets:
            deparsed = code_deparse(co)
            self.section('Offsets known:')
            m = self.columnize_commands(list(sorted(deparsed.offsets.keys(), key=lambda x: str(x[0]))))
            self.msg_nocr(m)
            return
        else:
            if offset is not None:
                mess = "The 'deparse' command when given an argument requires an instruction offset. Got: '%s'" % offset
                last_i = self.proc.get_an_int(offset, mess)
                if last_i is None:
                    return
            else:
                last_i = self.proc.curframe.f_lasti
                if last_i == -1:
                    last_i = 0
                deparsed, nodeInfo = deparse_offset(co, name, last_i, self.errmsg)
                if not deparsed:
                    return
                if nodeInfo:
                    extractInfo = deparsed.extract_node_info(nodeInfo)
                    parentInfo = None
                    if show_ast:
                        p = deparsed.ast
                        if show_parent:
                            parentInfo, p = deparsed.extract_parent_info(nodeInfo.node)
                        self.msg(p)
                    if extractInfo:
                        self.rst_msg('*instruction:* %s' % nodeInfo.node)
                        self.print_text(extractInfo.selectedLine)
                        self.msg(extractInfo.markerLine)
                        if show_parent:
                            if not parentInfo:
                                parentInfo, p = deparsed.extract_parent_info(nodeInfo.node)
                            if parentInfo:
                                self.section('Contained in...')
                                self.rst_msg('\t*Grammar Symbol:* %s' % p.kind)
                                self.print_text(parentInfo.selectedLine)
                                self.msg(parentInfo.markerLine)
                else:
                    if last_i == -1:
                        if name:
                            self.msg('At beginning of %s ' % name)
                        else:
                            if self.core.filename(None):
                                self.msg('At beginning of program %s' % self.core.filename(None))
                            else:
                                self.msg('At beginning')
                    else:
                        self.errmsg("haven't recorded info for offset %d. Offsets I know are:" % last_i)
                        offsets = [key[1] for key in deparsed.offsets.keys() if isinstance(key[1], int)]
                        m = self.columnize_commands(list(sorted(offsets)))
                        self.msg_nocr(m)
            return