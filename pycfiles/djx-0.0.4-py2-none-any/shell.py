# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/shell.py
# Compiled at: 2019-02-14 00:35:17
import os, select, sys, warnings
from django.core.management import BaseCommand, CommandError
from django.utils.datastructures import OrderedSet
from django.utils.deprecation import RemovedInDjango20Warning

class Command(BaseCommand):
    help = 'Runs a Python interactive interpreter. Tries to use IPython or bpython, if one of them is available. Any standard input is executed as code.'
    requires_system_checks = False
    shells = ['ipython', 'bpython', 'python']

    def add_arguments(self, parser):
        parser.add_argument('--plain', action='store_true', dest='plain', help='Tells Django to use plain Python, not IPython or bpython. Deprecated, use the `-i python` or `--interface python` option instead.')
        parser.add_argument('--no-startup', action='store_true', dest='no_startup', help='When using plain Python, ignore the PYTHONSTARTUP environment variable and ~/.pythonrc.py script.')
        parser.add_argument('-i', '--interface', choices=self.shells, dest='interface', help='Specify an interactive interpreter interface. Available options: "ipython", "bpython", and "python"')
        parser.add_argument('-c', '--command', dest='command', help='Instead of opening an interactive shell, run a command as Django and exit.')

    def ipython(self, options):
        from IPython import start_ipython
        start_ipython(argv=[])

    def bpython(self, options):
        import bpython
        bpython.embed()

    def python(self, options):
        import code
        imported_objects = {}
        try:
            import readline
        except ImportError:
            pass

        import rlcompleter
        readline.set_completer(rlcompleter.Completer(imported_objects).complete)
        readline_doc = getattr(readline, '__doc__', '')
        if readline_doc is not None and 'libedit' in readline_doc:
            readline.parse_and_bind('bind ^I rl_complete')
        else:
            readline.parse_and_bind('tab:complete')
        if not options['no_startup']:
            for pythonrc in OrderedSet([os.environ.get('PYTHONSTARTUP'), os.path.expanduser('~/.pythonrc.py')]):
                if not pythonrc:
                    continue
                if not os.path.isfile(pythonrc):
                    continue
                try:
                    with open(pythonrc) as (handle):
                        exec compile(handle.read(), pythonrc, 'exec') in imported_objects
                except NameError:
                    pass

        code.interact(local=imported_objects)
        return

    def handle(self, **options):
        if options['plain']:
            warnings.warn('The --plain option is deprecated in favor of the -i python or --interface python option.', RemovedInDjango20Warning)
            options['interface'] = 'python'
        if options['command']:
            exec options['command']
            return
        if sys.platform != 'win32' and select.select([sys.stdin], [], [], 0)[0]:
            exec sys.stdin.read()
            return
        available_shells = [options['interface']] if options['interface'] else self.shells
        for shell in available_shells:
            try:
                return getattr(self, shell)(options)
            except ImportError:
                pass

        raise CommandError(("Couldn't import {} interface.").format(shell))