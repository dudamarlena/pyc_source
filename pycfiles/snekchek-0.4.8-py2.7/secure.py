# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/secure.py
# Compiled at: 2020-03-03 07:34:32
"""
Checkers for security issues in the project.

Checkers included:
- Safety
- Dodgy
(bandit is supported in flake8-bandit)
"""
from __future__ import with_statement, unicode_literals
import io, json, os, sys, typing
from snekchek.structure import Linter
from snekchek.utils import redirect_stdout

def get_security():
    return (
     Safety, Dodgy)


class Safety(Linter):
    requires_install = [
     b'safety']

    def run(self, _):
        import safety.cli
        if b'requirements.txt' not in os.listdir(b'.'):
            self.hook([])
            return
        else:
            if sys.version_info >= (3, 0, 0):
                outfile = io.StringIO()
            else:
                outfile = io.BytesIO()
            try:
                with redirect_stdout(outfile):
                    safety.cli.check.callback(self.conf.get(b'pyup_key', b''), self.conf.get(b'db_path', b''), True, False, False, False, False, b'requirements.txt', self.conf.as_list(b'ignore'), b'', b'http', None, 80)
            except SystemExit:
                pass

            outfile.seek(0)
            json_data = json.load(outfile)
            self.status_code = 1 if json_data else 0
            self.hook(json_data)
            return


class Dodgy(Linter):
    requires_install = [
     b'dodgy']

    def run(self, _):
        import dodgy.run
        data = dodgy.run.run_checks(b'.', self.conf.as_list(b'ignore_paths'))
        self.status_code = 1 if data else 0
        self.hook(data)