# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_tf_util.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1093 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, tensorflow as tf
from deephyper.search.nas.baselines.common.tf_util import function, initialize, single_threaded_session

def test_function():
    with tf.Graph().as_default():
        x = tf.placeholder((tf.int32), (), name='x')
        y = tf.placeholder((tf.int32), (), name='y')
        z = 3 * x + 2 * y
        lin = function([x, y], z, givens={y: 0})
        with single_threaded_session():
            initialize()
            @py_assert1 = 2
            @py_assert3 = lin(@py_assert1)
            @py_assert6 = 6
            @py_assert5 = @py_assert3 == @py_assert6
            if @py_assert5 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_tf_util.py', lineno=20)
            if not @py_assert5:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lin) if 'lin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lin) else 'lin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
            @py_assert1 = 3
            @py_assert3 = lin(x=@py_assert1)
            @py_assert6 = 9
            @py_assert5 = @py_assert3 == @py_assert6
            if @py_assert5 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_tf_util.py', lineno=21)
            if not @py_assert5:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(x=%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lin) if 'lin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lin) else 'lin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
            @py_assert1 = 2
            @py_assert3 = 2
            @py_assert5 = lin(@py_assert1, @py_assert3)
            @py_assert8 = 10
            @py_assert7 = @py_assert5 == @py_assert8
            if @py_assert7 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_tf_util.py', lineno=22)
            if not @py_assert7:
                @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lin) if 'lin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lin) else 'lin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
                @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
                raise AssertionError(@pytest_ar._format_explanation(@py_format12))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
            @py_assert1 = 2
            @py_assert3 = 3
            @py_assert5 = lin(x=@py_assert1, y=@py_assert3)
            @py_assert8 = 12
            @py_assert7 = @py_assert5 == @py_assert8
            if @py_assert7 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_tf_util.py', lineno=23)
            if not @py_assert7:
                @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(x=%(py2)s, y=%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lin) if 'lin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lin) else 'lin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
                @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
                raise AssertionError(@pytest_ar._format_explanation(@py_format12))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


def test_multikwargs():
    with tf.Graph().as_default():
        x = tf.placeholder((tf.int32), (), name='x')
        with tf.variable_scope('other'):
            x2 = tf.placeholder((tf.int32), (), name='x')
        z = 3 * x + 2 * x2
        lin = function([x, x2], z, givens={x2: 0})
        with single_threaded_session():
            initialize()
            @py_assert1 = 2
            @py_assert3 = lin(@py_assert1)
            @py_assert6 = 6
            @py_assert5 = @py_assert3 == @py_assert6
            if @py_assert5 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_tf_util.py', lineno=36)
            if not @py_assert5:
                @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(lin) if 'lin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lin) else 'lin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
                @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
                raise AssertionError(@pytest_ar._format_explanation(@py_format10))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
            @py_assert1 = 2
            @py_assert3 = 2
            @py_assert5 = lin(@py_assert1, @py_assert3)
            @py_assert8 = 10
            @py_assert7 = @py_assert5 == @py_assert8
            if @py_assert7 is None:
                from _pytest.warning_types import PytestAssertRewriteWarning
                from warnings import warn_explicit
                warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/tests/test_tf_util.py', lineno=37)
            if not @py_assert7:
                @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py0)s(%(py2)s, %(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(lin) if 'lin' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lin) else 'lin',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
                @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
                raise AssertionError(@pytest_ar._format_explanation(@py_format12))
            @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None


if __name__ == '__main__':
    test_function()
    test_multikwargs()