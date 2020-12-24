# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/shell.py
# Compiled at: 2018-07-11 18:15:30
import os
from django.core.management.base import NoArgsCommand
from optparse import make_option

class Command(NoArgsCommand):
    shells = [
     'ipython', 'bpython']
    option_list = NoArgsCommand.option_list + (
     make_option('--plain', action='store_true', dest='plain', help='Tells Django to use plain Python, not IPython or bpython.'),
     make_option('-i', '--interface', action='store', type='choice', choices=shells, dest='interface', help='Specify an interactive interpreter interface. Available options: "ipython" and "bpython"'))
    help = 'Runs a Python interactive interpreter. Tries to use IPython or bpython, if one of them is available.'
    requires_model_validation = False

    def ipython(self):
        try:
            from IPython import embed
            embed()
        except ImportError:
            try:
                from IPython.Shell import IPShell
                shell = IPShell(argv=[])
                shell.mainloop()
            except ImportError:
                raise

    def bpython(self):
        import bpython
        bpython.embed()

    def run_shell(self, shell=None):
        available_shells = [shell] if shell else self.shells
        for shell in available_shells:
            try:
                return getattr(self, shell)()
            except ImportError:
                pass

        raise ImportError

    def handle_noargs(self, **options):
        from django.db.models.loading import get_models
        get_models()
        use_plain = options.get('plain', False)
        interface = options.get('interface', None)
        try:
            if use_plain:
                raise ImportError
            self.run_shell(shell=interface)
        except ImportError:
            import code
            imported_objects = {}
            try:
                import readline
            except ImportError:
                pass
            else:
                import rlcompleter
                readline.set_completer(rlcompleter.Completer(imported_objects).complete)
                readline.parse_and_bind('tab:complete')

            if not use_plain:
                for pythonrc in (os.environ.get('PYTHONSTARTUP'), os.path.expanduser('~/.pythonrc.py')):
                    if pythonrc and os.path.isfile(pythonrc):
                        try:
                            with open(pythonrc) as (handle):
                                exec compile(handle.read(), pythonrc, 'exec')
                        except NameError:
                            pass

            code.interact(local=imported_objects)

        return