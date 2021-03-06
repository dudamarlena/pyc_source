# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dafne/SalientRegions/SalientDetector-python/salientregions/detectors.py
# Compiled at: 2016-07-14 09:13:36
"""
Salient regions detectors.
"""
from __future__ import absolute_import
from abc import ABCMeta, abstractmethod
import cv2
from . import helpers
from . import binarization
import numpy as np
from .binarydetector import BinaryDetector
import six
from six.moves import range

class Detector(six.with_metaclass(ABCMeta, object)):
    """
    Abstract class for salient region detectors.

    Parameters
    ------
    SE_size_factor: float, optional
        The fraction of the image size that the structuring element should be
    lam_factor : float, optional
        The factor of lambda compared to the SE size
    area_factor: float, optional
        factor that describes the minimum area of a significent CC
    connectivity: int
        What connectivity to use to define CCs

    """

    def __init__(self, SE_size_factor=0.15, lam_factor=5, area_factor=0.05, connectivity=4):
        self.SE_size_factor = SE_size_factor
        self.lam_factor = lam_factor
        self.area_factor = area_factor
        self.connectivity = connectivity

    @abstractmethod
    def detect(self, img):
        """This method should be implemented to return a
        dictionary with the salientregions.
        Calling this function from the superclass makes sure the
        structuring element and lamda are created.

        Parameters
        ------
        img: numpy arrary
            grayscale or color image to detect regions
        """
        nrows, ncols = img.shape[0], img.shape[1]
        self.get_SE(nrows * ncols)

    def get_SE(self, imgsize):
        """Get the structuring element en minimum salient region area for this image.
        The standard type of binarization is Datadriven (as in DMSR),
        but it is possible to pass a different Binarizer.

        Parameters
        ------
        imgsize: int
            size (nr of pixels) of the image

        Returns
        ------
        SE: numpy array
            The structuring element for this image
        lam: float
            lambda, minimumm area of a salient region
        """
        SE_size = int(np.floor(self.SE_size_factor * np.sqrt(imgsize / np.pi)))
        SE_dim_size = SE_size * 2 - 1
        self.SE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (
         SE_dim_size, SE_dim_size))
        self.lam = self.lam_factor * SE_size
        return (self.SE, self.lam)


class SalientDetector(Detector):
    """Find salient regions of all four types, in color or greyscale images.
    The image is first binarized using the specified binarizer,
    then a binary detector is used.

    Parameters
    ------
    binarizer: Binerizer object, optional
        Binerizer object that handles the binarization.
        By default, we use datadriven binarization
    **kwargs
        Other arguments to pass along to the constructor of the superclass Detector

    Attributes
    ------
    gray : numpy array
        The image converted to grayscale
    binarized : numpy array
        The binarized image
    """

    def __init__(self, binarizer=None, **kwargs):
        super(SalientDetector, self).__init__(**kwargs)
        self.binarizer = binarizer
        self.gray = None
        self.binarized = None
        return

    def detect(self, img, find_holes=True, find_islands=True, find_indentations=True, find_protrusions=True, visualize=True):
        """Find salient regions of the types specified.

        Parameters
        ------
        img: numpy arrary
            grayscale or color image to detect regions
        find_holes: bool, optional
            Whether to detect regions of type hole
        find_islands: bool, optional
            Whether to detect regions of type island
        find_indentations: bool, optional
            Whether to detect regions of type indentation
        find_protrusions: bool, optional
            Whether to detect regions of type protrusion
        visualize: bool, optional
            Option for visualizing the process

        Returns
        ------
        regions: dict
            For each type of region, the maks with detected regions.
        """
        super(SalientDetector, self).detect(img)
        if self.binarizer is None:
            self.binarizer = binarization.DatadrivenBinarizer(lam=self.lam, connectivity=self.connectivity)
        if len(img.shape) == 3:
            self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            self.gray = img.copy()
        self.binarized = self.binarizer.binarize(self.gray, visualize)
        bindetector = BinaryDetector(SE=self.SE, lam=self.lam, area_factor=self.area_factor, connectivity=self.connectivity)
        result = bindetector.detect(self.binarized, find_holes, find_islands, find_indentations, find_protrusions, visualize)
        if visualize:
            helpers.visualize_elements(self.gray, holes=result.get('holes', None), islands=result.get('islands', None), indentations=result.get('indentations', None), protrusions=result.get('protrusions', None), title='Salient Regions visualized in grayscale image')
        return result


class MSSRDetector(Detector):
    """Find salient regions of all four types, in color or greyscale images.
    It uses MSSR, meaning that it detects on a series of threshold levels.

    Parameters
    ------
    min_thres: int, optional
        Minimum threshold level
    max_thres: int, optional
        Maximum threshold level
    step: int, optional
        Stepsize for looping through threshold levels
    perc: float, optional
        The percentile at which the threshold is taken
    **kwargs
        Other arguments to pass along to the constructor of the superclass `Detector`

    Attributes
    ------
    gray : numpy array
        The image converted to grayscale
    regions_sum : numpy array
        The sum of the regions of all levels, before thresholding

    Note
    ------
    This algorithm is much slower than the DMSR, so should be used with care.
    """

    def __init__(self, min_thres=0, max_thres=255, step=1, perc=0.7, **kwargs):
        super(MSSRDetector, self).__init__(**kwargs)
        self.min_thres = min_thres
        self.max_thres = max_thres
        self.step = step
        self.perc = perc
        self.gray = None
        self.regions_sum = None
        return

    def detect(self, img, find_holes=True, find_islands=True, find_indentations=True, find_protrusions=True, visualize=True):
        """Find salient regions of the types specified.

        Parameters
        ------
        img: numpy arrary
            grayscale or color image to detect regions
        find_holes: bool, optional
            Whether to detect regions of type hole
        find_islands: bool, optional
            Whether to detect regions of type island
        find_indentations: bool, optional
            Whether to detect regions of type indentation
        find_protrusions: bool, optional
            Whether to detect regions of type protrusion
        visualize: bool, optional
            Option for visualizing the process

        Returns
        ------
        regions: dict
            For each type of region, the maks with detected regions.
        """
        super(MSSRDetector, self).detect(img)
        if len(img.shape) == 3:
            self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            self.gray = img.copy()
        bindetector = BinaryDetector(SE=self.SE, lam=self.lam, area_factor=self.area_factor, connectivity=self.connectivity)
        result = {}
        if find_holes:
            result['holes'] = np.zeros(self.gray.shape, dtype='uint8')
        if find_islands:
            result['islands'] = np.zeros(self.gray.shape, dtype='uint8')
        if find_indentations:
            result['indentations'] = np.zeros(self.gray.shape, dtype='uint8')
        if find_protrusions:
            result['protrusions'] = np.zeros(self.gray.shape, dtype='uint8')
        previmg = np.zeros_like(self.gray, dtype='uint8')
        regions = result.copy()
        for t in range(self.min_thres, self.max_thres + 1, self.step):
            _, bint = cv2.threshold(self.gray, t, 255, cv2.THRESH_BINARY)
            if visualize:
                helpers.show_image(bint, 'binary image for threshold %i' % t)
            self.bint = bint.copy()
            if not helpers.image_diff(bint, previmg, visualize=False):
                regions = bindetector.detect(bint, find_holes, find_islands, find_indentations, find_protrusions, visualize=False)
            for regtype in regions.keys():
                result[regtype] += np.array(1 * (regions[regtype] > 0), dtype='uint8')

            previmg = bint

        self.regions_sum = result.copy()
        for regtype in result.keys():
            if visualize:
                helpers.show_image(result[regtype], regtype + ' before thresholding')
            result[regtype] = self.threshold_cumsum(result[regtype])
            if visualize:
                helpers.show_image(result[regtype], regtype + ' after thresholding')

        return result

    def threshold_cumsum(self, data):
        """Thresholds an image based on a percentile of the non-zero pixel values.

        Parameters
        ------
        data: 2-dimensional numpy array
            the image to threshold

        Returns
        ------
        binarized : numpy array
            Thresholded image
        """
        if len(np.unique(data)) <= 2:
            thres = np.min(data)
        else:
            data_values = data[(data > 0)]
            thres = np.percentile(data_values, int(self.perc * 100))
        _, binarized = cv2.threshold(data, thres, 255, cv2.THRESH_BINARY)
        return binarized