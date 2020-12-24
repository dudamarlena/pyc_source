# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py
# Compiled at: 2019-10-16 12:05:38
# Size of source mod 2**32: 16170 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, signal, pytest
from paleomix.atomiccmd.command import AtomicCmd
from paleomix.atomiccmd.sets import ParallelCmds, SequentialCmds
from paleomix.atomiccmd.pprint import pformat, _pformat_list

def test_pformat__simple():
    cmd = AtomicCmd(('touch', 'something'))
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = touch something\nSTDOUT* = '${TEMP_DIR}/pipe_touch_%i.stdout'\nSTDERR* = '${TEMP_DIR}/pipe_touch_%i.stderr'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=40)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__simple__running(tmp_path):
    cmd = AtomicCmd(('sleep', '10'))
    cmd.run(tmp_path)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = sleep 10\nStatus  = Running ...\nSTDOUT* = '{temp_dir}/pipe_sleep_{id}.stdout'\nSTDERR* = '{temp_dir}/pipe_sleep_{id}.stderr'\nCWD     = '{cwd}'"
    @py_assert7 = @py_assert5.format
    @py_assert11 = id(cmd)
    @py_assert14 = os.getcwd
    @py_assert16 = @py_assert14()
    @py_assert19 = @py_assert7(id=@py_assert11, cwd=@py_assert16, temp_dir=tmp_path)
    @py_assert4 = @py_assert2 == @py_assert19
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=50)
    if not @py_assert4:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py20)s\n{%(py20)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(id=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, cwd=%(py17)s\n{%(py17)s = %(py15)s\n{%(py15)s = %(py13)s.getcwd\n}()\n}, temp_dir=%(py18)s)\n}',), (@py_assert2, @py_assert19)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py18':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py20':@pytest_ar._saferepr(@py_assert19)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert14 = @py_assert16 = @py_assert19 = None
    cmd.terminate()
    cmd.join()


def test_pformat__simple__running__set_cwd(tmp_path):
    cmd = AtomicCmd(('sleep', '10'), set_cwd=True)
    cmd.run(tmp_path)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = sleep 10\nStatus  = Running ...\nSTDOUT* = 'pipe_sleep_{id}.stdout'\nSTDERR* = 'pipe_sleep_{id}.stderr'\nCWD     = '{temp_dir}'"
    @py_assert7 = @py_assert5.format
    @py_assert11 = id(cmd)
    @py_assert14 = @py_assert7(id=@py_assert11, temp_dir=tmp_path)
    @py_assert4 = @py_assert2 == @py_assert14
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=64)
    if not @py_assert4:
        @py_format16 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py15)s\n{%(py15)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(id=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, temp_dir=%(py13)s)\n}', ), (@py_assert2, @py_assert14)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert14 = None
    cmd.terminate()
    cmd.join()


def test_pformat__simple__done(tmp_path):
    cmd = AtomicCmd('true')
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=78)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = true\nStatus  = Exited with return-code 0\nSTDOUT* = '{temp_dir}/pipe_true_{id}.stdout'\nSTDERR* = '{temp_dir}/pipe_true_{id}.stderr'\nCWD     = '{cwd}'"
    @py_assert7 = @py_assert5.format
    @py_assert11 = id(cmd)
    @py_assert14 = os.getcwd
    @py_assert16 = @py_assert14()
    @py_assert19 = @py_assert7(id=@py_assert11, cwd=@py_assert16, temp_dir=tmp_path)
    @py_assert4 = @py_assert2 == @py_assert19
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=79)
    if not @py_assert4:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py20)s\n{%(py20)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(id=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, cwd=%(py17)s\n{%(py17)s = %(py15)s\n{%(py15)s = %(py13)s.getcwd\n}()\n}, temp_dir=%(py18)s)\n}',), (@py_assert2, @py_assert19)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py18':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py20':@pytest_ar._saferepr(@py_assert19)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert14 = @py_assert16 = @py_assert19 = None


def test_pformat__simple__done__before_join(tmp_path):
    cmd = AtomicCmd('true')
    cmd.run(tmp_path)
    cmd._proc.wait()
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = true\nStatus  = Exited with return-code 0\nSTDOUT* = '{temp_dir}/pipe_true_{id}.stdout'\nSTDERR* = '{temp_dir}/pipe_true_{id}.stderr'\nCWD     = '{cwd}'"
    @py_assert7 = @py_assert5.format
    @py_assert11 = id(cmd)
    @py_assert14 = os.getcwd
    @py_assert16 = @py_assert14()
    @py_assert19 = @py_assert7(id=@py_assert11, cwd=@py_assert16, temp_dir=tmp_path)
    @py_assert4 = @py_assert2 == @py_assert19
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=92)
    if not @py_assert4:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py20)s\n{%(py20)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(id=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, cwd=%(py17)s\n{%(py17)s = %(py15)s\n{%(py15)s = %(py13)s.getcwd\n}()\n}, temp_dir=%(py18)s)\n}',), (@py_assert2, @py_assert19)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py15':@pytest_ar._saferepr(@py_assert14),  'py17':@pytest_ar._saferepr(@py_assert16),  'py18':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py20':@pytest_ar._saferepr(@py_assert19)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert14 = @py_assert16 = @py_assert19 = None
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=99)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_pformat__simple__done__set_cwd(tmp_path):
    cmd = AtomicCmd('true', set_cwd=True)
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=105)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = true\nStatus  = Exited with return-code 0\nSTDOUT* = 'pipe_true_{id}.stdout'\nSTDERR* = 'pipe_true_{id}.stderr'\nCWD     = '{temp_dir}'"
    @py_assert7 = @py_assert5.format
    @py_assert11 = id(cmd)
    @py_assert14 = @py_assert7(id=@py_assert11, temp_dir=tmp_path)
    @py_assert4 = @py_assert2 == @py_assert14
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=106)
    if not @py_assert4:
        @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py15)s\n{%(py15)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(id=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, temp_dir=%(py13)s)\n}',), (@py_assert2, @py_assert14)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py15':@pytest_ar._saferepr(@py_assert14)}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert14 = None


def test_pformat__simple__terminated_by_pipeline(tmp_path):
    cmd = AtomicCmd(('sleep', '10'))
    cmd.run(tmp_path)
    cmd.terminate()
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     'SIGTERM']
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=119)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = sleep 10\nStatus  = Automatically terminated by PALEOMIX\nSTDOUT* = '{temp_dir}/pipe_sleep_{id}.stdout'\nSTDERR* = '{temp_dir}/pipe_sleep_{id}.stderr'\nCWD     = '{cwd}'"
    @py_assert7 = @py_assert5.format
    @py_assert11 = id(cmd)
    @py_assert15 = os.getcwd
    @py_assert17 = @py_assert15()
    @py_assert19 = @py_assert7(id=@py_assert11, temp_dir=tmp_path, cwd=@py_assert17)
    @py_assert4 = @py_assert2 == @py_assert19
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=120)
    if not @py_assert4:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py20)s\n{%(py20)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(id=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, temp_dir=%(py13)s, cwd=%(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py14)s.getcwd\n}()\n})\n}',), (@py_assert2, @py_assert19)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py14':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert15 = @py_assert17 = @py_assert19 = None


def test_pformat__simple__killed_by_signal(tmp_path):
    cmd = AtomicCmd(('sleep', '10'))
    cmd.run(tmp_path)
    os.killpg(cmd._proc.pid, signal.SIGTERM)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     'SIGTERM']
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=133)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = sleep 10\nStatus  = Terminated with signal SIGTERM\nSTDOUT* = '{temp_dir}/pipe_sleep_{id}.stdout'\nSTDERR* = '{temp_dir}/pipe_sleep_{id}.stderr'\nCWD     = '{cwd}'"
    @py_assert7 = @py_assert5.format
    @py_assert11 = id(cmd)
    @py_assert15 = os.getcwd
    @py_assert17 = @py_assert15()
    @py_assert19 = @py_assert7(id=@py_assert11, temp_dir=tmp_path, cwd=@py_assert17)
    @py_assert4 = @py_assert2 == @py_assert19
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=134)
    if not @py_assert4:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py20)s\n{%(py20)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(id=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, temp_dir=%(py13)s, cwd=%(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py14)s.getcwd\n}()\n})\n}',), (@py_assert2, @py_assert19)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py14':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert15 = @py_assert17 = @py_assert19 = None


def test_pformat__simple__temp_root_in_arguments(tmp_path):
    cmd = AtomicCmd(('echo', '${TEMP_DIR}'))
    cmd.run(tmp_path)
    @py_assert1 = cmd.join
    @py_assert3 = @py_assert1()
    @py_assert6 = [
     0]
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=146)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.join\n}()\n} == %(py7)s',), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = echo '{temp_dir}'\nStatus  = Exited with return-code 0\nSTDOUT* = '{temp_dir}/pipe_echo_{id}.stdout'\nSTDERR* = '{temp_dir}/pipe_echo_{id}.stderr'\nCWD     = '{cwd}'"
    @py_assert7 = @py_assert5.format
    @py_assert11 = id(cmd)
    @py_assert15 = os.getcwd
    @py_assert17 = @py_assert15()
    @py_assert19 = @py_assert7(id=@py_assert11, temp_dir=tmp_path, cwd=@py_assert17)
    @py_assert4 = @py_assert2 == @py_assert19
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=147)
    if not @py_assert4:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py20)s\n{%(py20)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(id=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, temp_dir=%(py13)s, cwd=%(py18)s\n{%(py18)s = %(py16)s\n{%(py16)s = %(py14)s.getcwd\n}()\n})\n}',), (@py_assert2, @py_assert19)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(tmp_path) if 'tmp_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tmp_path) else 'tmp_path',  'py14':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17),  'py20':@pytest_ar._saferepr(@py_assert19)}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert15 = @py_assert17 = @py_assert19 = None


def test_pformat__atomiccmd__simple_with_infile():
    cmd = AtomicCmd(('cat', '%(IN_SOMETHING)s'), IN_SOMETHING='/etc/fstab')
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = cat /etc/fstab\nSTDOUT* = '${TEMP_DIR}/pipe_cat_%i.stdout'\nSTDERR* = '${TEMP_DIR}/pipe_cat_%i.stderr'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=163)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_infile__set_cwd():
    cmd = AtomicCmd(('cat', '%(IN_SOMETHING)s'),
      IN_SOMETHING='/etc/fstab', set_cwd=True)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = cat /etc/fstab\nSTDOUT* = 'pipe_cat_%i.stdout'\nSTDERR* = 'pipe_cat_%i.stderr'\nCWD     = '${TEMP_DIR}'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=174)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_temp_infile():
    cmd = AtomicCmd(('cat', '%(TEMP_IN_FILE)s'), TEMP_IN_FILE='infile.txt')
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = cat '${TEMP_DIR}/infile.txt'\nSTDOUT* = '${TEMP_DIR}/pipe_cat_%i.stdout'\nSTDERR* = '${TEMP_DIR}/pipe_cat_%i.stderr'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=185)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_temp_infile__set_cwd():
    cmd = AtomicCmd(('zcat', '%(TEMP_IN_FILE)s'),
      TEMP_IN_FILE='infile.gz', set_cwd=True)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = zcat infile.gz\nSTDOUT* = 'pipe_zcat_%i.stdout'\nSTDERR* = 'pipe_zcat_%i.stderr'\nCWD     = '${TEMP_DIR}'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=197)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_outfile():
    cmd = AtomicCmd(('touch', '%(OUT_RC)s'), OUT_RC='/etc/bashrc')
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = touch '${TEMP_DIR}/bashrc'\nSTDOUT* = '${TEMP_DIR}/pipe_touch_%i.stdout'\nSTDERR* = '${TEMP_DIR}/pipe_touch_%i.stderr'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=212)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_outfile__set_cwd():
    cmd = AtomicCmd(('touch', '%(OUT_RC)s'), OUT_RC='/etc/bashrc', set_cwd=True)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = touch bashrc\nSTDOUT* = 'pipe_touch_%i.stdout'\nSTDERR* = 'pipe_touch_%i.stderr'\nCWD     = '${TEMP_DIR}'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=222)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_temp_outfile():
    cmd = AtomicCmd(('touch', '%(TEMP_OUT_RC)s'), TEMP_OUT_RC='bashrc')
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = touch '${TEMP_DIR}/bashrc'\nSTDOUT* = '${TEMP_DIR}/pipe_touch_%i.stdout'\nSTDERR* = '${TEMP_DIR}/pipe_touch_%i.stderr'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=233)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_temp_outfile__set_cwd():
    cmd = AtomicCmd(('touch', '%(TEMP_OUT_RC)s'), TEMP_OUT_RC='bashrc', set_cwd=True)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = touch bashrc\nSTDOUT* = 'pipe_touch_%i.stdout'\nSTDERR* = 'pipe_touch_%i.stderr'\nCWD     = '${TEMP_DIR}'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=243)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_stdin():
    cmd = AtomicCmd('gzip', IN_STDIN='/etc/fstab')
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = gzip\nSTDIN   = '/etc/fstab'\nSTDOUT* = '${TEMP_DIR}/pipe_gzip_%i.stdout'\nSTDERR* = '${TEMP_DIR}/pipe_gzip_%i.stderr'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=258)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_stdin__set_cwd():
    cmd = AtomicCmd('gzip', IN_STDIN='/etc/fstab', set_cwd=True)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = gzip\nSTDIN   = '/etc/fstab'\nSTDOUT* = 'pipe_gzip_%i.stdout'\nSTDERR* = 'pipe_gzip_%i.stderr'\nCWD     = '${TEMP_DIR}'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=268)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_temp_stdin():
    cmd = AtomicCmd('gzip', TEMP_IN_STDIN='stabstabstab')
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = gzip\nSTDIN*  = '${TEMP_DIR}/stabstabstab'\nSTDOUT* = '${TEMP_DIR}/pipe_gzip_%i.stdout'\nSTDERR* = '${TEMP_DIR}/pipe_gzip_%i.stderr'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=279)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_temp_stdin__set_cwd():
    cmd = AtomicCmd('gzip', TEMP_IN_STDIN='stabstabstab', set_cwd=True)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = gzip\nSTDIN*  = 'stabstabstab'\nSTDOUT* = 'pipe_gzip_%i.stdout'\nSTDERR* = 'pipe_gzip_%i.stderr'\nCWD     = '${TEMP_DIR}'"
    @py_assert7 = (
     id(cmd), id(cmd))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=289)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_stdin__cmd():
    cmd_1 = AtomicCmd('gzip', OUT_STDOUT=(AtomicCmd.PIPE))
    cmd_2 = AtomicCmd('gzip', IN_STDIN=cmd_1)
    @py_assert2 = pformat(cmd_2)
    @py_assert5 = "Command = gzip\nSTDIN   = <PIPE>\nSTDOUT* = '${TEMP_DIR}/pipe_gzip_%i.stdout'\nSTDERR* = '${TEMP_DIR}/pipe_gzip_%i.stderr'"
    @py_assert7 = (
     id(cmd_2), id(cmd_2))
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=301)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd_2) if 'cmd_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2) else 'cmd_2',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_stdout():
    cmd = AtomicCmd(('echo', 'Water. Water.'), OUT_STDOUT='/dev/ls')
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = echo 'Water. Water.'\nSTDOUT  = '${TEMP_DIR}/ls'\nSTDERR* = '${TEMP_DIR}/pipe_echo_%i.stderr'"
    @py_assert7 = (
     id(cmd),)
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=316)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_stdout__set_cwd():
    cmd = AtomicCmd(('echo', '*pant*. *pant*.'), OUT_STDOUT='/dev/barf', set_cwd=True)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = echo '*pant*. *pant*.'\nSTDOUT  = 'barf'\nSTDERR* = 'pipe_echo_%i.stderr'\nCWD     = '${TEMP_DIR}'"
    @py_assert7 = (
     id(cmd),)
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=325)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_temp_stdout():
    cmd = AtomicCmd(('echo', 'Oil. Oil.'), TEMP_OUT_STDOUT='dm')
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = echo 'Oil. Oil.'\nSTDOUT* = '${TEMP_DIR}/dm'\nSTDERR* = '${TEMP_DIR}/pipe_echo_%i.stderr'"
    @py_assert7 = (
     id(cmd),)
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=335)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_temp_stdout__set_cwd():
    cmd = AtomicCmd(('echo', 'Room service. Room service.'),
      TEMP_OUT_STDOUT='pv', set_cwd=True)
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = echo 'Room service. Room service.'\nSTDOUT* = 'pv'\nSTDERR* = 'pipe_echo_%i.stderr'\nCWD     = '${TEMP_DIR}'"
    @py_assert7 = (
     id(cmd),)
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=346)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_pformat__atomiccmd__simple_with_stdout_pipe():
    cmd = AtomicCmd(('echo', '!'), OUT_STDOUT=(AtomicCmd.PIPE))
    @py_assert2 = pformat(cmd)
    @py_assert5 = "Command = echo '!'\nSTDOUT  = <PIPE>\nSTDERR* = '${TEMP_DIR}/pipe_echo_%i.stderr'"
    @py_assert7 = (
     id(cmd),)
    @py_assert9 = @py_assert5 % @py_assert7
    @py_assert4 = @py_assert2 == @py_assert9
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=356)
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == (%(py6)s %% %(py8)s)', ), (@py_assert2, @py_assert9)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert9 = None


@pytest.mark.parametrize('cls, description', (
 (
  ParallelCmds, 'Parallel processes'), (SequentialCmds, 'Sequential processes')))
def test_pformat__sets__simple(cls, description):
    template = "{description}:\n  Process 1:\n    Command = echo foo\n    STDOUT  = Piped to process 2\n    STDERR* = '${{TEMP_DIR}}/pipe_echo_{cmd_1_id}.stderr'\n\n  Process 2:\n    Command = gzip\n    STDIN   = Piped from process 1\n    STDOUT* = '${{TEMP_DIR}}/pipe_gzip_{cmd_2_id}.stdout'\n    STDERR* = '${{TEMP_DIR}}/pipe_gzip_{cmd_2_id}.stderr'"
    cmd_1 = AtomicCmd(('echo', 'foo'), OUT_STDOUT=(AtomicCmd.PIPE))
    cmd_2 = AtomicCmd('gzip', IN_STDIN=cmd_1)
    cmd = cls((cmd_1, cmd_2))
    @py_assert2 = pformat(cmd)
    @py_assert6 = template.format
    @py_assert11 = id(cmd_1)
    @py_assert15 = id(cmd_2)
    @py_assert17 = @py_assert6(description=description, cmd_1_id=@py_assert11, cmd_2_id=@py_assert15)
    @py_assert4 = @py_assert2 == @py_assert17
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=390)
    if not @py_assert4:
        @py_format19 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py18)s\n{%(py18)s = %(py7)s\n{%(py7)s = %(py5)s.format\n}(description=%(py8)s, cmd_1_id=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, cmd_2_id=%(py16)s\n{%(py16)s = %(py13)s(%(py14)s)\n})\n}',), (@py_assert2, @py_assert17)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(cmd) if 'cmd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd) else 'cmd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(template) if 'template' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(template) else 'template',  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(description) if 'description' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(description) else 'description',  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd_1) if 'cmd_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_1) else 'cmd_1',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py14':@pytest_ar._saferepr(cmd_2) if 'cmd_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2) else 'cmd_2',  'py16':@pytest_ar._saferepr(@py_assert15),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = ('' + 'assert %(py20)s') % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert11 = @py_assert15 = @py_assert17 = None


def test_pformat__sets__nested():
    cmd_1 = AtomicCmd(('echo', 'foo'), OUT_STDOUT=(AtomicCmd.PIPE))
    cmd_2 = AtomicCmd('gzip', IN_STDIN=cmd_1)
    cmd_3 = AtomicCmd('sha1sum')
    set_1 = ParallelCmds((cmd_1, cmd_2))
    set_2 = SequentialCmds((set_1, cmd_3))
    @py_assert2 = pformat(set_2)
    @py_assert5 = "Sequential processes:\n  Parallel processes:\n    Process 1:\n      Command = echo foo\n      STDOUT  = Piped to process 2\n      STDERR* = '${{TEMP_DIR}}/pipe_echo_{cmd_1}.stderr'\n\n    Process 2:\n      Command = gzip\n      STDIN   = Piped from process 1\n      STDOUT* = '${{TEMP_DIR}}/pipe_gzip_{cmd_2}.stdout'\n      STDERR* = '${{TEMP_DIR}}/pipe_gzip_{cmd_2}.stderr'\n\n  Process 3:\n    Command = sha1sum\n    STDOUT* = '${{TEMP_DIR}}/pipe_sha1sum_{cmd_3}.stdout'\n    STDERR* = '${{TEMP_DIR}}/pipe_sha1sum_{cmd_3}.stderr'"
    @py_assert7 = @py_assert5.format
    @py_assert11 = id(cmd_1)
    @py_assert15 = id(cmd_2)
    @py_assert19 = id(cmd_3)
    @py_assert21 = @py_assert7(cmd_1=@py_assert11, cmd_2=@py_assert15, cmd_3=@py_assert19)
    @py_assert4 = @py_assert2 == @py_assert21
    if @py_assert4 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=401)
    if not @py_assert4:
        @py_format23 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py22)s\n{%(py22)s = %(py8)s\n{%(py8)s = %(py6)s.format\n}(cmd_1=%(py12)s\n{%(py12)s = %(py9)s(%(py10)s)\n}, cmd_2=%(py16)s\n{%(py16)s = %(py13)s(%(py14)s)\n}, cmd_3=%(py20)s\n{%(py20)s = %(py17)s(%(py18)s)\n})\n}',), (@py_assert2, @py_assert21)) % {'py0':@pytest_ar._saferepr(pformat) if 'pformat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pformat) else 'pformat',  'py1':@pytest_ar._saferepr(set_2) if 'set_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set_2) else 'set_2',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py9':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py10':@pytest_ar._saferepr(cmd_1) if 'cmd_1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_1) else 'cmd_1',  'py12':@pytest_ar._saferepr(@py_assert11),  'py13':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py14':@pytest_ar._saferepr(cmd_2) if 'cmd_2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_2) else 'cmd_2',  'py16':@pytest_ar._saferepr(@py_assert15),  'py17':@pytest_ar._saferepr(id) if 'id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id) else 'id',  'py18':@pytest_ar._saferepr(cmd_3) if 'cmd_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cmd_3) else 'cmd_3',  'py20':@pytest_ar._saferepr(@py_assert19),  'py22':@pytest_ar._saferepr(@py_assert21)}
        @py_format25 = ('' + 'assert %(py24)s') % {'py24': @py_format23}
        raise AssertionError(@pytest_ar._format_explanation(@py_format25))
    @py_assert2 = @py_assert4 = @py_assert5 = @py_assert7 = @py_assert11 = @py_assert15 = @py_assert19 = @py_assert21 = None


@pytest.mark.parametrize('value', (1, {}, ''))
def test_pformat__bad_input(value):
    with pytest.raises(TypeError):
        pformat(value)


def test_pformat_list__empty():
    @py_assert1 = []
    @py_assert3 = _pformat_list(@py_assert1)
    @py_assert6 = ''
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=439)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_pformat_list__single():
    @py_assert1 = [
     3]
    @py_assert3 = _pformat_list(@py_assert1)
    @py_assert6 = '3'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=443)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_pformat_list__multiple():
    @py_assert1 = [
     3, 2, 1]
    @py_assert3 = _pformat_list(@py_assert1)
    @py_assert6 = '3 2 1'
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=447)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_pformat_list__wrapped():
    @py_assert1 = [
     3, 2, 1]
    @py_assert3 = 1
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = '3 \\\n    2 \\\n    1'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=451)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = [3, 2, 1]
    @py_assert3 = 2
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = '3 \\\n    2 \\\n    1'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=452)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = [3, 2, 1]
    @py_assert3 = 3
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = '3 \\\n    2 \\\n    1'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=453)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = [3, 2, 1]
    @py_assert3 = 4
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = '3 2 \\\n    1'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=454)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = [3, 2, 1]
    @py_assert3 = 5
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = '3 2 \\\n    1'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=455)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = [3, 2, 1]
    @py_assert3 = 6
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = '3 2 1'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=456)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = [3, 2, 1]
    @py_assert3 = 7
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = '3 2 1'
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=457)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_pformat_list__escaped():
    @py_assert1 = [
     'a', 'b c']
    @py_assert3 = 100
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = "a 'b c'"
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=461)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = ['a', '$c']
    @py_assert3 = 100
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = "a '$c'"
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=462)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = ['!a', 'c']
    @py_assert3 = 100
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = "'!a' c"
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=463)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = ['a', "'c"]
    @py_assert3 = 100
    @py_assert5 = _pformat_list(@py_assert1, width=@py_assert3)
    @py_assert8 = 'a \'\'"\'"\'c\''
    @py_assert7 = @py_assert5 == @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/mischu/devel/paleomix/tests/atomiccmd_test/pprint_test.py', lineno=464)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, width=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(_pformat_list) if '_pformat_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_pformat_list) else '_pformat_list',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None