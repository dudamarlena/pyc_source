# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/macro.py
# Compiled at: 2015-02-16 15:47:50
import os, sys, types
from trepan.processor.command import base_cmd as Mbase_cmd

class MacroCommand(Mbase_cmd.DebuggerCommand):
    """**macro** *macro-name* *lambda-object*

Define *macro-name* as a debugger macro. Debugger macros get a list of
arguments which you supply without parenthesis or commas. See below
for an example.

The macro (really a Python lambda) should return either a String or an
List of Strings. The string in both cases is a debugger command.  Each
string gets tokenized by a simple split() .  Note that macro
processing is done right after splitting on `;;`. As a result, if the
macro returns a string containing `;;` this will not be interpreted as
separating debugger commands.

If a list of strings is returned, then the first string is
shifted from the list and executed. The remaining strings are pushed
onto the command queue. In contrast to the first string, subsequent
strings can contain other macros. `;;` in those strings will be
split into separate commands.

Here is an trivial example. The below creates a macro called `l=` which is
the same thing as `list`:

    macro l= lambda: 'list .'

A simple text to text substitution of one command was all that was
needed here. But usually you will want to run several commands. So those
have to be wrapped up into a list.

The below creates a macro called `fin+` which issues two commands
`finish` followed by `step`:

    macro fin+ lambda: ['finish','step']

If you wanted to parameterize the argument of the `finish` command
you could do that this way:

    macro fin+ lambda levels: ['finish %s' % levels ,'step']

Invoking with:

     fin+ 3

would expand to: `['finish 3', 'step']`

If you were to add another parameter for `step`, the note that the
invocation might be:

     fin+ 3 2

rather than `fin+(3,2)` or `fin+ 3, 2`.

See also:
---------

 `alias` and `info macro`.
  """
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
    (dbgr, cmd) = Mmock.dbg_setup()
    command = MacroCommand(cmd)
    for cmdline in ['macro foo lambda a,y: x+y',
     'macro bad2 1+2']:
        args = cmdline.split()
        cmd_argstr = cmdline[len(args[0]):].lstrip()
        cmd.cmd_argstr = cmd_argstr
        command.run(args)

    print cmd.macros