# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\nosetp\commmands.py
# Compiled at: 2014-05-20 09:25:46
try:
    from setuptools import Commands
except ImportError:
    pass
else:
    import sys

    class nosetp(Command):
        description = 'Run nosetests, with extended options.'
        user_options = tuple()

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            orig_exit = sys.exit
            exit_code = None

            def exit(code=None):
                exit_code = code
                if exit_code:
                    orig_exit(code)

            sys.exit = exit
            self.run_command('nosetests')
            sys.exit = orig_exit
            return