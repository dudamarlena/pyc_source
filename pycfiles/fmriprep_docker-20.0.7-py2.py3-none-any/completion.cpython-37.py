# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/commands/completion.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 2957 bytes
from __future__ import absolute_import
import sys, textwrap
from pip._internal.cli.base_command import Command
from pip._internal.utils.misc import get_prog
BASE_COMPLETION = '\n# pip {shell} completion start{script}# pip {shell} completion end\n'
COMPLETION_SCRIPTS = {'bash':'\n        _pip_completion()\n        {{\n            COMPREPLY=( $( COMP_WORDS="${{COMP_WORDS[*]}}" \\\n                           COMP_CWORD=$COMP_CWORD \\\n                           PIP_AUTO_COMPLETE=1 $1 2>/dev/null ) )\n        }}\n        complete -o default -F _pip_completion {prog}\n    ', 
 'zsh':'\n        function _pip_completion {{\n          local words cword\n          read -Ac words\n          read -cn cword\n          reply=( $( COMP_WORDS="$words[*]" \\\n                     COMP_CWORD=$(( cword-1 )) \\\n                     PIP_AUTO_COMPLETE=1 $words[1] 2>/dev/null ))\n        }}\n        compctl -K _pip_completion {prog}\n    ', 
 'fish':'\n        function __fish_complete_pip\n            set -lx COMP_WORDS (commandline -o) ""\n            set -lx COMP_CWORD ( \\\n                math (contains -i -- (commandline -t) $COMP_WORDS)-1 \\\n            )\n            set -lx PIP_AUTO_COMPLETE 1\n            string split \\  -- (eval $COMP_WORDS[1])\n        end\n        complete -fa "(__fish_complete_pip)" -c {prog}\n    '}

class CompletionCommand(Command):
    __doc__ = 'A helper command to be used for command completion.'
    ignore_require_venv = True

    def __init__(self, *args, **kw):
        (super(CompletionCommand, self).__init__)(*args, **kw)
        cmd_opts = self.cmd_opts
        cmd_opts.add_option('--bash',
          '-b', action='store_const',
          const='bash',
          dest='shell',
          help='Emit completion code for bash')
        cmd_opts.add_option('--zsh',
          '-z', action='store_const',
          const='zsh',
          dest='shell',
          help='Emit completion code for zsh')
        cmd_opts.add_option('--fish',
          '-f', action='store_const',
          const='fish',
          dest='shell',
          help='Emit completion code for fish')
        self.parser.insert_option_group(0, cmd_opts)

    def run(self, options, args):
        """Prints the completion code of the given shell"""
        shells = COMPLETION_SCRIPTS.keys()
        shell_options = ['--' + shell for shell in sorted(shells)]
        if options.shell in shells:
            script = textwrap.dedent(COMPLETION_SCRIPTS.get(options.shell, '').format(prog=(get_prog())))
            print(BASE_COMPLETION.format(script=script, shell=(options.shell)))
        else:
            sys.stderr.write('ERROR: You must pass {}\n'.format(' or '.join(shell_options)))