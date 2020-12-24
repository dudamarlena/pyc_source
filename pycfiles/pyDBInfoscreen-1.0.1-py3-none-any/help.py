# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/help.py
# Compiled at: 2013-03-17 12:07:41
import os, re
from import_relative import import_relative
import_relative('processor', '....pydbgr')
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdproc = import_relative('cmdproc', '..', 'pydbgr')
Mmisc = import_relative('misc', '...', 'pydbgr')
categories = {'breakpoints': 'Making the program stop at certain points', 'data': 'Examining data', 'files': 'Specifying and examining files', 'running': 'Running the program', 'status': 'Status inquiries', 'support': 'Support facilities', 'stack': 'Examining the call stack'}

class HelpCommand(Mbase_cmd.DebuggerCommand):
    """**help** [*command* [*subcommand*]|*expression*]
        
Without argument, print the list of available debugger commands.

When an argument is given, it is first checked to see if it is command
name.

If the argument is an expression or object name, you get the same
help that you would get inside a Python shell running the built-in
*help()* command.

If the environment variable *$PAGER* is defined, the file is
piped through that command.  You'll notice this only for long help
output.

Some commands like `info`, `set`, and `show` can accept an
additional subcommand to give help just about that particular
subcommand. For example `help info line` give help about the
info line command.

See also `examine` and `whatis`.
"""
    __module__ = __name__
    aliases = ('?', )
    category = 'support'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Print commands or give help for command(s)'

    def run(self, args):
        self.proc.last_command = ''
        if len(args) > 1:
            cmd_name = args[1]
            if cmd_name == '*':
                self.section('List of all debugger commands:')
                self.msg_nocr(self.columnize_commands(list(self.proc.commands.keys())))
                return
            elif cmd_name in list(categories.keys()):
                self.show_category(cmd_name, args[2:])
                return
            command_name = Mcmdproc.resolve_name(self.proc, cmd_name)
            if command_name:
                instance = self.proc.commands[command_name]
                if hasattr(instance, 'help'):
                    return instance.help(args)
                else:
                    doc = instance.__doc__ or instance.run.__doc__
                    doc = doc.rstrip('\n')
                    self.rst_msg(doc.rstrip('\n'))
                    aliases = [ key for key in self.proc.aliases if command_name == self.proc.aliases[key] ]
                    if len(aliases) > 0:
                        self.msg('')
                        msg = Mmisc.wrapped_lines('Aliases:', (', ').join(aliases) + '.', self.settings['width'])
                        self.msg(msg)
            else:
                cmds = [ cmd for cmd in list(self.proc.commands.keys()) if re.match('^' + cmd_name, cmd) ]
                if cmds is None:
                    self.errmsg('No commands found matching /^%s/. Try "help".' % cmd_name)
                else:
                    self.section('Command names matching /^%s/:' % cmd_name)
                    self.msg_nocr(self.columnize_commands(cmds))
            return
        else:
            self.list_categories()
        return False

    def list_categories(self):
        """List the command categories and a short description of each."""
        self.section('Classes of commands:')
        cats = list(categories.keys())
        cats.sort()
        for cat in cats:
            self.msg('  %-13s -- %s' % (cat, categories[cat]))

        final_msg = '\nType `help` followed by a class name for a list of commands in that class.\nType `help *` for the list of all commands.\nType `help` *regexp* for the list of commands matching /^#{*regexp*}/\nType `help` *category* `*` for the list of all commands in category *category*\nType `help` followed by command name for full documentation.\n'
        for line in re.compile('\n').split(final_msg.rstrip('\n')):
            self.rst_msg(line)

    def show_category(self, category, args):
        """Show short help for all commands in `category'."""
        n2cmd = self.proc.commands
        names = list(n2cmd.keys())
        if len(args) == 1 and args[0] == '*':
            self.section('Commands in class %s:' % category)
            cmds = [ cmd for cmd in names if category == n2cmd[cmd].category ]
            cmds.sort()
            self.msg_nocr(self.columnize_commands(cmds))
            return
        self.msg('%s.\n' % categories[category])
        self.section('List of commands:')
        names.sort()
        for name in names:
            if category != n2cmd[name].category:
                continue
            self.msg('%-13s -- %s' % (name, n2cmd[name].short_help))


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = HelpCommand(cp)
    print '-' * 20
    command.run(['help'])
    print '-' * 20
    command.run(['help', '*'])
    print '-' * 20
    command.run(['help', 'quit'])
    print '-' * 20
    command.run(['help', 'stack'])
    print '-' * 20
    command.run(['help', 'breakpoints'])
    print '-' * 20
    command.run(['help', 'breakpoints', '*'])
    print '-' * 20
    command.run(['help', 'c.*'])