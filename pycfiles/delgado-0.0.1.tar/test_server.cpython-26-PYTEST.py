# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alfredo/python/delgado/delgado/tests/test_server.py
# Compiled at: 2013-03-11 23:52:29
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from mock import Mock
from pytest import raises
from delgado import server

class TestServer(object):

    def setup(self):
        self.conn = Mock()
        self.conn.return_value = self.conn

    def set_debug_level(self):
        import delgado
        delgado.config['verbosity'] = 'debug'

    def test_run(self):
        fake_conn = Mock(side_effect=TypeError)
        srv = server.Server([], connection=fake_conn)
        with raises(TypeError):
            srv.parse_args()

    def test_not_allowed(self, capsys):
        self.set_debug_level()
        self.conn.recv = Mock(side_effect=['{"ls": []}', TypeError])
        srv = server.Server([], connection=self.conn)
        with raises(TypeError):
            srv.parse_args()
        (out, err) = capsys.readouterr()
        @py_assert0 = 'ls, is not allow'
        @py_assert2 = @py_assert0 in out
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, out)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() is not @py_builtins.globals() else 'out'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        return