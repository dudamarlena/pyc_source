# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/islatu/image.py
# Compiled at: 2020-04-21 09:19:16
# Size of source mod 2**32: 6770 bytes
"""
The two-dimension detector generates images of the reflected
intensity. 
The purpose of this class is the investigation and manipulation
of these images.
"""
import os, numpy as np
from matplotlib.pyplot import imshow
from PIL import Image as PILIm
from uncertainties import unumpy as unp

class Image:
    __doc__ = '\n    This class stores information about the detector images.\n\n    Attributes:\n        file_path (str): File path for the image.\n        data (pd.DataFrame): Experimental data about the measurement.\n        metadata (dict): Metadata regarding the measurement.\n        array (array_like): The image described as an array.\n        bkg (uncertainties.cores.Variable): The background that was\n            subtracted from the image.\n        n_pixels (float): The width of the peak in number of pixels, used\n            to calculate an uncertainty in q on the detector.\n\n    Args:\n        file_path (str): The file path for the image.\n        data (pd.DataFrame, optional): Experimental data about the\n            measurement. Defaults to ``None``.\n        metadata (dict, optional): Metadata regarding the measurement.\n            Defaults to ``None``.\n        transpose (bool, optional): Should the data be rotated by 90 degrees?\n            Defaults to ``False``.\n        hot_pixel_threshold (int, optional): The number of counts above\n            which a pixel should be assessed to determine if it is hot.\n            Defaults to ``200000``.\n    '

    def __init__(self, file_path, data=None, metadata=None, transpose=False, hot_pixel_threshold=200000):
        """
        Initialisation of the Image class, includes running hot pixel
        check and assigning uncertainties.
        """
        self.file_path = file_path
        self.data = data
        self.metadata = metadata
        img = PILIm.open(file_path)
        array = np.array(img)
        img.close()
        if transpose:
            array = array.T
        array = _find_hot_pixels(array, threshold=hot_pixel_threshold)
        array[np.where(array > 500000)] = 0
        array[np.where(array < 0)] = 0
        array_error = np.sqrt(array)
        array_error[np.where(array == 0)] = 1
        self.array = unp.uarray(array, array_error)
        self.bkg = 0
        self.n_pixel = 0

    @property
    def nominal_values(self):
        """
        Get the nominal values of the image array.

        Returns:
            (np.ndarray): Nominal values of image.
        """
        return unp.nominal_values(self.array)

    @property
    def std_devs(self):
        """
        Get the standard deviation values of the image array.

        Returns:
            (np.ndarray): Standard deviation values of image.
        """
        return unp.std_devs(self.array)

    @property
    def n(self):
        """
        Get the nominal values of the image array.

        Returns:
            (np.ndarray): Nominal values of image.
        """
        return unp.nominal_values(self.array)

    @property
    def s(self):
        """
        Get the standard deviation values of the image array.

        Returns:
            (np.ndarray): Standard deviation values of image.
        """
        return unp.std_devs(self.array)

    @property
    def shape(self):
        """
        Array shape

        Returns:
            (tuple_of_int): The shape of the image.
        """
        return unp.nominal_values(self.array).shape

    def show(self):
        """
        Show the image.

        Return:
            (mpl.Figure): Matplotlib imshow of array.
        """
        return im.show(self.n)

    def __repr__(self):
        """
        Custom representation.

        Returns:
            (np.ndarray): Image array.
        """
        return self.array

    def __str__(self):
        """
        Custom string.

        Returns:
            (np.ndarray): Image array.
        """
        return self.array

    def crop(self, crop_function, **kwargs):
        """
        Perform an image crop based on some function.

        Args:
            crop_function (callable): The function to crop the data.
            **kwargs (dict): The function keyword arguments.
        """
        self.array = (unp.uarray)(*crop_function((self.n), (self.s), **kwargs))

    def background_subtraction(self, background_subtraction_function, **kwargs):
        """
        Perform a background subtraction based on some function.

        Args:
            background_subtraction_function (callable): The function to model
                the data and therefore remove the background.
            **kwargs (dict): The function keyword arguments.
        """
        bkg_popt, bkg_idx, pixel_idx = background_subtraction_function(
         (self.n), (self.s), **kwargs)
        self.bkg = bkg_popt[bkg_idx]
        self.n_pixel = bkg_popt[pixel_idx]
        self.array -= self.bkg

    def sum(self, axis=None):
        """
        Perform a summation on the image

        Args:
            axis (int, optional): The axis of the array to perform the
                summation over.
        """
        return self.array.sum(axis)


def _find_hot_pixels(array, threshold=200000):
    """
    Find some dead pixels and assign them with some local average value.

    Args:
        array (np.ndarray): NumPy array describing the image.
        threshold (int, optional): The number of counts above which a pixel
            should be assessed to determine if it is hot. Defaults to
            ``200000``.

    Returns:
        (np.ndarray): NumPy array where hot pixels have been removed.
    """
    sorted_array = np.sort(array.flatten())[::-1]
    for i in sorted_array:
        if i >= threshold:
            pos_a, pos_b = np.where(array == i)
            lower_a = pos_a[0] - 1
            upper_a = pos_a[0] + 2
            lower_b = pos_b[0] - 1
            upper_b = pos_b[0] + 2
            if pos_a[0] == 0:
                lower_a = 0
            else:
                if pos_a[0] == array.shape[0] - 1:
                    upper_a = array.shape[0]
                elif pos_b[0] == 0:
                    lower_b = 0
                else:
                    if pos_b[0] == array.shape[1] - 1:
                        upper_b = array.shape[1]
            local = np.copy(array[lower_a:upper_a, lower_b:upper_b])
            local[np.where(local == i)] = 0
            local_average = np.mean(local)
            local_std = np.std(local)
            if i > local_average + 2 * local_std:
                array[(pos_a[0], pos_b[0])] = local_average
        else:
            break

    return array