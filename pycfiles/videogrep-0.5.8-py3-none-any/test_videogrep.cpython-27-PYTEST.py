# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sam/Dropbox/Projects/videogrep/build/lib/videogrep/tests/test_videogrep.py
# Compiled at: 2016-08-28 23:16:12
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from subprocess import call
from videogrep import videogrep
filename = 'TEST_OUTPUT.mp4'

def test_videogrep():
    videogrep.videogrep('test_videos/test.mp4', filename, 'video', 'pos')
    files = os.listdir('.')
    @py_assert1 = filename in files
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (filename, files)) % {'py0': @pytest_ar._saferepr(filename) if 'filename' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filename) else 'filename', 'py2': @pytest_ar._saferepr(files) if 'files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(files) else 'files'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_cli():
    command = 'videogrep_cli.py -i test_videos/test.mp4 -s video -st pos'
    call(command.split())
    files = os.listdir('.')
    @py_assert0 = 'supercut.mp4'
    @py_assert2 = @py_assert0 in files
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, files)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(files) if 'files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(files) else 'files'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


def test_cleanup():
    call(['rm', filename])
    call(['rm', 'supercut.mp4'])