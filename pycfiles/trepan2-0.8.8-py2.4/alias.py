# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/alias.py
# Compiled at: 2015-04-24 06:27:43
from trepan.processor.command import base_cmd as Mbase_cmd

class AliasCommand(Mbase_cmd.DebuggerCommand):
    """**alias** *alias-name* *debugger-command*

Add alias *alias-name* for a debugger command *debugger-command*.  You
might do this if you want shorter command names or more commands that
have more familiar meanings.

Another related use is as a command abbreviation for a command that
would otherwise be ambiguous. For example, by default we make `s` be
an alias of `step` to force it to be used. Without the alias, `s`
might be `step`, `show`, or `set` among others.

Examples:
--------

    alias cat list   # "cat prog.py" is the same as "list prog.py"
    alias s   step   # "s" is now an alias for "step".
                     # The above example is done by default.

See also:
---------

`unalias` and `show alias`.
    """
    __module__ = __name__
    category = 'support'
    min_args = 0
    max_args = 2
    name = 'alias'
    need_stack = True
    short_help = 'Add an alias for a debugger command'

    def run(self, args):
        if len(args) == 1:
            self.proc.commands['show'].run(['show', 'alias'])
        elif len(args) == 2:
            self.proc.commands['show'].run(['show', 'alias', args[1]])
        else:
            (junk, al, command) = args
            if command in self.proc.commands:
                if al in self.proc.aliases:
                    old_command = self.proc.aliases[al]
                    self.msg(("Alias '%s#' for command '%s'replaced old " + "alias for '%s'.") % (al, command, old_command))
                else:
                    self.msg("New alias '%s' for command '%s' created." % (al, command))
                self.proc.aliases[al] = command
            else:
                self.errmsg(("You must alias to a command name, and '%s' " + 'and is not one.') % command)
            return


if __name__ == '__main__':
    from trepan.processor.command import mock
    (d, cp) = mock.dbg_setup()
    command = AliasCommand(cp)
    command.run(['alias', 'yy', 'foo'])
    command.run(['alias', 'yy', ' foo'])
    command.run(['alias', 'yystep'])
    command.run(['alias'])
    command.run(['alias', 'yynext'])