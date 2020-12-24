# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/folz/DFKI/Hacks/augpy/test/test_blur.py
# Compiled at: 2020-01-07 11:52:25
# Size of source mod 2**32: 2874 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, random, numpy as np, augpy
from _common import TYPES
from _common import safe_cast
N, C, H, W = (7, 11, 57, 138)

def __gaussian_kernel(sigma, ksize, dtype):
    r = ksize // 2
    x = np.arange((-r), (r + 1), dtype=dtype)
    kernel = np.exp(-x ** 2 / (2 * sigma ** 2))
    return kernel / kernel.sum()


def __gaussian_blur_one(im, sigma, max_ksize=None):
    dtype = augpy.to_temp_dtype(im.dtype)
    ksize = max(3, int(sigma * 6.6 - 2.3) | 1)
    ksize = min(max_ksize or ksize, ksize)
    pad = ksize // 2
    c, h, w = im.shape
    im = np.pad(im, [(0, 0), (pad, pad), (pad, pad)], mode='edge')
    temp = im.astype(dtype)
    kernel = __gaussian_kernel(sigma, ksize, dtype)
    for c in range(c):
        for y in range(pad + h + pad):
            temp[(c, y)] = np.convolve((temp[(c, y)]), kernel, mode='same')

        for x in range(pad, w + pad):
            temp[c, :, x] = np.convolve((temp[c, :, x]), kernel, mode='same')

    return safe_cast(temp[:, pad:-pad, pad:-pad], im.dtype)


def __gaussian_blur_all(batch, sigmas, max_ksize):
    blurred = np.empty_like(batch)
    for im, out, sigma in zip(batch, blurred, sigmas):
        out[...] = __gaussian_blur_one(im, sigma, max_ksize)

    return blurred


def test_gaussian_blur():
    for _, ntype in TYPES:
        a = np.random.rand(N, C, H, W).astype(ntype) * 127
        b = augpy.array_to_tensor(a)
        sigmas = np.random.rand(N).astype(np.float32) + 1
        ksize = max(3, int(sigmas.max() * 6.6 - 2.3) | 1)
        sigmas_tensor = augpy.array_to_tensor(sigmas)
        augpy_blur = augpy.gaussian_blur(b, sigmas_tensor, ksize)
        augpy_blur = augpy_blur.numpy()
        reference_blur = __gaussian_blur_all(a, sigmas, ksize)
        augpy.default_stream.synchronize()
        @py_assert1 = np.isclose
        @py_assert5 = @py_assert1(augpy_blur, reference_blur)
        @py_assert7 = @py_assert5.all
        @py_assert9 = @py_assert7()
        if not @py_assert9:
            @py_format11 = (@pytest_ar._format_assertmsg(ntype) + '\n>assert %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(augpy_blur) if 'augpy_blur' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_blur) else 'augpy_blur',  'py4':@pytest_ar._saferepr(reference_blur) if 'reference_blur' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reference_blur) else 'reference_blur',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_gaussian_blur_small_kernel():
    for _, ntype in TYPES:
        a = np.random.rand(N, C, H, W).astype(ntype) * 127
        b = augpy.array_to_tensor(a)
        sigmas = np.random.rand(N).astype(np.float32) * 2 + 1
        sigmas_tensor = augpy.array_to_tensor(sigmas)
        augpy_blur = augpy.gaussian_blur(b, sigmas_tensor, 3)
        augpy_blur = augpy_blur.numpy()
        reference_blur = __gaussian_blur_all(a, sigmas, 3)
        augpy.default_stream.synchronize()
        @py_assert1 = np.isclose
        @py_assert5 = @py_assert1(augpy_blur, reference_blur)
        @py_assert7 = @py_assert5.all
        @py_assert9 = @py_assert7()
        if not @py_assert9:
            @py_format11 = (@pytest_ar._format_assertmsg(ntype) + '\n>assert %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(augpy_blur) if 'augpy_blur' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_blur) else 'augpy_blur',  'py4':@pytest_ar._saferepr(reference_blur) if 'reference_blur' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reference_blur) else 'reference_blur',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_gaussian_blur_single():
    for _, ntype in TYPES:
        a = np.random.rand(C, H, W).astype(ntype) * 127
        b = augpy.array_to_tensor(a)
        sigma = random.random() + 1
        augpy_blur = augpy.gaussian_blur_single(b, sigma)
        augpy_blur = augpy_blur.numpy()
        reference_blur = __gaussian_blur_one(a, sigma)
        augpy.default_stream.synchronize()
        @py_assert1 = np.isclose
        @py_assert5 = @py_assert1(augpy_blur, reference_blur)
        @py_assert7 = @py_assert5.all
        @py_assert9 = @py_assert7()
        if not @py_assert9:
            @py_format11 = (@pytest_ar._format_assertmsg(ntype) + '\n>assert %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.isclose\n}(%(py3)s, %(py4)s)\n}.all\n}()\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(augpy_blur) if 'augpy_blur' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(augpy_blur) else 'augpy_blur',  'py4':@pytest_ar._saferepr(reference_blur) if 'reference_blur' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reference_blur) else 'reference_blur',  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert5 = @py_assert7 = @py_assert9 = None


if __name__ == '__main__':
    test_gaussian_blur()