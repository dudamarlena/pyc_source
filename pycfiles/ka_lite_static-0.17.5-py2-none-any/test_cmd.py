# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/tests/test_cmd.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import os, sys, StringIO, tempfile, unittest
from contextlib import contextmanager

@contextmanager
def redirected_input_output(input=''):
    old_inp, old_out = sys.stdin, sys.stdout
    inp, out = StringIO.StringIO(input), StringIO.StringIO()
    sys.stdin, sys.stdout = inp, out
    try:
        yield out
    finally:
        sys.stdin, sys.stdout = old_inp, old_out


@contextmanager
def redirected_sys_argv(argv):
    old = sys.argv
    sys.argv = argv
    try:
        yield argv
    finally:
        sys.argv = old


class CmdTestCase(unittest.TestCase):

    def setUp(self):
        fd, path = tempfile.mkstemp()
        self.path = path
        with os.fdopen(fd, 'w') as (fout):
            fout.write('var global = 5;')

    def tearDown(self):
        os.remove(self.path)

    def test_main_dash_m_with_input_file(self):
        from slimit.minifier import main
        out = StringIO.StringIO()
        main(['-m', '-t', self.path], out=out)
        self.assertEqual('var a=5;', out.getvalue())

    def test_main_dash_dash_mangle_with_input_file(self):
        from slimit.minifier import main
        out = StringIO.StringIO()
        main(['--mangle', '--mangle-toplevel', self.path], out=out)
        self.assertEqual('var a=5;', out.getvalue())

    def test_main_dash_m_with_mock_stdin(self):
        from slimit.minifier import main
        out = StringIO.StringIO()
        inp = StringIO.StringIO('function foo() { var local = 5; }')
        main(['-m'], inp=inp, out=out)
        self.assertEqual('function foo(){var a=5;}', out.getvalue())

    def test_main_stdin_stdout(self):
        old_module = None
        try:
            old_module = sys.modules.pop('slimit.minifier')
        except KeyError:
            pass

        with redirected_input_output(input='function foo() { var local = 5; }') as (out):
            from slimit.minifier import main
            main(['-m'])
        self.assertEqual('function foo(){var a=5;}', out.getvalue())
        if old_module is not None:
            sys.modules['slimit.minifier'] = old_module
        return

    def test_main_sys_argv(self):
        out = StringIO.StringIO()
        inp = StringIO.StringIO('var global = 5;')
        with redirected_sys_argv(['slimit', '-m', '-t']):
            from slimit.minifier import main
            main(inp=inp, out=out)
        self.assertEqual('var a=5;', out.getvalue())