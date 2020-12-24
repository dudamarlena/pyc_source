# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py
# Compiled at: 2019-05-13 06:18:18
# Size of source mod 2**32: 7710 bytes
"""Functional tests for the rendering script.

These tests create files on the filesystem, bring up a small webserver and
generally test the script under reasonably realistic conditions.
"""
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest, subprocess, threading
try:
    import SimpleHTTPServer, SocketServer
except ImportError:
    from http import server as SimpleHTTPServer
    import socketserver as SocketServer

@pytest.fixture
def rootdir(tmpdir):
    """Directory with prepared list fragments."""
    rootdir = tmpdir.join('root')
    rootdir.mkdir()
    rootdir.join('simple.txt').write('[Adblock]\nOk')
    rootdir.join('unicode.txt').write('[Adblock]\nሴ'.encode('utf-8'), mode='wb')
    rootdir.join('includer.txt').write('[Adblock]\n%include inc:includee.txt%')
    rootdir.join('circ.txt').write('[Adblock]\n%include inc:circular.txt%')
    rootdir.join('brk.txt').write('[Adblock]\n%include inc:broken.txt%')
    incdir = rootdir.join('inc')
    incdir.mkdir()
    incdir.join('includee.txt').write('I am included!')
    incdir.join('broken.txt').write('%include missing.txt%')
    incdir.join('circular.txt').write('%include circular.txt%')
    return rootdir


@pytest.fixture
def webserver_port(tmpdir, request):
    """Serve fragments via HTTP on a random port (return the port number)."""
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(('', 0), handler)
    port = httpd.socket.getsockname()[1]
    webroot = tmpdir.join('webroot')
    webroot.mkdir()
    webroot.join('inc.txt').write('Web ሴ'.encode('utf-8'), mode='wb')
    webroot.join('metainc.txt').write('%include http://localhost:{}/inc.txt%'.format(port))
    os.chdir(str(webroot))
    thread = threading.Thread(target=httpd.serve_forever)
    thread.setDaemon(True)
    thread.start()
    request.addfinalizer(httpd.shutdown)
    return port


@pytest.fixture
def dstfile(tmpdir):
    """Destination file for saving rendered list."""
    return tmpdir.join('dst')


def run_script(*args, **kw):
    """Run rendering script with given arguments and return its output."""
    cmd = [
     'flrender'] + list(args)
    test_in = kw.pop('test_in', None)
    if test_in is not None:
        test_in = test_in.encode('utf-8')
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE, **kw)
    stdout, stderr = proc.communicate(input=test_in)
    return (proc.returncode, stderr.decode('utf-8'), stdout.decode('utf-8'))


@pytest.mark.parametrize('test_input, args', [
 (
  'None', ["'simple.txt'", 'str(dstfile)']),
 (
  'None', ["'simple.txt'"]),
 (
  "rootdir.join('simple.txt').read()", [])])
def test_render_no_includes(test_input, args, rootdir, dstfile):
    test_input = eval(test_input)
    args = list(map(eval, args))
    _, _, stdout = run_script(*args, test_in=test_input)
    if len(args) > 1:
        output = dstfile.read()
    else:
        output = stdout
    @py_assert0 = 'Ok'
    @py_assert2 = @py_assert0 in output
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=123)
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, output)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(output) if 'output' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(output) else 'output'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None


def test_render_unicode(rootdir, dstfile):
    code, err, _ = run_script(str(rootdir.join('unicode.txt')), str(dstfile))
    @py_assert0 = 'ሴ'
    @py_assert4 = dstfile.read
    @py_assert6 = 'rb'
    @py_assert8 = @py_assert4(mode=@py_assert6)
    @py_assert10 = @py_assert8.decode
    @py_assert12 = 'utf-8'
    @py_assert14 = @py_assert10(@py_assert12)
    @py_assert2 = @py_assert0 in @py_assert14
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=128)
    if not @py_assert2:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py15)s\n{%(py15)s = %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.read\n}(mode=%(py7)s)\n}.decode\n}(%(py13)s)\n}', ), (@py_assert0, @py_assert14)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py13': @pytest_ar._saferepr(@py_assert12), 'py7': @pytest_ar._saferepr(@py_assert6), 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(dstfile) if 'dstfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dstfile) else 'dstfile', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_render_with_includes(rootdir, dstfile):
    run_script(str(rootdir.join('includer.txt')), str(dstfile), '-i', 'inc=' + str(rootdir.join('inc')))
    @py_assert0 = 'I am included!'
    @py_assert4 = dstfile.read
    @py_assert6 = @py_assert4()
    @py_assert2 = @py_assert0 in @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=134)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.read\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(dstfile) if 'dstfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dstfile) else 'dstfile', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_render_with_includes_relative(rootdir, dstfile):
    run_script('includer.txt', str(dstfile), '-i', 'inc=inc', cwd=str(rootdir))
    @py_assert0 = 'I am included!'
    @py_assert4 = dstfile.read
    @py_assert6 = @py_assert4()
    @py_assert2 = @py_assert0 in @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=139)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.read\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(dstfile) if 'dstfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dstfile) else 'dstfile', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_render_verbose(rootdir, dstfile):
    code, err, _ = run_script('includer.txt', str(dstfile), '-i', 'inc=inc', '-v', cwd=str(rootdir))
    @py_assert2 = 'Rendering: includer.txt\n- including: inc:includee.txt\n'
    @py_assert1 = err == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=145)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_no_header(rootdir, dstfile):
    code, err, _ = run_script('inc/includee.txt', str(dstfile), cwd=str(rootdir))
    @py_assert2 = 1
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=151)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 'No header found at the beginning of the input.\n'
    @py_assert1 = err == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=152)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_wrong_file(dstfile):
    code, err, _ = run_script('wrong.txt', str(dstfile))
    @py_assert2 = 1
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=157)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = "File not found: 'wrong.txt'\n"
    @py_assert1 = err == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=158)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_wrong_include_source(rootdir, dstfile):
    code, err, _ = run_script('brk.txt', str(dstfile), cwd=str(rootdir))
    @py_assert2 = 1
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=163)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = "Unknown source: 'inc' when including 'inc:broken.txt' from 'brk.txt'\n"
    @py_assert1 = err == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=164)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_wrong_include(rootdir, dstfile):
    code, err, _ = run_script('brk.txt', str(dstfile), '-i', 'inc=inc', cwd=str(rootdir))
    missing_path = str(rootdir.join('inc', 'missing.txt'))
    expect = "File not found: '{}' when including 'missing.txt' from 'inc:broken.txt' from 'brk.txt'\n".format(missing_path)
    @py_assert2 = 1
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=174)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = err == expect
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=175)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (err, expect)) % {'py2': @pytest_ar._saferepr(expect) if 'expect' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expect) else 'expect', 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_circular_includes(rootdir, dstfile):
    code, err, _ = run_script('circ.txt', str(dstfile), '-i', 'inc=inc', cwd=str(rootdir))
    expect = "Include loop encountered when including 'circular.txt' from 'circular.txt' from 'inc:circular.txt' from 'circ.txt'\n"
    @py_assert2 = 1
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=183)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = err == expect
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=184)
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (err, expect)) % {'py2': @pytest_ar._saferepr(expect) if 'expect' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expect) else 'expect', 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_wrong_source(rootdir, dstfile):
    code, err, _ = run_script('foo:bar.txt', str(dstfile))
    @py_assert2 = 1
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=189)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = "Unknown source: 'foo'\n"
    @py_assert1 = err == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=190)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (err, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@pytest.mark.tryfirst
@pytest.mark.slowtest
def test_web_include(rootdir, dstfile, webserver_port):
    url = 'http://localhost:{}/metainc.txt'.format(webserver_port)
    webinc = rootdir.join('webinc.txt')
    webinc.write('[Adblock]\n%include {}%'.format(url))
    code, err, _ = run_script(str(webinc), str(dstfile))
    @py_assert0 = 'Web ሴ'
    @py_assert4 = dstfile.read
    @py_assert6 = 'rb'
    @py_assert8 = @py_assert4(mode=@py_assert6)
    @py_assert10 = @py_assert8.decode
    @py_assert12 = 'utf-8'
    @py_assert14 = @py_assert10(@py_assert12)
    @py_assert2 = @py_assert0 in @py_assert14
    if @py_assert2 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=200)
    if not @py_assert2:
        @py_format16 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py15)s\n{%(py15)s = %(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.read\n}(mode=%(py7)s)\n}.decode\n}(%(py13)s)\n}', ), (@py_assert0, @py_assert14)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py13': @pytest_ar._saferepr(@py_assert12), 'py7': @pytest_ar._saferepr(@py_assert6), 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(dstfile) if 'dstfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dstfile) else 'dstfile', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format18 = 'assert %(py17)s' % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


@pytest.mark.slowtest
def test_failed_web_include(rootdir, dstfile, webserver_port):
    url = 'http://localhost:{}/missing.txt'.format(webserver_port)
    webinc = rootdir.join('webinc.txt')
    webinc.write('[Adblock]\n%include {}%'.format(url))
    code, err, _ = run_script(str(webinc), str(dstfile))
    @py_assert2 = 1
    @py_assert1 = code == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=209)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (code, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(code) if 'code' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(code) else 'code'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = err.startswith
    @py_assert3 = "HTTP 404 Not found: '{0}' when including '{0}'"
    @py_assert5 = @py_assert3.format
    @py_assert8 = @py_assert5(url)
    @py_assert10 = @py_assert1(@py_assert8)
    if @py_assert10 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit(PytestAssertRewriteWarning('asserting the value None, please use "assert is None"'), category=None, filename='/home/vkuznetsov/prog/devops/python-abp/tests/test_render_script.py', lineno=210)
    if not @py_assert10:
        @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.startswith\n}(%(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s.format\n}(%(py7)s)\n})\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(err) if 'err' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(err) else 'err', 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py6': @pytest_ar._saferepr(@py_assert5), 'py7': @pytest_ar._saferepr(url) if 'url' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(url) else 'url'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = None