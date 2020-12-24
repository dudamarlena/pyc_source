# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/.pythonpath/vcs/commands/completion.py
# Compiled at: 2013-04-27 15:11:11
from vcs.cli import BaseCommand
from vcs.cli import COMPLETION_ENV_NAME
COMPLETION_TEMPLATE = '\n# %(prog_name)s bash completion start\n_%(prog_name)s_completion()\n{\n    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \\\n                   COMP_CWORD=$COMP_CWORD \\\n                   %(ENV_VAR_NAME)s=1 $1 ) )\n}\ncomplete -o default -F _%(prog_name)s_completion %(prog_name)s\n# %(prog_name)s bash completion end\n\n'

class CompletionCommand(BaseCommand):
    help = ('').join(('Prints out shell snippet that once evaluated would allow this command utility to use completion abilities.', ))
    template = COMPLETION_TEMPLATE

    def get_completion_snippet(self):
        return self.template % {'prog_name': 'vcs', 'ENV_VAR_NAME': COMPLETION_ENV_NAME}

    def handle(self, **options):
        self.stdout.write(self.get_completion_snippet())