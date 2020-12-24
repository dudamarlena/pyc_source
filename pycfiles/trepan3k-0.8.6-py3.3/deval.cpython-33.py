# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/deval.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2956 bytes
import os
from sys import version_info
from trepan.processor.command import base_cmd as Mbase_cmd
from uncompyle6.semantics.fragments import deparse_code
from xdis import IS_PYPY
from trepan.processor.command.deparse import deparsed_find

class DEvalCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**deval**\n    **deval?**\n\nRun a the current deparsed expression in the context of the current\nframe. Normally we are stopped before an expression so the thing that\ncorresponds to the `eval` command is running the parent\nconstruct. `deval?` will run just the command associated with the next\npiece of code to be run.\n\nExamples:\n---------\n\n    deval   # Run *parent* of current deparsed code\n    deval?  # Run current deparsed code\n\nSee also:\n---------\n\n`eval`\n\n    '
    category = 'data'
    aliases = ('deval?', )
    min_args = 0
    max_args = 0
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print value of deparsed expression'

    def run(self, args):
        co = self.proc.curframe.f_code
        name = co.co_name
        last_i = self.proc.curframe.f_lasti
        if last_i == -1:
            last_i = 0
        sys_version = version_info[0] + version_info[1] / 10.0
        try:
            deparsed = deparse_code(sys_version, co, is_pypy=IS_PYPY)
            nodeInfo = deparsed_find((name, last_i), deparsed, co)
            if not nodeInfo:
                self.errmsg("Can't find exact offset %d" % last_i)
                return
        except:
            self.errmsg('error in deparsing code')
            return

        if '?' == args[0][(-1)]:
            extractInfo = deparsed.extract_node_info(nodeInfo.node)
        else:
            extractInfo, _ = deparsed.extract_parent_info(nodeInfo.node)
        text = extractInfo.selectedText
        text = text.strip()
        self.msg('Evaluating: %s' % text)
        try:
            self.proc.exec_line(text)
        except:
            pass


if __name__ == '__main__':
    import inspect
    from trepan import debugger
    d = debugger.Debugger()
    cp = d.core.processor
    cp.curframe = inspect.currentframe()
    command = DEvalCommand(cp)
    me = 10