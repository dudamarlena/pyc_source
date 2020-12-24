# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/warping/warping.py
# Compiled at: 2016-11-29 20:56:28
import time, numpy as np
from _warping import warp2dFast, warp3dFast, _warp2dFastLab, _warp3dFastLab

def warp2dJoint(img, lab, patch_size, rot, shear, scale, stretch):
    """
    Warp image and label data jointly. Non-image labels are ignored i.e. lab must be 3d to be warped

    Parameters
    ----------

    img: array
      Image data
      The array must be 3-dimensional (ch,x,y) and larger/equal the patch size
    lab: array
      Label data (with offsets subtracted)
    patch_size: 2-tuple
      Patch size *excluding* channel for the image: (px, py).
      The warping result of the input image is cropped to this size
    rot: float
      Rotation angle in deg for rotation around z-axis
    shear: float
      Shear angle in deg for shear w.r.t xy-diagonal
    scale: 3-tuple of float
      Scale per axis
    stretch: 4-tuple of float
      Fraction of perspective stretching from the center (where stretching is always 1)
      to the outer border of image per axis. The 4 entry correspond to:

      - X stretching depending on Y
      - Y stretching depending on X

    Returns
    -------

    img, lab: np.ndarrays
      Warped image and labels (cropped to patch_size)

    """
    if len(lab.shape) == 2:
        lab = _warp2dFastLab(lab, patch_size, img.shape[1:], rot, shear, scale, stretch)
    img = warp2dFast(img, patch_size, rot, shear, scale, stretch)
    return (img, lab)


def warp3dJoint(img, lab, patch_size, rot=0, shear=0, scale=(1, 1, 1), stretch=(0, 0, 0, 0), twist=0):
    """
    Warp image and label data jointly. Non-image labels are ignored i.e. lab must be 3d to be warped

    Parameters
    ----------

    img: array
      Image data
      The array must be 4-dimensional (z,ch,x,y) and larger/equal the patch size
    lab: array
      Label data (with offsets subtracted)
    patch_size: 3-tuple
      Patch size *excluding* channel for the image: (pz, px, py).
      The warping result of the input image is cropped to this size
    rot: float
      Rotation angle in deg for rotation around z-axis
    shear: float
      Shear angle in deg for shear w.r.t xy-diagonal
    scale: 3-tuple of float
      Scale per axis
    stretch: 4-tuple of float
      Fraction of perspective stretching from the center (where stretching is always 1)
      to the outer border of image per axis. The 4 entry correspond to:

      - X stretching depending on Y
      - Y stretching depending on X
      - X stretching depending on Z
      - Y stretching depending on Z

    twist: float
      Dependence of the rotation angle on z in deg from center to outer border

    Returns
    -------

    img, lab: np.ndarrays
      Warped image and labels (cropped to patch_size)

    """
    if len(lab.shape) == 3:
        lab = _warp3dFastLab(lab, patch_size, np.array(img.shape)[[0, 2, 3]], rot, shear, scale, stretch, twist)
    img = warp3dFast(img, patch_size, rot, shear, scale, stretch, twist)
    return (img, lab)


def warp3d(img, patch_size, rot=0, shear=0, scale=(1, 1, 1), stretch=(0, 0, 0, 0), twist=0):
    return warp3dFast(img, patch_size, rot, shear, scale, stretch, twist)


def warp3dLab(lab, patch_size, size, rot=0, shear=0, scale=(1, 1, 1), stretch=(0, 0, 0, 0), twist=0):
    return _warp3dFastLab(lab, patch_size, size, rot, shear, scale, stretch, twist)


def getCornerIx(sh):
    """Returns array-indices of corner elements for n-dim shape"""

    def getGrayCode(n, n_dim):
        if n == 0:
            return np.zeros(n_dim, dtype=np.int)
        return np.array([ n // 2 ** i % 2 for i in range(max(n_dim, int(np.ceil(np.log2(n))))) ])

    sh = np.array(sh) - 1
    n_dim = len(sh)
    ix = []
    for i in xrange(2 ** n_dim):
        ix.append(getGrayCode(i, n_dim))

    ix = np.array(ix)
    corners = ix * sh
    return corners


def _warpCorners2d(sh, corners, rot=0, shear=0, scale=(1, 1), stretch=(0, 0), plot=False):
    """
    Create warped coordinates of corners
    """
    rot = rot * np.pi / 180
    shear = shear * np.pi / 180
    scale = np.array(scale)
    scale = 1.0 / scale
    stretch = np.array(stretch)
    corners = corners.astype(np.float).copy()
    x_center_off = float(sh[0]) / 2 - 0.5
    y_center_off = float(sh[1]) / 2 - 0.5
    stretch[0] /= x_center_off
    stretch[1] /= y_center_off
    x = corners[:, 0] - x_center_off
    y = corners[:, 1] - y_center_off
    xt = x * (scale[0] + stretch[0] * y)
    yt = y * (scale[1] + stretch[1] * x)
    u = xt * np.cos(rot - shear) - yt * np.sin(rot + shear) + x_center_off
    v = yt * np.cos(rot + shear) + xt * np.sin(rot - shear) + y_center_off
    if plot:
        coords = np.array([u, v]).T
        coords = coords[[3, 2, 0, 1, 3]]
        plt.figure(figsize=(5, 5))
        plt.scatter(corners[:, 1], corners[:, 0], c='b')
        plt.plot(corners[:, 1], corners[:, 0], 'b:')
        plt.scatter(coords[:, 1], coords[:, 0], c='r', marker='x')
        plt.plot(coords[:, 1], coords[:, 0], c='r')
        plt.axes().set_aspect('equal')
        plt.gca().invert_yaxis()
        plt.grid()
    return np.array([u, v]).T


def _warpCorners3d(sh, corners, rot=0, shear=0, scale=(1, 1, 1), stretch=(0, 0, 0, 0), twist=0):
    """
    Create warped coordinates of corners
    """
    rot = rot * np.pi / 180
    shear = shear * np.pi / 180
    twist = twist * np.pi / 180
    scale = np.array(scale)
    scale = 1.0 / scale
    stretch = np.array(stretch)
    corners = corners.astype(np.float).copy()
    z_center_off = float(sh[0]) / 2 - 0.5
    x_center_off = float(sh[1]) / 2 - 0.5
    y_center_off = float(sh[2]) / 2 - 0.5
    stretch[0] /= x_center_off
    stretch[1] /= y_center_off
    stretch[2] /= z_center_off
    stretch[3] /= z_center_off
    twist /= z_center_off
    z = corners[:, 0] - z_center_off
    x = corners[:, 1] - x_center_off
    y = corners[:, 2] - y_center_off
    w = z * scale[2] + z_center_off
    rot = rot + z * twist
    xt = x * (scale[0] + stretch[0] * y + stretch[2] * z)
    yt = y * (scale[1] + stretch[1] * x + stretch[3] * z)
    u = xt * np.cos(rot - shear) - yt * np.sin(rot + shear) + x_center_off
    v = yt * np.cos(rot + shear) + xt * np.sin(rot - shear) + y_center_off
    return np.array((w, u, v)).T


def getRequiredPatchSize(patch_size, rot, shear, scale, stretch, twist=None):
    """
    Given desired patch size and warping parameters:
    return required size for warping input patch
    """
    patch_size = np.array(patch_size)
    corners = getCornerIx(patch_size)
    if len(patch_size) == 2:
        coords = _warpCorners2d(patch_size, corners, rot, shear, scale, stretch)
    elif len(patch_size) == 3:
        coords = _warpCorners3d(patch_size, corners, rot, shear, scale, stretch, twist)
    eff_size = np.ceil(coords.max(axis=0) - coords.min(axis=0))
    left_exc = np.floor(np.abs(np.minimum(coords.min(axis=0), 0)))
    right_exc = np.ceil(np.maximum(coords.max(axis=0) - patch_size + 1, 0))
    total_exc = np.maximum(left_exc, right_exc)
    req_size = patch_size + 2 * total_exc
    return (
     req_size.astype(np.int), eff_size.astype(np.int), left_exc.astype(np.int))


def getWarpParams(patch_size, amount=1.0, **kwargs):
    """
    To be called from CNNData. Get warping parameters + required warping input patch size.
    """
    if amount > 1:
        print 'WARNING: warpAugment amount > 1 this requires more than 1.4 bigger patches before warping'
    rot_max = 15 * amount
    shear_max = 3 * amount
    scale_max = 1.2 * amount
    stretch_max = 0.1 * amount
    n_dim = len(patch_size)
    if 'scale_max' in kwargs:
        scale_max = kwargs['scale_max']
    shear = shear_max * 2 * (np.random.rand() - 0.5)
    if n_dim == 3:
        twist = rot_max * 2 * (np.random.rand() - 0.5)
        rot = min(rot_max - abs(twist), rot_max * np.random.rand())
        scale = 1 - (scale_max - 1) * np.random.rand()
        scale = (scale, scale, 1)
        stretch = stretch_max * 2 * (np.random.rand(4) - 0.5)
    elif n_dim == 2:
        rot = rot_max * 2 * (np.random.rand() - 0.5)
        scale = 1 - (scale_max - 1) * np.random.rand(2)
        stretch = stretch_max * 2 * (np.random.rand(2) - 0.5)
        twist = None
    if 'rot' in kwargs:
        rot = kwargs['rot']
    if 'shear' in kwargs:
        shear = kwargs['shear']
    if 'scale' in kwargs:
        scale = kwargs['scale']
    if 'stretch' in kwargs:
        stretch = kwargs['stretch']
    if 'twist' in kwargs:
        twist = kwargs['twist']
    req_size, _, _ = getRequiredPatchSize(patch_size, rot, shear, scale, stretch, twist)
    return (
     req_size, rot, shear, scale, stretch, twist)


def test():
    try:
        img_s = np.random.rand(11, 11)
        img_s = np.concatenate((img_s[None], np.exp(img_s[None])), axis=0)
        out = warp2dFast(img_s, (11, 11), 0, 0, (1, 1), (0.0, 0.0))
    except Exception as e:
        print '%s\n        Warping is broken. Most likeley the distributed _warping.so is not binary compatible to your system.' % (e,)

    return


test()

def maketestimage(sh):
    img = np.ones(sh) * 0.5
    xs, ys = sh
    try:
        d = np.diag(np.ones(xs))
        img[:xs, :xs] += d
        img[:xs, :xs] += d[::-1]
        img[-xs:, -xs:] += d
        img[-xs:, -xs:] += d[::-1]
    except:
        d = np.diag(np.ones(ys))
        img[:ys, :ys] += d
        img[:ys, :ys] += d[::-1]
        img[-ys:, -ys:] += d
        img[-ys:, -ys:] += d[::-1]

    img[0, :] += 1
    img[:, 0] += 1
    img[-1, :] += 1
    img[:, -1] += 1
    if sh[0] > 80:
        img[30, :] += 1
        img[:, 30] += 1
        img[-31, :] += 1
        img[:, -31] += 1
    return img / img.max()


if __name__ == '__main__':
    ps = (200, 200)
    if True:
        ext_size, rot, shear, scale, stretch, twist = getWarpParams(ps, amount=1.0)
        t = []
        for i in xrange(10000):
            ext_size, rot, shear, scale, stretch, twist = getWarpParams(ps, amount=1.0)
            t.append(ext_size)

        img_in = maketestimage(ext_size)[None]
        out = warp2dFast(img_in, ps, rot, shear, scale, stretch)
        plt.figure()
        plt.subplot(121)
        plt.imshow(img_in[0], interpolation='none', cmap='gray')
        plt.hlines(ext_size[0] / 2 - 0.5, 0, ext_size[1] - 1, color='r')
        plt.vlines(ext_size[1] / 2 - 0.5, 0, ext_size[0] - 1, color='r')
        plt.subplot(122)
        plt.imshow(out[0], interpolation='none', cmap='gray')
        plt.hlines(ps[0] / 2 - 0.5, 0, ps[1] - 1, color='r')
        plt.vlines(ps[1] / 2 - 0.5, 0, ps[0] - 1, color='r')
    if False:
        test_img = np.concatenate((test_img[None], np.exp(test_img[None])), axis=0)
        out2 = warp2dFast(test_img, (512, 512), 20, 10, (1, 1.1), (0.1, 0))
        plt.figure()
        plt.subplot(121)
        plt.imshow(test_img, interpolation='none', cmap='gray')
        plt.subplot(122)
        plt.imshow(out2[0], interpolation='none', cmap='gray')
    if False:
        img_s = maketestimage((11, 11))
        img_s = np.concatenate((img_s[None], np.exp(img_s[None])), axis=0)
        out = warp2dFast(img_s, (11, 11), 0, 0, (1, 1), (0.0, 0.0))
    if False:
        img_s = maketestimage((110, 110))
        img_s = np.concatenate((img_s[None],) * 4, axis=0)
        img_s = np.concatenate((img_s[None], np.exp(img_s[None])), axis=0)
        out = warp3dFast(img_s, (4, 110, 110), 0, 0, (1, 1, 1), (0.0, 0.0, 0.0, 0.0), 10)
    if False:
        n = 100
        img_s = np.tile(test_img, n)
        img_s = img_s.reshape((s1, n, s2))
        img_s = np.swapaxes(img_s, 1, 0)
        patch_size = img_s.shape
        off = 0
        lab = img_s[off:-off, off:-off, off:-off]
        img = np.concatenate((test_img[None], np.exp(test_img[None])), axis=0)
        img1, lab1 = warpAugment(img_s[None], lab, patch_size=patch_size)
        for i in xrange(n):
            plt.imsave('/tmp/%i-img.png' % i, img1[0, i, :, :] / 255)

        for i in xrange(lab1.shape[0]):
            plt.imsave('/tmp/%i-lab.png' % (i + off), lab1[i, :, :])

    if False:
        n = 40
        img_s = np.tile(test_img, n)
        img_s = img_s.reshape((s1, n, s2))
        img_s = np.swapaxes(img_s, 1, 2)
        wow1 = warp3dFast(img_s[None], (s1, s2, n), 0, 0, (1, 1, 1), (0.1, 0.1, 0.1,
                                                                      -0.1), 10)
        for i in xrange(n):
            plt.imsave('/tmp/%i-ref.png' % i, wow1[:, :, i] / 255)

        wow2 = _warp3dFastLab(img_s[20:-20, 20:-20], (s1 - 40, s2 - 40, n), (
         s1, s2, n), 0, 0, (1, 1, 1), (0.1, 0.1, 0.1, -0.1), 10)
        for i in xrange(wow2.shape[2]):
            plt.imsave('/tmp/%i.png' % i, wow2[:, :, i] / 255)

    if False:
        s = 400
        test = np.random.rand(s, s, s).astype(np.float32)
        test2 = np.random.rand(s * 2, s * 2, s * 2).astype(np.float32)
        t0 = time.time()
        wow1 = warp3dFast(test[None], (s, s, s), 20, 5, (1, 1, 1), (0.1, 0.1, 0.1,
                                                                    0.1), 10)
        print time.time() - t0