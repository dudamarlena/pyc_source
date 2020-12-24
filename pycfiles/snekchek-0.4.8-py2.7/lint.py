# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/lint.py
# Compiled at: 2020-03-03 07:34:32
"""
This file contains linters.

Linters included:

- flake8
- flake8-bugbear (ext)
- flake8-import-order (ext)
- flake8-mypy (ext)
- flake8-docstrings (ext)
- flake8-todo (ext)
- flake8-requirements (ext)
- flake8-string-format (ext)
- flake8-tidy-import (ext)
- flake8-bandit (ext, bandit)
- pylint
- vulture
- pyroma
"""
from __future__ import print_function, with_statement, unicode_literals
import io, json, os, re, sys, typing
from snekchek.structure import Linter
from snekchek.utils import redirect_stderr, redirect_stdout

def get_linters():
    return (
     Vulture, Pylint, Pyroma, Flake8)


class Flake8(Linter):
    requires_install = [
     b'flake8']
    patt = re.compile(b'(?P<path>[^:]+):(?P<line>[0-9]+):(?P<col>[0-9]+): (?P<errcode>[A-Z][0-9]+) (?P<msg>.+)$\\n', re.M)

    def run(self, files):
        from logging import StreamHandler
        old_emit, StreamHandler.emit = StreamHandler.emit, lambda *_: None
        import flake8.main.cli
        try:
            sett = [
             b'--config=' + self.confpath, b'--output-file=.flake8_output']
            sett.extend(files)
            flake8.main.cli.main(sett)
        except SystemExit:
            pass

        StreamHandler.emit = old_emit
        with open(b'.flake8_output') as (file):
            matches = list(self.patt.finditer(file.read()))
            self.status_code = 1 if matches else 0
            self.hook(list(sorted([ x.groupdict() for x in matches ], key=lambda x: x[b'line'])))
        if os.path.exists(b'.flake8_output'):
            os.remove(b'.flake8_output')


class Vulture(Linter):
    requires_install = [
     b'vulture']
    base_pyversion = (3, 0, 0)
    patt = re.compile(b"^(?P<path>[^:]+):(?P<line>[0-9]+): (?P<err>unused (class|attribute|function) '[a-zA-Z0-9]+') \\((?P<conf>[0-9]+)% confidence\\)$")

    def run(self, files):
        import vulture.core
        vult = vulture.core.Vulture(self.conf.as_bool(b'verbose'))
        vult.scavenge(files, [ x.strip() for x in self.conf.as_list(b'exclude') ])
        if sys.version_info >= (3, 0, 0):
            file = io.StringIO()
        else:
            file = io.BytesIO()
        with redirect_stdout(file):
            vult.report(self.conf.as_int(b'min-confidence'), self.conf.as_bool(b'sort-by-size'))
        file.seek(0)
        matches = list(self.patt.finditer(file.read()))
        self.status_code = 1 if matches else 0
        self.hook(list(sorted([ x.groupdict() for x in matches ], key=lambda x: x[b'line'])))


class Pylint(Linter):
    requires_install = [
     b'pylint']

    def run(self, files):
        args = [
         b'-f', b'json'] + files
        if sys.version_info >= (3, 0, 0):
            file = io.StringIO()
        else:
            file = io.BytesIO()
        with redirect_stdout(sys.stderr):
            with redirect_stderr(file):
                import pylint.lint
                if sys.version_info < (3, 0, 0):
                    from pylint.reporters.json import JSONReporter
                    JSONReporter.__init__.__func__.__defaults__ = (
                     file,)
                else:
                    from pylint.reporters.json_reporter import JSONReporter
                    JSONReporter.__init__.__defaults__ = (
                     file,)
                if sys.version_info >= (3, 0, 0):
                    pylint.lint.Run(args, do_exit=False)
                else:
                    pylint.lint.Run(args, exit=False)
        file.seek(0)
        text = file.read()
        if text.startswith(b'Using config file'):
            text = (b'\n').join(text.split(b'\n')[1:])
        data = json.loads(text) if text.strip() else []
        self.status_code = bool(data)
        self.hook(data)


class Pyroma(Linter):
    requires_install = [
     b'pyroma']

    def run(self, _):
        if sys.version_info >= (3, 0, 0):
            t = io.StringIO
        else:
            t = io.BytesIO
        file = t()
        with redirect_stdout(file):
            with redirect_stderr(file):
                import pyroma
                pyroma.run(b'directory', b'.')
        file.seek(0)
        text = file.read()
        lines = text.split(b'\n')
        lines.pop(0)
        if sys.version_info >= (3, 0, 0):
            lines.pop(0)
        data = {b'modules': {}}
        module = lines.pop(0)[6:].strip()
        data[b'modules'][module] = []
        lines.pop(0)
        if len(lines) >= 6:
            line = lines.pop(0)
            while line != b'-' * 30:
                data[b'modules'][module].append(line)
                line = lines.pop(0)

        rating = lines.pop(0)
        data[b'rating'] = int(rating[14:-3])
        data[b'rating_word'] = lines.pop(0)
        self.status_code = 0 if data[b'rating'] == 10 else 1
        if data[b'rating'] == 10:
            data = []
        self.hook(data)