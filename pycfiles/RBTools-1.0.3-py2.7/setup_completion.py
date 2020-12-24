# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/setup_completion.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
import logging, os, platform, sys
from pkg_resources import resource_string
from rbtools.commands import Command

class SetupCompletion(Command):
    """Setup auto-completion for rbt.

    By default, the command installs an auto-completion file for the user's
    login shell. The user can optionally specify a shell for which the command
    will install the auto-completion file for.
    """
    name = b'setup-completion'
    author = b'The Review Board Project'
    description = b'Setup auto-completion for bash or zsh.'
    args = b'<shell>'
    SHELLS = {b'bash': {b'Linux': {b'src': b'commands/conf/rbt-bash-completion', 
                            b'dest': b'/etc/bash_completion.d', 
                            b'filename': b'rbt'}, 
                 b'Darwin': {b'src': b'commands/conf/rbt-bash-completion', 
                             b'dest': b'/usr/local/etc/bash_completion.d', 
                             b'filename': b'rbt'}}, 
       b'zsh': {b'Linux': {b'src': b'commands/conf/_rbt-zsh-completion', 
                           b'dest': b'/usr/share/zsh/functions/Completion', 
                           b'filename': b'_rbt'}, 
                b'Darwin': {b'src': b'commands/conf/_rbt-zsh-completion', 
                            b'dest': b'/usr/share/zsh/site-functions', 
                            b'filename': b'_rbt'}}}

    def setup(self, shell):
        """Install auto-completions for the appropriate shell.

        Args:
            shell (str):
                String specifying name of shell for which auto-completions
                will be installed for.
        """
        system = platform.system()
        script = resource_string(b'rbtools', self.SHELLS[shell][system][b'src'])
        dest = os.path.join(self.SHELLS[shell][system][b'dest'], self.SHELLS[shell][system][b'filename'])
        try:
            with open(dest, b'w') as (f):
                f.write(script)
        except IOError as e:
            logging.error(b'I/O Error (%s): %s', e.errno, e.strerror)
            sys.exit()

        print(b'Successfully installed %s auto-completions.' % shell)
        print(b'Restart the terminal for completions to work.')

    def main(self, shell=None):
        """Run the command.

        Args:
            shell (str):
                An optional string specifying name of shell for which
                auto-completions will be installed for.
        """
        if not shell:
            shell = os.environ.get(b'SHELL')
            if shell:
                shell = os.path.basename(shell)
            else:
                logging.error(b'No login shell found. Re-run the command with a shell as an argument or refer to manual installation in documentation')
                sys.exit()
        if shell in self.SHELLS:
            system = platform.system()
            if system in self.SHELLS[shell]:
                if os.path.exists(self.SHELLS[shell][system][b'dest']):
                    self.setup(shell)
                else:
                    logging.error(b'Could not locate %s completion directory. Refer to manual installation in documentation', shell)
            else:
                logging.error(b'The %s operating system is currently unsupported', system)
        else:
            logging.error(b'The shell "%s" is currently unsupported', shell)