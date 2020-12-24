# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/style.py
# Compiled at: 2020-03-03 07:34:32
"""
This file contains Style checkers.

Stylers included:
- isort
- yapf
- black
note that black is not compatible with pylint
"""
from __future__ import with_statement, unicode_literals
import io, sys, typing
from snekchek.structure import Linter
from snekchek.utils import redirect_stderr, redirect_stdout

def get_stylers():
    return (
     ISort, Yapf, Black)


class ISort(Linter):
    requires_install = [
     b'isort']

    def run(self, files):
        import isort
        self.conf[b'line_length'] = self.conf.as_int(b'line_length')
        self.conf[b'sections'] = self.conf.as_list(b'sections')
        self.conf[b'multi_line_output'] = self.conf.as_int(b'multi_line_output')
        res = []
        for filename in files:
            with redirect_stdout(io.StringIO()):
                sort = isort.SortImports(filename, **self.conf)
            if sort.skipped:
                continue
            self.status_code = self.status_code or (1 if sort.incorrectly_sorted else 0)
            if self.conf.as_bool(b'inplace'):
                with io.open(filename, b'w', encoding=b'utf-8') as (file):
                    file.write(sort.output)
            else:
                with io.open(filename, encoding=b'utf-8') as (file):
                    out = io.StringIO()
                    with redirect_stdout(out):
                        sort._show_diff(file.read())
                    out.seek(0)
                    diff = out.read()
                if diff.strip():
                    res.append(diff.strip())

        self.hook(res)


class Yapf(Linter):
    requires_install = [
     b'yapf']
    base_pyversion = (3, 4, 0)

    def run(self, files):
        import yapf.yapflib.yapf_api
        res = []
        for file in files:
            code, _, changed = yapf.yapflib.yapf_api.FormatFile(file, style_config=self.confpath)
            self.status_code = self.status_code or (1 if changed else 0)
            if changed:
                if self.conf.as_bool(b'inplace'):
                    with io.open(file, b'w', encoding=b'utf-8') as (new_file):
                        new_file.write(code)
                else:
                    res.append(code.strip())

        self.hook(res)


class Black(Linter):
    requires_install = [
     b'black']
    base_pyversion = (3, 6, 0)

    def run(self, files):
        from black import main, TargetVersion
        conf = self.conf
        file = io.StringIO()
        with redirect_stderr(file):
            try:
                main.callback.__closure__[0].cell_contents(sys, None, conf.as_int(b'line_length'), list(map(lambda x: getattr(TargetVersion, x), conf.as_list(b'versions'))), False, False, False, False, False, True, conf.as_bool(b'quiet'), False, b'', conf[b'exclude'], tuple(files), self.confpath)
            except SystemExit:
                pass

        file.seek(0)
        self.status_code = b'reformatted' in file.read()
        self.hook([])
        return