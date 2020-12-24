# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/andres/Dev/whatodo/build/lib/src/test_todo.py
# Compiled at: 2015-04-18 19:12:32
# Size of source mod 2**32: 1701 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from main import *
test_files = ['examples/C/filenames/script', 'examples/Clojure/index.cljs.hl',
 'examples/Chapel/lulesh.chpl', 'examples/Forth/core.fth',
 'examples/GAP/Magic.gd', 'examples/JavaScript/steelseries-min.js',
 'examples/Matlab/FTLE_reg.m', 'examples/Perl6/for.t',
 'examples/VimL/solarized.vim', 'examples/C/cpu.c',
 'examples/CSS/bootstrap.css', 'examples/D/mpq.d',
 'examples/Go/api.pb.go', 'examples/HTML+ERB/index.html.erb']
number_of_comments = [
 423,
 13,
 609,
 0,
 3,
 2,
 6,
 586,
 20,
 39,
 680,
 167,
 0,
 10]

def test_get_comment_tokens():
    from pygments.lexers.c_cpp import CLexer
    file_text_test = 'int main(int argc, char[] argv){\n//This is a comment\n}\n'
    c_lexer = CLexer()
    results = []
    for comment in get_comment_tokens(file_text_test, c_lexer):
        results.append(comment)

    @py_assert2 = len(results)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = results[0]
    @py_assert3 = '//This is a comment\n'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_get_tokens_from_file():
    for index, file in enumerate(test_files, 0):
        result = get_tokens_from_file('../' + file)
        print(file)
        @py_assert0 = number_of_comments[index]
        @py_assert5 = result.keys
        @py_assert7 = @py_assert5()
        @py_assert9 = len(@py_assert7)
        @py_assert2 = @py_assert0 == @py_assert9
        if not @py_assert2:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py10)s\n{%(py10)s = %(py3)s(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.keys\n}()\n})\n}', ), (@py_assert0, @py_assert9)) % {'py4': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py6': @pytest_ar._saferepr(@py_assert5),  'py8': @pytest_ar._saferepr(@py_assert7),  'py1': @pytest_ar._saferepr(@py_assert0),  'py10': @pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = None

    return