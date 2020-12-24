# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /softdev/akuurstr/python/modules/vidi3d/vidi3d/Examples/simulation.py
# Compiled at: 2017-05-17 11:20:51
"""
The following module for phantom generation was taken from ismrmrd-python-tools:
https://github.com/ismrmrd/ismrmrd-python-tools
"""
import numpy as np

def sample_data(img_obj, csm, acc=1, ref=0, sshift=0):
    sshift = sshift % acc
    assert img_obj.ndim == 2, 'Only two dimensional objects supported at the moment'
    assert csm.ndim == 3, 'csm must be a 3 dimensional array'
    assert img_obj.shape[0] == csm.shape[1], 'Object and csm dimension mismatch'
    assert img_obj.shape[1] == csm.shape[2], 'Object and csm dimension mismatch'
    pat_img = np.zeros(img_obj.shape, dtype=np.int8)
    pat_img[sshift:-1:acc, :] = 1
    pat_ref = np.zeros(img_obj.shape, dtype=np.int8)
    if ref > 0:
        pat_ref[0 + img_obj.shape[0] / 2:ref + img_obj.shape[0] / 2, :] = 2
    pat = pat_img + pat_ref
    coil_images = np.tile(img_obj, (csm.shape[0], 1, 1)) * csm
    data = transform.transform_image_to_kspace(coil_images, dim=(1, 2))
    data = data * (np.tile(pat, (csm.shape[0], 1, 1)) > 0).astype('float32')
    return (data, pat)


def generate_birdcage_sensitivities(matrix_size=256, number_of_coils=8, relative_radius=1.5, normalize=True):
    """ Generates birdcage coil sensitivites.
    :param matrix_size: size of imaging matrix in pixels (default ``256``)
    :param number_of_coils: Number of simulated coils (default ``8``)
    :param relative_radius: Relative radius of birdcage (default ``1.5``)
    This function is heavily inspired by the mri_birdcage.m Matlab script in
    Jeff Fessler's IRT package: http://web.eecs.umich.edu/~fessler/code/
    """
    out = np.zeros((number_of_coils, matrix_size,
     matrix_size), dtype=np.complex64)
    for c in range(0, number_of_coils):
        coilx = relative_radius * np.cos(c * (2 * np.pi / number_of_coils))
        coily = relative_radius * np.sin(c * (2 * np.pi / number_of_coils))
        coil_phase = -c * (2 * np.pi / number_of_coils)
        for y in range(0, matrix_size):
            y_co = float(y - matrix_size / 2) / float(matrix_size / 2) - coily
            for x in range(0, matrix_size):
                x_co = float(x - matrix_size / 2) / float(matrix_size / 2) - coilx
                rr = np.sqrt(x_co ** 2 + y_co ** 2)
                phi = np.arctan2(x_co, -y_co) + coil_phase
                out[(c, y, x)] = 1 / rr * np.exp(complex(0.0, 1.0) * phi)

    if normalize:
        rss = np.squeeze(np.sqrt(np.sum(abs(out) ** 2, 0)))
        out = out / np.tile(rss, (number_of_coils, 1, 1))
    return out


def phantom(matrix_size=256, phantom_type='Modified Shepp-Logan', ellipses=None):
    """
    Create a Shepp-Logan or modified Shepp-Logan phantom::
        phantom (n = 256, phantom_type = 'Modified Shepp-Logan', ellipses = None)
    :param matrix_size: size of imaging matrix in pixels (default 256)
    :param phantom_type: The type of phantom to produce.
        Either "Modified Shepp-Logan" or "Shepp-Logan". This is overridden
        if ``ellipses`` is also specified.
    :param ellipses: Custom set of ellipses to use.  These should be in
        the form::
            [[I, a, b, x0, y0, phi],
            [I, a, b, x0, y0, phi],
                            ...]
        where each row defines an ellipse.
        :I: Additive intensity of the ellipse.
        :a: Length of the major axis.
        :b: Length of the minor axis.
        :x0: Horizontal offset of the centre of the ellipse.
        :y0: Vertical offset of the centre of the ellipse.
        :phi: Counterclockwise rotation of the ellipse in degrees,
            measured as the angle between the horizontal axis and
            the ellipse major axis.
    The image bounding box in the algorithm is ``[-1, -1], [1, 1]``,
    so the values of ``a``, ``b``, ``x0``, ``y0`` should all be specified with
    respect to this box.
    :returns: Phantom image
    References:
    Shepp, L. A.; Logan, B. F.; Reconstructing Interior Head Tissue
    from X-Ray Transmissions, IEEE Transactions on Nuclear Science,
    Feb. 1974, p. 232.
    Toft, P.; "The Radon Transform - Theory and Implementation",
    Ph.D. thesis, Department of Mathematical Modelling, Technical
    University of Denmark, June 1996.
    """
    if ellipses is None:
        ellipses = _select_phantom(phantom_type)
    else:
        if np.size(ellipses, 1) != 6:
            raise AssertionError('Wrong number of columns in user phantom')
        ph = np.zeros((matrix_size, matrix_size), dtype=np.float32)
        ygrid, xgrid = np.mgrid[-1:1:complex(0.0, 1.0) * matrix_size, -1:1:complex(0.0, 1.0) * matrix_size]
        for ellip in ellipses:
            I = ellip[0]
            a2 = ellip[1] ** 2
            b2 = ellip[2] ** 2
            x0 = ellip[3]
            y0 = ellip[4]
            phi = ellip[5] * np.pi / 180
            x = xgrid - x0
            y = ygrid - y0
            cos_p = np.cos(phi)
            sin_p = np.sin(phi)
            locs = (x * cos_p + y * sin_p) ** 2 / a2 + (y * cos_p - x * sin_p) ** 2 / b2 <= 1
            ph[locs] += I

    return ph


def _select_phantom(name):
    if name.lower() == 'shepp-logan':
        e = _shepp_logan()
    elif name.lower() == 'modified shepp-logan':
        e = _mod_shepp_logan()
    else:
        raise ValueError('Unknown phantom type: %s' % name)
    return e


def _shepp_logan():
    return [
     [
      2, 0.69, 0.92, 0, 0, 0],
     [
      -0.98, 0.6624, 0.874, 0, -0.0184, 0],
     [
      -0.02, 0.11, 0.31, 0.22, 0, -18],
     [
      -0.02, 0.16, 0.41, -0.22, 0, 18],
     [
      0.01, 0.21, 0.25, 0, 0.35, 0],
     [
      0.01, 0.046, 0.046, 0, 0.1, 0],
     [
      0.02, 0.046, 0.046, 0, -0.1, 0],
     [
      0.01, 0.046, 0.023, -0.08, -0.605, 0],
     [
      0.01, 0.023, 0.023, 0, -0.606, 0],
     [
      0.01, 0.023, 0.046, 0.06, -0.605, 0]]


def _mod_shepp_logan():
    return [
     [
      1, 0.69, 0.92, 0, 0, 0],
     [
      -0.8, 0.6624, 0.874, 0, -0.0184, 0],
     [
      -0.2, 0.11, 0.31, 0.22, 0, -18],
     [
      -0.2, 0.16, 0.41, -0.22, 0, 18],
     [
      0.1, 0.21, 0.25, 0, 0.35, 0],
     [
      0.1, 0.046, 0.046, 0, 0.1, 0],
     [
      0.1, 0.046, 0.046, 0, -0.1, 0],
     [
      0.1, 0.046, 0.023, -0.08, -0.605, 0],
     [
      0.1, 0.023, 0.023, 0, -0.606, 0],
     [
      0.1, 0.023, 0.046, 0.06, -0.605, 0]]