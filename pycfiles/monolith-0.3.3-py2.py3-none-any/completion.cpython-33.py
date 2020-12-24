# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/monolith/build/lib/monolith/cli/completion.py
# Compiled at: 2013-11-30 15:42:16
# Size of source mod 2**32: 1139 bytes
from monolith.compat import str
from monolith.cli.base import BaseCommand
COMPLETION_TEMPLATE = '\n# %(prog_name)s bash completion start\n_%(prog_name)s_completion()\n{\n    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \\\n                   COMP_CWORD=$COMP_CWORD \\\n                   %(ENV_VAR_NAME)s=1 $1 ) )\n}\ncomplete -o default -F _%(prog_name)s_completion %(prog_name)s\n# %(prog_name)s bash completion end\n\n'

class CompletionCommand(BaseCommand):
    help = ''.join(('Prints out shell snippet that once evaluated would allow this command utility to use completion abilities.', ))
    template = COMPLETION_TEMPLATE

    def get_env_var_name(self):
        return '_'.join((self.prog_name.upper(), 'AUTO_COMPLETE'))

    def get_completion_snippet(self):
        return self.template % {'prog_name': self.prog_name,  'ENV_VAR_NAME': self.get_env_var_name()}

    def handle(self, namespace):
        self.stdout.write(str(self.get_completion_snippet()))

    def post_register(self, manager):
        manager.completion = True
        manager.completion_env_var_name = self.get_env_var_name()