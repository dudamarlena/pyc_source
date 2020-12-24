# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/macro.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 4054 bytes
import os, sys, types
from trepan.processor.command import base_cmd as Mbase_cmd

class MacroCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = "**macro** *macro-name* *lambda-object*\n\nDefine *macro-name* as a debugger macro. Debugger macros get a list of\narguments which you supply without parenthesis or commas. See below\nfor an example.\n\nThe macro (really a Python lambda) should return either a String or an\nList of Strings. The string in both cases is a debugger command.  Each\nstring gets tokenized by a simple split() .  Note that macro\nprocessing is done right after splitting on `;;`. As a result, if the\nmacro returns a string containing `;;` this will not be interpreted as\nseparating debugger commands.\n\nIf a list of strings is returned, then the first string is\nshifted from the list and executed. The remaining strings are pushed\nonto the command queue. In contrast to the first string, subsequent\nstrings can contain other macros. `;;` in those strings will be\nsplit into separate commands.\n\nHere is an trivial example. The below creates a macro called `l=` which is\nthe same thing as `list`:\n\n    macro l= lambda: 'list .'\n\nA simple text to text substitution of one command was all that was\nneeded here. But usually you will want to run several commands. So those\nhave to be wrapped up into a list.\n\nThe below creates a macro called `fin+` which issues two commands\n`finish` followed by `step`:\n\n    macro fin+ lambda: ['finish','step']\n\nIf you wanted to parameterize the argument of the `finish` command\nyou could do that this way:\n\n    macro fin+ lambda levels: ['finish %s' % levels ,'step']\n\nInvoking with:\n\n     fin+ 3\n\nwould expand to: `['finish 3', 'step']`\n\nIf you were to add another parameter for `step`, the note that the\ninvocation might be:\n\n     fin+ 3 2\n\nrather than `fin+(3,2)` or `fin+ 3, 2`.\n\nSee also:\n---------\n\n `alias` and `info macro`.\n  "
    category = 'support'
    min_args = 2
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Define a macro'

    def run(self, args):
        cmd_name = args[1]
        cmd_argstr = self.proc.cmd_argstr[len(cmd_name):].lstrip()
        proc_obj = None
        try:
            proc_obj = eval(cmd_argstr)
        except (SyntaxError, NameError, ValueError):
            self.errmsg('Expecting a Python lambda expression; got %s' % cmd_argstr)

        if proc_obj:
            if isinstance(proc_obj, types.FunctionType):
                self.proc.macros[cmd_name] = [
                 proc_obj, cmd_argstr]
                self.msg('Macro "%s" defined.' % cmd_name)
            else:
                self.errmsg('Expecting a Python lambda expression; got: %s' % cmd_argstr)
        return


if __name__ == '__main__':
    from trepan.processor.command import mock as Mmock
    dbgr, cmd = Mmock.dbg_setup()
    command = MacroCommand(cmd)
    for cmdline in ['macro foo lambda a,y: x+y',
     'macro bad2 1+2']:
        args = cmdline.split()
        cmd_argstr = cmdline[len(args[0]):].lstrip()
        cmd.cmd_argstr = cmd_argstr
        command.run(args)

    print(cmd.macros)