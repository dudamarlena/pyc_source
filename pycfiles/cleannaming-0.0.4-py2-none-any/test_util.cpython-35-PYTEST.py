# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/cosmin/workspace/github/cleanmymac/build/lib/cleanmymac/test/test_util.py
# Compiled at: 2016-02-14 18:36:43
# Size of source mod 2**32: 1352 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, tempfile, pytest, os
from cleanmymac.util import yaml_files, delete_dir_content, Dir

def test_yaml_files():
    with tempfile.NamedTemporaryFile(suffix='.yaml') as (a_file):
        files = list(yaml_files(tempfile.gettempdir()))
        @py_assert2 = len(files)
        @py_assert5 = 1
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(files) if 'files' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(files) else 'files', 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None


def test_delete_dir_content():
    start_len = len(os.listdir(tempfile.gettempdir()))
    with tempfile.NamedTemporaryFile() as (a_file):
        with tempfile.NamedTemporaryFile() as (b_file):
            @py_assert2 = os.listdir
            @py_assert5 = tempfile.gettempdir
            @py_assert7 = @py_assert5()
            @py_assert9 = @py_assert2(@py_assert7)
            @py_assert11 = len(@py_assert9)
            @py_assert15 = 2
            @py_assert17 = start_len + @py_assert15
            @py_assert13 = @py_assert11 == @py_assert17
            if not @py_assert13:
                @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.gettempdir\n}()\n})\n})\n} == (%(py14)s + %(py16)s)',), (@py_assert11, @py_assert17)) % {'py1': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py12': @pytest_ar._saferepr(@py_assert11), 'py4': @pytest_ar._saferepr(tempfile) if 'tempfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tempfile) else 'tempfile', 'py8': @pytest_ar._saferepr(@py_assert7), 'py16': @pytest_ar._saferepr(@py_assert15), 'py10': @pytest_ar._saferepr(@py_assert9), 'py14': @pytest_ar._saferepr(start_len) if 'start_len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(start_len) else 'start_len', 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
                @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
                raise AssertionError(@pytest_ar._format_explanation(@py_format20))
            @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert15 = @py_assert17 = None
    delete_dir_content(Dir(tempfile.gettempdir()))
    @py_assert2 = os.listdir
    @py_assert5 = tempfile.gettempdir
    @py_assert7 = @py_assert5()
    @py_assert9 = @py_assert2(@py_assert7)
    @py_assert11 = len(@py_assert9)
    @py_assert14 = 0
    @py_assert13 = @py_assert11 == @py_assert14
    if not @py_assert13:
        @py_format16 = @pytest_ar._call_reprcompare(('==',), (@py_assert13,), ('%(py12)s\n{%(py12)s = %(py0)s(%(py10)s\n{%(py10)s = %(py3)s\n{%(py3)s = %(py1)s.listdir\n}(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.gettempdir\n}()\n})\n})\n} == %(py15)s',), (@py_assert11, @py_assert14)) % {'py1': @pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os', 'py12': @pytest_ar._saferepr(@py_assert11), 'py4': @pytest_ar._saferepr(tempfile) if 'tempfile' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tempfile) else 'tempfile', 'py8': @pytest_ar._saferepr(@py_assert7), 'py10': @pytest_ar._saferepr(@py_assert9), 'py15': @pytest_ar._saferepr(@py_assert14), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format18 = ('' + 'assert %(py17)s') % {'py17': @py_format16}
        raise AssertionError(@pytest_ar._format_explanation(@py_format18))
    @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = @py_assert14 = None
    with pytest.raises(AssertionError):
        delete_dir_content(tempfile.gettempdir())