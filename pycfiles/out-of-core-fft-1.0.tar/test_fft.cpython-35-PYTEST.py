# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyle/Research/Code/out_of_core_fft/tests/test_fft.py
# Compiled at: 2016-01-27 06:32:57
# Size of source mod 2**32: 5114 bytes
from __future__ import division, print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os.path, pytest, numpy as np, h5py, out_of_core_fft
oneGB_complex = 67108864
oneMB_complex = 65536

@pytest.mark.parametrize('N', [
 oneMB_complex * 2,
 oneGB_complex * 2])
def test_transpose(N):
    print()
    with out_of_core_fft._TemporaryDirectory() as (temp_dir):
        np.random.seed(1234)
        N_creation = min(16777216, N)
        print('\tCreating file with test data, N={0}'.format(N))
        with h5py.File(os.path.join(temp_dir, 'test_in.h5'), 'w') as (f):
            x = f.create_dataset('x', shape=(N,), dtype=complex)
            for k in range(0, N, N_creation):
                size = min(N - k, N_creation)
                x[k:k + size] = np.random.random(size) + complex(0.0, 1.0) * np.random.random(size)

        print('\t\tFinished creating file with test data')
        print('\tPerforming first transpose')
        with h5py.File(os.path.join(temp_dir, 'test_in.h5'), 'r') as (f):
            x = f['x']
            R2, C2 = N // 1024, 1024
            f2, d = out_of_core_fft.transpose(x, os.path.join(temp_dir, 'test_transpose.h5'), 'x', R2=R2, C2=C2, show_progress=True)
            f2.close()
        print('\t\tFinished performing first transpose')
        print('\tPerforming second transpose')
        with h5py.File(os.path.join(temp_dir, 'test_transpose.h5'), 'r') as (f):
            x = f['x']
            f2, d = out_of_core_fft.transpose(x, os.path.join(temp_dir, 'test_transpose2.h5'), 'x', show_progress=True)
            try:
                @py_assert1 = np.all
                @py_assert3 = [np.array_equal(x[c2a:c2b, r2a:r2b].T, d[r2a:r2b, c2a:c2b]) for r2a in range(0, R2, min(R2, C2)) for r2b in [min(R2, r2a + min(R2, C2))] for c2a in range(0, C2, min(R2, C2)) for c2b in []]
                @py_assert5 = @py_assert1(@py_assert3)
                if not @py_assert5:
                    @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.all\n}(%(py4)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np', 'py2': @pytest_ar._saferepr(@py_assert1)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert3 = @py_assert5 = None
            finally:
                f2.close()

        print('\t\tFinished performing second transpose')


@pytest.mark.parametrize('myfunc, npfunc', [
 (
  out_of_core_fft.ifft, np.fft.ifft),
 (
  out_of_core_fft.fft, np.fft.fft)])
def test_dft(myfunc, npfunc):
    print()
    with out_of_core_fft._TemporaryDirectory() as (temp_dir):
        np.random.seed(1234)
        N = oneMB_complex * 4
        fname_in = os.path.join(temp_dir, 'test_in.h5')
        fname_out = os.path.join(temp_dir, 'test_out.h5')
        print('\tCreating file with test data, N={0}'.format(N))
        with h5py.File(fname_in, 'w') as (f):
            f.create_dataset('X', data=np.random.random(N) + complex(0.0, 1.0) * np.random.random(N))
        print('\t\tFinished creating file with test data')
        print('\tPerforming out-of-core FFT')
        myfunc(fname_in, 'X', fname_out, 'x', mem_limit=1048576)
        print('\t\tFinished performing out-of-core FFT')
        with h5py.File(fname_in, 'r') as (f_in):
            with h5py.File(fname_out, 'r') as (f_out):
                @py_assert1 = np.allclose
                @py_assert4 = f_in['X']
                @py_assert6 = npfunc(@py_assert4)
                @py_assert8 = f_out['x']
                @py_assert10 = @py_assert1(@py_assert6, @py_assert8)
                if not @py_assert10:
                    @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.allclose\n}(%(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}, %(py9)s)\n}') % {'py9': @pytest_ar._saferepr(@py_assert8), 'py3': @pytest_ar._saferepr(npfunc) if 'npfunc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(npfunc) else 'npfunc', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format12))
                @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None


def test_roundtrip_fft():
    print()
    with out_of_core_fft._TemporaryDirectory() as (temp_dir):
        fname_x = os.path.join(temp_dir, 'x.h5')
        fname_X = os.path.join(temp_dir, 'Xtilde.h5')
        fname_xx = os.path.join(temp_dir, 'xx.h5')
        np.random.seed(1234)
        N = oneGB_complex // 2
        mem_limit = N
        N_creation = min(16777216, N)
        print('\tCreating file with test data, N={0}'.format(N))
        with h5py.File(fname_x, 'w') as (f):
            x = f.create_dataset('x', shape=(N,), dtype=complex)
            for k in range(0, N, N_creation):
                size = min(N - k, N_creation)
                x[k:k + size] = np.random.random(size) + complex(0.0, 1.0) * np.random.random(size)

        print('\t\tFinished creating file with test data')
        print('\tPerforming out-of-core FFT')
        out_of_core_fft.fft(fname_x, 'x', fname_X, 'X', show_progress=True, mem_limit=mem_limit)
        print('\t\tFinished performing out-of-core FFT')
        print('\tPerforming out-of-core inverse FFT')
        out_of_core_fft.ifft(fname_X, 'X', fname_xx, 'xx', show_progress=True, mem_limit=mem_limit)
        print('\t\tFinished performing out-of-core inverse FFT')
        print('\tTesting equality of x and ifft(fft(x))')
        with h5py.File(fname_x, 'r') as (f_in):
            with h5py.File(fname_xx, 'r') as (f_out):
                x = f_in['x']
                xx = f_out['xx']
                step = oneGB_complex // 16
                @py_assert1 = np.all
                @py_assert3 = [np.allclose(x[i_a:i_b], xx[i_a:i_b]) for i_a in range(0, x.shape[0], step) for i_b in [min(x.shape[0], i_a + step)]]
                @py_assert5 = @py_assert1(@py_assert3)
                if not @py_assert5:
                    @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.all\n}(%(py4)s)\n}') % {'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np', 'py2': @pytest_ar._saferepr(@py_assert1)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert1 = @py_assert3 = @py_assert5 = None
        print('\tFinished testing equality')