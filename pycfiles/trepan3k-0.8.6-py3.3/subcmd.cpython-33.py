# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/subcmd.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 5614 bytes
"""Handles gdb-like subcommand processing."""

class Subcmd:
    __doc__ = 'Gdb-like subcommand handling '

    def __init__(self, name, cmd_obj):
        self.name = name
        self.cmd_obj = cmd_obj
        self.subcmds = {}
        self.cmdlist = []

    def lookup(self, subcmd_prefix):
        """Find subcmd in self.subcmds"""
        for subcmd_name in list(self.subcmds.keys()):
            if subcmd_name.startswith(subcmd_prefix) and len(subcmd_prefix) >= self.subcmds[subcmd_name].__class__.min_abbrev:
                return self.subcmds[subcmd_name]

        return

    def short_help(self, subcmd_cb, subcmd_name, label=False):
        """Show short help for a subcommand."""
        entry = self.lookup(subcmd_name)
        if entry:
            if label:
                prefix = entry.name
            else:
                prefix = ''
            if hasattr(entry, 'short_help'):
                if prefix:
                    prefix += ' -- '
                self.cmd_obj.msg(prefix + entry.short_help)
        else:
            self.undefined_subcmd('help', subcmd_name)

    def add(self, subcmd_cb):
        """Add subcmd to the available subcommands for this object.
        It will have the supplied docstring, and subcmd_cb will be called
        when we want to run the command. min_len is the minimum length
        allowed to abbreviate the command. in_list indicates with the
        show command will be run when giving a list of all sub commands
        of this object. Some commands have long output like "show commands"
        so we might not want to show that.
        """
        subcmd_name = subcmd_cb.name
        self.subcmds[subcmd_name] = subcmd_cb
        self.cmdlist.append(subcmd_name)

    def run(self, subcmd_name, arg):
        """Run subcmd_name with args using obj for the environent"""
        entry = self.lookup(subcmd_name)
        if entry:
            entry['callback'](arg)
        else:
            self.cmdproc.undefined_cmd(entry.__class__.name, subcmd_name)

    def help(self, *args):
        """help for subcommands."""
        print(args)
        subcmd_prefix = args[0]
        if not subcmd_prefix or len(subcmd_prefix) == 0:
            self.msg(self.doc)
            self.msg('\nList of %s subcommands:\n' % self.name)
            for subcmd_name in self.list():
                self._subcmd_helper(subcmd_name, self, True, True)

            return
        entry = self.lookup(subcmd_prefix)
        if entry and hasattr(entry, 'help'):
            entry.help(args)
        else:
            self.cmd_obj.errmsg("Unknown 'help %s' subcommand %s" % (
             self.name, subcmd_prefix))

    def list(self):
        l = list(self.subcmds.keys())
        l.sort()
        return l

    def undefined_subcmd(self, cmd, subcmd):
        """Error message when a subcommand doesn't exist"""
        self.cmd_obj.errmsg('Undefined "%s" command: "%s". Try "help".' % (
         cmd, subcmd))


if __name__ == '__main__':
    from trepan.processor.command import mock as Mmock
    from trepan.processor.command import base_cmd as Mbase_cmd

    class TestCommand(Mbase_cmd.DebuggerCommand):
        __doc__ = 'Doc string for testing'
        category = 'data'
        min_args = 0
        max_args = 5
        name = 'test'

        def __init__(self):
            self.name = 'test'

        def run(self, args):
            print('test command run')


    class TestTestingSubcommand:
        __doc__ = 'Doc string for test testing subcommand'

        def __init__(self):
            self.name = 'testing'

        short_help = 'This is short help for test testing'
        min_abbrev = 4
        in_list = True

        def run(self, args):
            print('test testing run')


    d = Mmock.MockDebugger()
    testcmd = TestCommand()
    testcmd.debugger = d
    testcmd.proc = d.core.processor
    testcmdMgr = Subcmd('test', testcmd)
    testsub = TestTestingSubcommand()
    testcmdMgr.add(testsub)
    for prefix in ['tes', 'test', 'testing', 'testing1']:
        x = testcmdMgr.lookup(prefix)
        if x:
            print(x.name)
        else:
            print('None')

    testcmdMgr.short_help(testcmd, 'testing')
    testcmdMgr.short_help(testcmd, 'test', True)
    testcmdMgr.short_help(testcmd, 'tes')
    print(testcmdMgr.list())
    testsub2 = TestTestingSubcommand()
    testsub2.name = 'foobar'
    testcmdMgr.add(testsub2)
    print(testcmdMgr.list())