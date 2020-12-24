# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/test_inplacepickle.py
# Compiled at: 2018-02-25 01:12:57
# Size of source mod 2**32: 527 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pickle

class InPlaceByteWriter:

    def __init__(self, memory, loc=0):
        self.memory = memory
        self.loc = loc

    def write(self, bytes):
        n_bytes = len(bytes)
        next_loc = self.loc + n_bytes
        self.memory[self.loc:next_loc] = bytes
        self.loc = next_loc


def test_inplace():
    m = bytearray(13)
    bw = InPlaceByteWriter(memoryview(m))
    pickle.dump('abc', bw)
    @py_assert3 = pickle.dumps
    @py_assert5 = 'abc'
    @py_assert7 = @py_assert3(@py_assert5)
    @py_assert1 = m == @py_assert7
    if not @py_assert1:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s.dumps\n}(%(py6)s)\n}', ), (m, @py_assert7)) % {'py0':@pytest_ar._saferepr(m) if 'm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(m) else 'm',  'py2':@pytest_ar._saferepr(pickle) if 'pickle' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pickle) else 'pickle',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None