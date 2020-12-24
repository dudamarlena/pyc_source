# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/croppingimage/field.py
# Compiled at: 2008-07-23 09:49:01
from cStringIO import StringIO
from types import StringType, DictType
from Products.Archetypes.Field import ImageField, HAS_PIL, shasattr
if HAS_PIL:
    import PIL
_marker = []

class CroppingImageField(ImageField):
    """XXX Document me!
    """
    __module__ = __name__
    _properties = ImageField._properties.copy()
    _properties.update({'long_edge_size': 600, 'short_edge_size': 400, 'force_format': None})

    def _resize(self, imagestrio, dwidth, dheight):
        imagestrio.seek(0)
        image = PIL.Image.open(imagestrio)
        format = image.format
        size = (int(dwidth), int(dheight))
        image = image.resize(size=size)
        image.load()
        (width, height) = image.size
        data = StringIO()
        image.save(data, format)
        image.format = format
        data.seek(0)
        return (data, image, width, height)

    def rescaleOriginal(self, value, **kwargs):
        """rescales the original image and sets the data

        for self.original_size or self.max_size
        
        value must be an OFS.Image.Image instance
        """
        if not HAS_PIL:
            return data
        data = StringIO(str(value.data))
        image = PIL.Image.open(data)
        data.seek(0)
        (width, height) = image.size
        if self.force_format == 'landscape':
            is_landscape = True
        elif self.force_format == 'portrait':
            is_landscape = False
        else:
            is_landscape = False
            if width >= height:
                is_landscape = True
        is_portrait = not is_landscape
        self.is_landscape = is_landscape
        if is_landscape:
            desired_width = self.long_edge_size
            desired_height = self.short_edge_size
        else:
            desired_width = self.short_edge_size
            desired_height = self.long_edge_size
        aspect_ratio = float(height) / float(width)
        desired_ratio = float(desired_height) / float(desired_width)
        if desired_ratio == aspect_ratio:
            if width != desired_width:
                dwidth = desired_width
                dheight = desired_height
                (data, image, width, height) = self._resize(data, dwidth, dheight)
        elif is_landscape and desired_ratio < aspect_ratio:
            dwidth = desired_width
            dheight = desired_width * aspect_ratio
            (data, image, width, height) = self._resize(data, dwidth, dheight)
        elif is_landscape and desired_ratio > aspect_ratio:
            dwidth = desired_height / aspect_ratio
            dheight = desired_height
            (data, image, width, height) = self._resize(data, dwidth, dheight)
        elif is_portrait and desired_ratio > aspect_ratio:
            dwidth = desired_height / aspect_ratio
            dheight = desired_height
            (data, image, width, height) = self._resize(data, dwidth, dheight)
        elif is_portrait and desired_ratio < aspect_ratio:
            dwidth = desired_width
            dheight = desired_width * aspect_ratio
            (data, image, width, height) = self._resize(data, dwidth, dheight)
        if height > desired_height:
            diff = height - desired_height
            top_left = (
             0, diff / 2)
            bottom_right = (width, height - diff / 2)
            (data, format) = self.crop(image, top_left=top_left, bottom_right=bottom_right, default_format=image.format)
        elif width > desired_width:
            diff = width - desired_width
            top_left = (
             diff / 2, 0)
            bottom_right = (width - diff / 2, height)
            (data, format) = self.crop(image, top_left=top_left, bottom_right=bottom_right, default_format=image.format)
        data.seek(0)
        return data.read()

    def crop(self, data, top_left=(0, 0), bottom_right=None, default_format='PNG'):
        """Crop out a box from the image, defined by the co-ordinates of
        bottom_left and top_right.
        
        Return that box.
        """
        if bottom_right is None:
            msg = "Must provide a 'bottom_right' two-tuple of co-ordinates for the crop box."
            raise Exception(msg)
        if isinstance(data, PIL.Image.Image):
            image = data
        else:
            original_image = StringIO(data)
            image = PIL.Image.open(original_image)
        format = image.format
        box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        new_image = image.crop(box=box)
        new_image.load()
        cropped_output = StringIO()
        format = format and format or default_format
        new_image.save(cropped_output, format, quality=self.pil_quality)
        cropped_output.seek(0)
        return (cropped_output, format.lower())

    def getAvailableSizes(self, instance):
        """Get sizes

        Supports:
            self.sizes as dict
            A method in instance called like sizes that returns dict
            A callable
        """
        sizes = self.sizes
        if type(sizes) is DictType:
            pass
        elif type(sizes) is StringType:
            assert shasattr(instance, sizes)
            method = getattr(instance, sizes)
            data = method()
            assert type(data) is DictType
            sizes = data
        elif callable(sizes):
            sizes = sizes()
        elif sizes is None:
            sizes = {}
        else:
            raise TypeError, 'Wrong self.sizes has wrong type: %s' % type(sizes)
        try:
            is_landscape = self.is_landscape
        except AttributeError:
            return sizes

        for key in sizes.keys():
            (width, height) = sizes[key]
            if is_landscape and width < height or not is_landscape and width > height:
                sizes[key] = (
                 height, width)

        return sizes