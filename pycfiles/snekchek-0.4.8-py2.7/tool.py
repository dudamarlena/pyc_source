# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/tool.py
# Compiled at: 2020-03-03 07:34:32
"""
Tools to run over code that don't lint and don't format

Currently included:
- Pytest
- Unittest
- Upload to pypi (twine)
"""
from __future__ import print_function, with_statement, unicode_literals
import glob, io, json, os, subprocess, sys, typing
from snekchek.misc import __version__
from snekchek.structure import Linter
from snekchek.utils import redirect_stderr, redirect_stdout

def get_tools():
    return (
     Pytest, UnitTest, Pypi)


class Pytest(Linter):
    requires_install = [
     b'pytest', b'pytest-json']

    def run(self, _):
        import pytest
        if sys.version_info >= (3, 0, 0):
            file = io.StringIO()
        else:
            file = io.BytesIO()
        with redirect_stdout(file):
            with redirect_stderr(file):
                exitcode = pytest.main([
                 b'--json=.log.json', b'-qqqq', b'-c', self.confpath])
        self.status_code = exitcode
        with io.open(b'.log.json', encoding=b'utf-8') as (file):
            data = json.load(file)
        os.remove(b'.log.json')
        self.hook([ test for test in data[b'report'][b'tests'] if test[b'outcome'] == b'failed'
                  ])


class UnitTest(Linter):

    def run(self, _):
        errors = []
        if sys.version_info >= (3, 0, 0):
            fileo = io.StringIO()
        else:
            fileo = io.BytesIO()
        with redirect_stdout(fileo):
            with redirect_stderr(fileo):
                from unittest import TestProgram, TextTestRunner
                paths = glob.glob(self.conf[b'testpaths'])
                if len(paths) == 1 and os.path.isdir(paths[0]):
                    paths = [ paths[0] + b'/' + path for path in os.listdir(paths[0]) if not os.path.isdir(paths[0] + b'/' + path)
                            ]
                for path in paths:
                    test_name = path.split(b'.')[0].replace(b'/', b'.')
                    try:
                        prog = TestProgram(test_name, testRunner=TextTestRunner(stream=fileo), exit=False)
                    except SystemExit:
                        pass

                    errors += prog.result.errors
                    errors += prog.result.failures

        fileo.seek(0)
        self.status_code = bool(errors)
        self.hook(errors)


class Pypi(Linter):
    requires_install = [
     b'twine', b'wheel', b'requests']

    def run(self, _):
        import requests, twine.commands.upload, twine.settings
        try:
            with redirect_stdout(io.StringIO()):
                with redirect_stderr(io.StringIO()):
                    if sys.version_info >= (3, 0, 0):
                        proc = subprocess.Popen([
                         sys.executable,
                         b'setup.py',
                         b'sdist',
                         b'bdist_wheel'], stdout=subprocess.DEVNULL)
                    else:
                        proc = subprocess.Popen([
                         sys.executable, b'setup.py', b'-q', b'sdist',
                         b'bdist_wheel'])
                    proc.wait()
                    twine.commands.upload.upload(twine.settings.Settings(sign=self.conf.as_bool(b'sign'), repository=self.conf[b'TWINE_REPOSITORY'], username=self.conf[b'TWINE_USERNAME'], identity=self.conf.get(b'identity'), password=self.conf[b'TWINE_PASSWORD'], comment=self.conf.get(b'comment'), sign_with=self.conf.get(b'sign-with'), config_file=self.confpath, skip_existing=self.conf.get(b'skip-existing', True)), [
                     (b'dist/*{0}*').format(self.conf.get(b'version', __version__))])
        except requests.exceptions.HTTPError as err:
            print(err)

        self.hook([])