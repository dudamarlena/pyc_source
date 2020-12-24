# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/folz/DFKI/Hacks/augpy/test/test_tensor.py
# Compiled at: 2020-01-24 11:34:18
# Size of source mod 2**32: 2483 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np, pytest, augpy
N, C, H, W = (16, 3, 56, 57)
I_TYPES = [
 (
  augpy.uint8, np.uint8),
 (
  augpy.int8, np.int8),
 (
  augpy.int16, np.int16),
 (
  augpy.uint16, np.uint16),
 (
  augpy.int32, np.int32),
 (
  augpy.uint32, np.uint32),
 (
  augpy.int64, np.int64),
 (
  augpy.uint64, np.uint64)]
F_TYPES = [
 (
  augpy.float32, np.float32),
 (
  augpy.float64, np.float64)]
TYPES = I_TYPES + F_TYPES

def test_index_operator_slice():
    a = np.arange(100).reshape((10, 10))
    b = augpy.array_to_tensor(a)
    numpy_slice = a[0]
    result = b[0].numpy()
    augpy.default_stream.synchronize()
    print(result)
    @py_assert1 = numpy_slice == result
    @py_assert5 = @py_assert1.all
    @py_assert7 = @py_assert5()
    if not @py_assert7:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (numpy_slice, result)) % {'py0':@pytest_ar._saferepr(numpy_slice) if 'numpy_slice' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_slice) else 'numpy_slice',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}' % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_index_operator_slice_middle():
    a = np.arange(100).reshape((10, 10))
    b = augpy.array_to_tensor(a)
    numpy_slice = a[4:6]
    result = b[4:6].numpy()
    augpy.default_stream.synchronize()
    print(result)
    print(numpy_slice)
    @py_assert1 = numpy_slice == result
    @py_assert5 = @py_assert1.all
    @py_assert7 = @py_assert5()
    if not @py_assert7:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (numpy_slice, result)) % {'py0':@pytest_ar._saferepr(numpy_slice) if 'numpy_slice' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_slice) else 'numpy_slice',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}' % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_index_scalar_exception():
    scalar = 1337.0
    numpy_scalar = np.asarray(scalar)
    augpy_scalar = augpy.array_to_tensor(numpy_scalar)
    with pytest.raises(IndexError) as (excinfo):
        augpy_scalar[0]


def test_types():
    @py_assert1 = augpy.float16
    @py_assert3 = @py_assert1.bits
    @py_assert6 = 16
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.float16\n}.bits\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(augpy) if 'augpy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy) else 'augpy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = augpy.float32
    @py_assert3 = @py_assert1.bits
    @py_assert6 = 32
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.float32\n}.bits\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(augpy) if 'augpy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy) else 'augpy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = augpy.float64
    @py_assert3 = @py_assert1.bits
    @py_assert6 = 64
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.float64\n}.bits\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(augpy) if 'augpy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy) else 'augpy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = augpy.int8
    @py_assert3 = @py_assert1.bits
    @py_assert6 = 8
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.int8\n}.bits\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(augpy) if 'augpy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy) else 'augpy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = augpy.uint8
    @py_assert3 = @py_assert1.bits
    @py_assert6 = 8
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.uint8\n}.bits\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(augpy) if 'augpy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy) else 'augpy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = augpy.int16
    @py_assert3 = @py_assert1.bits
    @py_assert6 = 16
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.int16\n}.bits\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(augpy) if 'augpy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy) else 'augpy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = augpy.uint16
    @py_assert3 = @py_assert1.bits
    @py_assert6 = 16
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.uint16\n}.bits\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(augpy) if 'augpy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy) else 'augpy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = augpy.int32
    @py_assert3 = @py_assert1.bits
    @py_assert6 = 32
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.int32\n}.bits\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(augpy) if 'augpy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy) else 'augpy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = augpy.uint32
    @py_assert3 = @py_assert1.bits
    @py_assert6 = 32
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.uint32\n}.bits\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(augpy) if 'augpy' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy) else 'augpy',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_numpy_function_noncontiguous():
    a = np.arange(100).reshape((10, 10))
    b = augpy.array_to_tensor(a)
    numpy_result = a[::2]
    augpy_result = b[::2].numpy()
    augpy.default_stream.synchronize()
    @py_assert1 = numpy_result == augpy_result
    @py_assert5 = @py_assert1.all
    @py_assert7 = @py_assert5()
    if not @py_assert7:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (numpy_result, augpy_result)) % {'py0':@pytest_ar._saferepr(numpy_result) if 'numpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(numpy_result) else 'numpy_result',  'py2':@pytest_ar._saferepr(augpy_result) if 'augpy_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_result) else 'augpy_result'}
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}' % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert5 = @py_assert7 = None


def test_gamma():
    a = np.random.rand(N, C, H, W)
    b = augpy.array_to_tensor(a)
    gamma_grays = augpy.array_to_tensor(np.random.rand(N)) + 0.25
    gamma_colors = augpy.array_to_tensor(np.random.rand(N, C)) + 0.25
    contrasts = augpy.array_to_tensor(np.random.rand(N, C)) + 0.2
    result = augpy.add_gamma(b, gamma_grays, gamma_colors, contrasts, float(1.0))
    result = result.numpy()
    augpy.default_stream.synchronize()
    @py_assert1 = a == result
    @py_assert5 = @py_assert1.all
    @py_assert7 = @py_assert5()
    @py_assert9 = not @py_assert7
    if not @py_assert9:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (a, result)) % {'py0':@pytest_ar._saferepr(a) if 'a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a) else 'a',  'py2':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.all\n}()\n}' % {'py4':@py_format3,  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None