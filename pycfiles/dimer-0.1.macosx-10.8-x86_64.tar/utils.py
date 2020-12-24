# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/nnet/utils.py
# Compiled at: 2013-06-28 01:46:47
""" This file contains different utility functions that are not connected
in anyway to the networks presented in the tutorials, but rather help in
processing the outputs into a more understandable way.

For example ``tile_raster_images`` helps in generating a easy to grasp
image from a set of samples or weights.
"""
import numpy

def scale_to_unit_interval(ndar, eps=1e-08):
    """ Scales all values in the ndarray ndar to be between 0 and 1 """
    ndar = ndar.copy()
    ndar -= ndar.min()
    ndar *= 1.0 / (ndar.max() + eps)
    return ndar


def tile_raster_images(X, img_shape, tile_shape, tile_spacing=(0, 0), scale_rows_to_unit_interval=True, output_pixel_vals=True):
    """
    Transform an array with one flattened image per row, into an array in
    which images are reshaped and layed out like tiles on a floor.

    This function is useful for visualizing datasets whose rows are images,
    and also columns of matrices for transforming those rows
    (such as the first layer of a neural net).

    :type X: a 2-D ndarray or a tuple of 4 channels, elements of which can
    be 2-D ndarrays or None;
    :param X: a 2-D array in which every row is a flattened image.

    :type img_shape: tuple; (height, width)
    :param img_shape: the original shape of each image

    :type tile_shape: tuple; (rows, cols)
    :param tile_shape: the number of images to tile (rows, cols)

    :param output_pixel_vals: if output should be pixel values (i.e. int8
    values) or floats

    :param scale_rows_to_unit_interval: if the values need to be scaled before
    being plotted to [0,1] or not

    :returns: array suitable for viewing as an image.
    (See:`PIL.Image.fromarray`.)
    :rtype: a 2-d array with same dtype as X.

    """
    assert len(img_shape) == 2
    assert len(tile_shape) == 2
    assert len(tile_spacing) == 2
    out_shape = [ (ishp + tsp) * tshp - tsp for ishp, tshp, tsp in zip(img_shape, tile_shape, tile_spacing)
                ]
    if isinstance(X, tuple):
        assert len(X) == 4
        if output_pixel_vals:
            out_array = numpy.zeros((out_shape[0], out_shape[1], 4), dtype='uint8')
        else:
            out_array = numpy.zeros((out_shape[0], out_shape[1], 4), dtype=X.dtype)
        if output_pixel_vals:
            channel_defaults = [
             0, 0, 0, 255]
        else:
            channel_defaults = [
             0.0, 0.0, 0.0, 1.0]
        for i in xrange(4):
            if X[i] is None:
                dt = out_array.dtype
                if output_pixel_vals:
                    dt = 'uint8'
                out_array[:, :, i] = numpy.zeros(out_shape, dtype=dt) + channel_defaults[i]
            else:
                out_array[:, :, i] = tile_raster_images(X[i], img_shape, tile_shape, tile_spacing, scale_rows_to_unit_interval, output_pixel_vals)

        return out_array
    H, W = img_shape
    Hs, Ws = tile_spacing
    dt = X.dtype
    if output_pixel_vals:
        dt = 'uint8'
    out_array = numpy.zeros(out_shape, dtype=dt)
    for tile_row in xrange(tile_shape[0]):
        for tile_col in xrange(tile_shape[1]):
            if tile_row * tile_shape[1] + tile_col < X.shape[0]:
                this_x = X[(tile_row * tile_shape[1] + tile_col)]
                if scale_rows_to_unit_interval:
                    this_img = scale_to_unit_interval(this_x.reshape(img_shape))
                else:
                    this_img = this_x.reshape(img_shape)
                c = 1
                if output_pixel_vals:
                    c = 255
                out_array[tile_row * (H + Hs):tile_row * (H + Hs) + H, tile_col * (W + Ws):tile_col * (W + Ws) + W] = this_img * c

    return out_array
    return


def cnn_filters2raster_image(X):
    K, I, H, W = X.shape
    return numpy.swapaxes(X, 0, 1).reshape((I, K, -1)).reshape(I * K, -1)