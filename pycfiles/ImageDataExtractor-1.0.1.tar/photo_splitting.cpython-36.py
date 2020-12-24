# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edward/github/ImageDataExtractor/imagedataextractor/photo_splitting.py
# Compiled at: 2019-05-20 06:43:25
# Size of source mod 2**32: 7681 bytes
"""
Photo Detection
===============

Detect photos in figures.

@author : Matt Swain

TODO : This code is from Matt's currently unpublished FigureDataExtractor code. We must ask his permission before
publishing it with this code

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging, numpy as np
from skimage.measure import label, regionprops
import six
from marshmallow import Schema, fields
from skimage.color import rgb2gray
log = logging.getLogger(__name__)

def python_2_unicode_compatible(klass):
    """Fix ``__str__``, ``__unicode__`` and ``__repr__`` methods under Python 2.

    Add this decorator to a class, then define ``__str__`` and ``__repr__`` methods that both return unicode strings.
    Under python 2, this will return encoded strings for ``__str__`` (utf-8) and ``__repr__`` (ascii), and add
    ``__unicode__`` and ``_unicode_repr`` to return the original unicode strings. Under python 3, this does nothing.
    """
    if six.PY2:
        if '__str__' not in klass.__dict__:
            raise ValueError('Define __str__() on %s to use @python_2_unicode_compatible' % klass.__name__)
        if '__repr__' not in klass.__dict__:
            raise ValueError('Define __repr__() on %s to use @python_2_unicode_compatible' % klass.__name__)
        klass.__unicode__ = klass.__str__
        klass._unicode_repr = klass.__repr__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
        klass.__repr__ = lambda self: self._unicode_repr().encode('ascii', errors='backslashreplace')
    return klass


class BaseSchema(Schema):

    class Meta:
        ordered = True


class RectSchema(BaseSchema):
    __doc__ = 'Rect schema.'
    left = fields.Integer()
    right = fields.Integer()
    top = fields.Integer()
    bottom = fields.Integer()


class PhotoSchema(RectSchema):
    __doc__ = 'Photo schema.'


@python_2_unicode_compatible
class Rect(object):
    __doc__ = 'A rectangular region.'

    def __init__(self, left, right, top, bottom):
        """

        :param int left: Left edge of rectangle.
        :param int right: Right edge of rectangle.
        :param int top: Top edge of rectangle.
        :param int bottom: Bottom edge of rectangle.
        """
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    @property
    def width(self):
        """Return width of rectangle in pixels. May be floating point value.

        :rtype: int
        """
        return self.right - self.left

    @property
    def height(self):
        """Return height of rectangle in pixels. May be floating point value.

        :rtype: int
        """
        return self.bottom - self.top

    @property
    def perimeter(self):
        """Return length of the perimeter around rectangle.

        :rtype: int
        """
        return 2 * self.height + 2 * self.width

    @property
    def area(self):
        """Return area of rectangle in pixels. May be floating point values.

        :rtype: int
        """
        return self.width * self.height

    @property
    def center(self):
        """Center point of rectangle. May be floating point values.

        :rtype: tuple(int|float, int|float)
        """
        xcenter = (self.left + self.right) / 2
        ycenter = (self.bottom + self.top) / 2
        return (xcenter, ycenter)

    @property
    def center_px(self):
        """(x, y) coordinates of pixel nearest to center point.

        :rtype: tuple(int, int)
        """
        xcenter, ycenter = self.center
        return (np.around(xcenter), np.around(ycenter))

    def contains(self, other_rect):
        """Return true if ``other_rect`` is within this rect.

        :param Rect other_rect: Another rectangle.
        :return: Whether ``other_rect`` is within this rect.
        :rtype: bool
        """
        return other_rect.left >= self.left and other_rect.right <= self.right and other_rect.top >= self.top and other_rect.bottom <= self.bottom

    def overlaps(self, other_rect):
        """Return true if ``other_rect`` overlaps this rect.

        :param Rect other_rect: Another rectangle.
        :return: Whether ``other_rect`` overlaps this rect.
        :rtype: bool
        """
        return min(self.right, other_rect.right) > max(self.left, other_rect.left) and min(self.bottom, other_rect.bottom) > max(self.top, other_rect.top)

    def __repr__(self):
        return '%s(left=%s, right=%s, top=%s, bottom=%s)' % (
         self.__class__.__name__, self.left, self.right, self.top, self.bottom)

    def __str__(self):
        return '<%s (%s, %s, %s, %s)>' % (self.__class__.__name__, self.left, self.right, self.top, self.bottom)


class Photo(Rect):
    __doc__ = 'A photo within a figure.'

    def __init__(self, left, right, top, bottom):
        super(Photo, self).__init__(left, right, top, bottom)

    def serialize(self):
        """Serialize this panel with :class:`~figuredataextractor.schema.PhotoSchema`."""
        return PhotoSchema().dump(self).data


def get_photos(img, min_edge=0.05, min_fill=0.8, binary_threshold=0.98):
    """Extract the photos in an image.

    :param numpy.ndarray img: Input image.
    :param float min_edge: Minimum photo edge length as fraction of shortest image dimension.
    :param float min_fill: Threshold for how much of a region must be non-white to be considered a photo.
    :param float binary_threshold: Threshold to use when binarizing image.
    :return: Extracted photos.
    :rtype: list[figuredataextractor.model.Photo]
    """
    log.debug('Detecting photos in image')
    photos = []
    binary = binarize(img, binary_threshold)
    min_length_px = np.around(min_edge * min(binary.shape))
    log.debug('Minimum photo edge length: %s * shortest image dimension = %s pixels', min_edge, min_length_px)
    label_image = label(1 - binary)
    for region in regionprops(label_image):
        top, left, bottom, right = region.bbox
        if right - left > min_length_px and bottom - top > min_length_px and region.extent > min_fill:
            photos.append(Photo(left=left, right=right, top=top, bottom=bottom))

    log.debug('Found photos: %s', photos)
    return photos


def binarize(img, threshold=0.9):
    """Convert image to binary.

    RGB images are converted to greyscale using :class:`skimage.color.rgb2gray` before binarizing.

    :param numpy.ndarray img: Input image
    :param float|numpy.ndarray threshold: Threshold to use.
    :return: Binary image.
    :rtype: numpy.ndarray
    """
    if img.ndim <= 2:
        if img.dtype == bool:
            return img
    if img.ndim == 3:
        if img.shape[(-1)] in (3, 4):
            img = rgb2gray(img)
    binary = img > threshold
    return binary