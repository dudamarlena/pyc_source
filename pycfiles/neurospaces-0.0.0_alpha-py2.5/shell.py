# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/neurospaces/shell.py
# Compiled at: 2011-09-06 12:02:45
"""!

An interactive shell for use with the developer python package.

"""
import cmd, os, pdb, re, shlex, sys

class PackageShell(cmd.Cmd):
    """!

    
    """

    def __init__(self, package_manager=None, intro='Welcome to the Neurospaces Developer shell. Type help or ? to list commands.\n', prompt='ns-pkgmgr> ', verbose=True):
        """

        @param developer The developer object to wrap around
        @param intro The intro text to use when starting the shell
        @param prompt The text for the command line prompt.
        """
        cmd.Cmd.__init__(self)
        try:
            import readline
        except ImportError:
            print 'The readline module for python is not installed, autocompletion will not work.'

        self.verbose = verbose
        self.intro = intro
        self.prompt = prompt
        self.histfile = None
        self.package_manager = package_manager
        self._package_names = self.package_manager.get_package_names()
        return

    def _get_completions(self, token, text='', items=[]):
        if token == '':
            return []
        offs = len(token) - len(text)
        completions = [ f[offs:] for f in items if f.startswith(token)
                      ]
        return completions

    def do_EOF(self, arg):
        return True

    def help_EOF(self, arg):
        print 'Terminates the shell'

    def help_help(self):
        self.do_help()

    def do_hello(self, arg):
        print 'hello again', arg, '!'

    def help_hello(self):
        print 'usage: hello [message]',
        print '-- prints a hello message'

    def complete_hello(self, text, line, start_index, end_index):
        tokens = line.split()
        if len(tokens) == 1:
            completions = ['option_1', 'option_2', 'option_3']
        elif len(tokens) == 2:
            completions = self._get_completions(tokens[1], text, [])
        else:
            return []
        return completions

    def do_list_packages(self, arg):
        verbose = False
        if arg == 'verbose' or arg == 'v':
            verbose = True
        package_list = self.package_manager.get_installed_packages()
        print ''
        for p in package_list:
            if verbose:
                print 'Name: %s' % p['info'].GetName()
                print 'Version: %s' % p['info'].GetVersion()
                print 'Revision: %s' % p['info'].GetRevisionInfo()
                print 'Install Location: %s' % p['installed']
                print ''
            else:
                print '%s' % p['info'].GetName()

        print ''

    def help_list_packages(self):
        print 'usage: list_packages [v, verbose]',
        print '-- '

    def complete_list_packages(self, text, line, start_index, end_index):
        tokens = line.split()
        if len(tokens) == 1:
            completions = ['v', 'verbose']
        else:
            return []
        return completions

    def do_uninstall(self, arg):
        if arg == '' or arg is None:
            print 'No package given to uninstall'
        package = arg
        try:
            self.package_manager.uninstall(arg)
        except Exception, e:
            print e

        return

    def help_uninstall(self):
        print 'usage: uninstall [package_name]',
        print '-- uninstalls a python package'

    def complete_uninstall(self, text, line, start_index, end_index):
        tokens = line.split()
        if len(tokens) == 1:
            completions = self._package_names
        elif len(tokens) == 2:
            completions = self._get_completions(tokens[1], text, self._package_names)
        else:
            return []
        return completions

    def do_clear(self, arg):
        if arg != '':
            self.help_clear()
        os.system('clear')

    def help_clear(self):
        print 'usage: clear',
        print '-- clears the screen'

    do_continue = do_EOF

    def help_continue(self):
        print 'usage: continue',
        print '-- exits the shell and continues the developer'

    do_c = do_continue

    def help_c(self):
        print 'usage: c',
        print '-- exits the shell and continues the developer'

    def do_pwd(self, arg):
        if arg:
            self.help_pwd()
        print os.getcwd()

    def help_pwd(self):
        print 'usage: pwd',
        print '-- print the current directory'

    def do_cd(self, arg):
        try:
            os.chdir(arg)
        except Exception, e:
            print e
            return

    def help_cd(self):
        print 'usage: cd [directory]',
        print '-- Change the current working directory'

    def do_version(self, arg):
        version = self.package_manager.get_version()
        print '%s' % version

    def help_version(self):
        print 'usage: version',
        print '-- prints the version'

    def do_quit(self, arg):
        self.package_manager = None
        sys.exit(1)
        return

    def help_quit(self):
        print 'usage: quit',
        print '-- terminates the shell and sspy'

    def do_shell(self, arg):
        """Run a shell command"""
        print 'running shell command:', arg
        output = os.popen(arg).read()
        print output

    def help_shell(self):
        print 'usage: shell [command]',
        print '-- Executes a shell command'

    do_q = do_quit
    help_q = help_quit