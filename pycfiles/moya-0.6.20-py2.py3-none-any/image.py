# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/image.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import division
import logging, threading
from ..elements.elementbase import LogicElement, Attribute
from ..tags.context import DataSetterBase
from .. import namespaces
from ..compat import implements_to_string
from fs.path import basename, join, splitext
from PIL import Image, ImageFilter
try:
    from PIL import ExifTags
except ImportError:
    ExifTags = None

log = logging.getLogger(b'moya.image')

@implements_to_string
class MoyaImage(object):
    """Proxy interface for a PIL image"""

    def __init__(self, img, filename):
        self._img = img
        self.filename = filename
        self._lock = threading.RLock()

    def __str__(self):
        w, h = self._img.size
        return (b"<image '{}' {}x{} {}>").format(self.filename, w, h, self.mode)

    def __repr__(self):
        w, h = self._img.size
        return (b"<image '{}' {}x{} {}>").format(self.filename, w, h, self.mode)

    def replace(self, img):
        self._img = img

    @property
    def format(self):
        return self._img.format

    @property
    def size(self):
        w, h = self._img.size
        return {b'width': w, b'height': h}

    @property
    def mode(self):
        return self._img.mode

    @property
    def info(self):
        return self._img.info

    @property
    def exif(self):
        with self._lock:
            self._img.load()
            _exif = self._img._getexif()
            if _exif is None:
                return {}
            exif = {}
            if ExifTags:
                for k, v in _exif.items():
                    try:
                        key = ExifTags.TAGS.get(k, None)
                        if key is not None:
                            value = v.decode(b'utf-8', b'replace') if isinstance(v, bytes) else v
                            exif[key] = value
                    except Exception as e:
                        log.debug(b'exif extract error: %s', e)

            return exif
        return


class Read(DataSetterBase):
    """Read an image"""
    xmlns = namespaces.image

    class Help:
        synopsis = b'read an image from disk'

    class Meta:
        one_of = [
         ('fsobj', 'fs', 'file')]

    path = Attribute(b'Path', required=False, default=None)
    fsobj = Attribute(b'FS', type=b'Index')
    fs = Attribute(b'FS name')
    dst = Attribute(b'Destination', type=b'reference', default=b'image')
    _file = Attribute(b'File object with image data', type=b'expression')
    filename = Attribute(b"Filename to associate with the image if the filename can't be detected", default=b'', type=b'expression')

    def get_image(self, context, params):
        if self.has_parameter(b'file'):
            fp = getattr(params.file, b'__moyafile__', lambda : params.file)()
            try:
                fp.seek(0)
                img = Image.open(fp)
                img.load()
                fp.seek(0)
            except Exception as e:
                self.throw(b'image.read-fail', (b'Failed to read image from file ({})').format(e))

        elif params.fsobj is not None:
            fs = params.fsobj
        else:
            try:
                fs = self.archive.filesystems[params.fs]
            except KeyError:
                self.throw(b'image.no-fs', (b"No filesystem called '{}'").format(params.fs))

            if params.path is None:
                self.throw(b'image.path-required', b'a path is required when reading from a filesystem')
            try:
                fp = fs.open(params.path, b'rb')
                img = Image.open(fp)
            except Exception as e:
                self.throw(b'image.read-fail', (b"failed to read '{}' from {!r} ({})").format(params.path, fs, e))

        return img

    def logic(self, context):
        params = self.get_parameters(context)
        img = self.get_image(context, params)
        try:
            img.load()
        except Exception as e:
            self.throw(b'image.read-fail', (b'Failed to read image ({})').format(e))

        moya_image = MoyaImage(img, filename=basename(params.path or params.filename or b''))
        self.set_context(context, params.dst, moya_image)
        log.debug(b'%r read', moya_image)


class GetSize(Read):
    """Get the dimensions of an image without loading image data, returns a dictionary with keys 'width' and 'height'."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'get the dimensions of an image'

    class Meta:
        one_of = [
         ('fsobj', 'fs', 'file')]

    path = Attribute(b'Path')
    fsobj = Attribute(b'FS', type=b'Index')
    fs = Attribute(b'FS name')
    dst = Attribute(b'Destination', type=b'reference', default=b'image')
    _file = Attribute(b'File object with image data', type=b'expression')

    def logic(self, context):
        params = self.get_parameters(context)
        img = self.get_image(context, params)
        w, h = img.size
        result = {b'width': w, b'height': h}
        self.set_context(context, params.dst, result)


class CheckImageMixin(object):
    """Mixin for checking images."""

    def check_image(self, context, image):
        if not isinstance(image, MoyaImage):
            _msg = b"attribute 'image' should reference an image object, not {}"
            self.throw(b'bad-value.image', _msg.format(context.to_expr(image)))


class ImageElement(LogicElement, CheckImageMixin):
    pass


class Write(ImageElement):
    """Write an image"""
    xmlns = namespaces.image

    class Help:
        synopsis = b'write an image to disk'

    class Meta:
        one_of = [
         ('fs', 'fsobj')]

    image = Attribute(b'Image to write', type=b'expression', default=b'image', evaldefault=True, missing=False)
    dirpath = Attribute(b'Directory to write image', required=False, default=b'/')
    filename = Attribute(b'Image filename', required=True)
    fsobj = Attribute(b'FS', type=b'expression')
    fs = Attribute(b'FS name')
    format = Attribute(b'Image format', default=None, choices=[b'jpeg', b'png', b'gif'])

    def logic(self, context):
        params = self.get_parameters(context)
        self.check_image(context, params.image)
        if params.fsobj is not None:
            fs = params.fsobj
        else:
            try:
                fs = self.archive.filesystems[params.fs]
            except KeyError:
                self.throw(b'image.no-fs', (b"No filesystem called '{}'").format(params.fs))
                return

        path = join(params.dirpath, params.filename)
        with params.image._lock:
            img = params.image._img
            img_format = params.format or splitext(params.filename or b'')[(-1)].lstrip(b'.') or b'jpeg'
            if img_format == b'jpeg':
                if img.mode != b'RGB':
                    img = img.convert(b'RGB')
            save_params = self.get_let_map(context)
            try:
                with fs.makedirs(params.dirpath, recreate=True) as (dir_fs):
                    with dir_fs.open(params.filename, b'wb') as (f):
                        img.save(f, img_format, **save_params)
                log.debug(b"wrote '%s'", params.filename)
            except Exception as e:
                raise
                self.throw(b'image.write-fail', (b"Failed to write {} to '{}' in {!r} ({})").format(params.image, path, fs, e))

        return


class New(DataSetterBase, CheckImageMixin):
    """Create a blank image."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'create a blank image'

    size = Attribute(b'Size of new image', type=b'expression', required=True)
    mode = Attribute(b'Mode', default=b'RGB')
    color = Attribute(b'Color', default=b'#000000')
    dst = Attribute(b'Destination', type=b'index', default=b'image')

    def logic(self, context):
        params = self.get_parameters(context)
        image = Image.new(params.mode, params.size, params.color)
        moya_image = MoyaImage(image, filename=b'new.jpg')
        self.set_context(context, params.dst, moya_image)


class Copy(DataSetterBase, CheckImageMixin):
    """Create an copy of [c]image[/c] in [c]dst[/c]."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'create a copy of an image'

    image = Attribute(b'Image to copy', type=b'expression', default=b'image', evaldefault=True)
    dst = Attribute(b'Destination', type=b'reference', default=b'image')

    def logic(self, context):
        params = self.get_parameters(context)
        self.check_image(context, params.image)
        with params.image._lock:
            img = params.image._img
            moya_image = MoyaImage(img.copy(), params.image.filename)
            self.set_context(context, params.dst, moya_image)


class Show(ImageElement):
    """Show an image (for debugging purposes). Imagemagick is required for this operation."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'show an image'

    image = Attribute(b'Image to show', type=b'expression', default=b'image', evaldefault=True)

    def logic(self, context):
        if context[b'.debug']:
            self.image(context)._img.show()
        else:
            log.warn(b'<show> can be used in debug mode only')


_resample_methods = {b'nearest': Image.NEAREST, 
   b'bilinear': Image.BILINEAR, 
   b'bicubic': Image.BICUBIC, 
   b'antialias': Image.ANTIALIAS}

def _fit_dimensions(image, width, height):
    w, h = image.size
    if width is None:
        width = w * (height / h)
    if height is None:
        height = h * (width / w)
    ratio = min(width / w, height / h)
    width = w * ratio
    height = h * ratio
    return (
     int(round(width)), int(round(height)))


class ResizeToFit(ImageElement):
    """Resize image to fit within the given dimensions (maintains aspect ratio)."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'resize an image to fit within new dimensions'

    image = Attribute(b'Image to show', type=b'expression', default=b'image', evaldefault=True)
    width = Attribute(b'New width', type=b'integer', required=False, default=None)
    height = Attribute(b'New height', type=b'integer', required=False, default=None)
    resample = Attribute(b'Method for resampling', default=b'antialias', choices=_resample_methods.keys())

    def logic(self, context):
        params = self.get_parameters(context)
        self.check_image(context, params.image)
        with params.image._lock:
            image = params.image._img
            new_size = _fit_dimensions(image, params.width, params.height)
            w, h = new_size
            if not w or not h:
                self.throw(b'image.bad-dimensions', (b'Invalid image dimensions ({} x {})').format(params.width, params.height), diagnosis=b'Width and / or height should be supplied, and should be non-zero')
            params.image.replace(image.resize(new_size, _resample_methods[params.resample]))


class ZoomToFit(ImageElement):
    """Resize image to given dimensions, cropping if necessary."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'resize an image to fit in new dimensions, with cropping'

    image = Attribute(b'Image to show', type=b'expression', default=b'image', evaldefault=True)
    width = Attribute(b'New width', type=b'integer', required=True)
    height = Attribute(b'New height', type=b'integer', required=True)
    resample = Attribute(b'Method for resampling', default=b'antialias', choices=_resample_methods.keys())

    def logic(self, context):
        params = self.get_parameters(context)
        self.check_image(context, params.image)
        with params.image._lock:
            image = params.image._img
            aspect = image.size[0] / image.size[1]
            if image.size[0] > image.size[1]:
                new_size = (
                 int(params.height * aspect), params.height)
            else:
                new_size = (
                 params.width, int(params.width / aspect))
            img = image.resize(new_size, _resample_methods[params.resample])
            w = params.width
            h = params.height
            x = (img.size[0] - w) // 2
            y = (img.size[1] - h) // 2
            box = (
             x, y, x + w, y + h)
            params.image.replace(img.crop(box))


class Resize(ImageElement):
    """Resize an image to new dimensions."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'resize an image'

    image = Attribute(b'Image to show', type=b'expression', default=b'image', evaldefault=True)
    width = Attribute(b'New width', type=b'integer', required=False, default=None)
    height = Attribute(b'New height', type=b'integer', required=False, default=None)
    resample = Attribute(b'Method for resampling', default=b'antialias', choices=[b'nearest', b'bilinear', b'bicubic', b'antialias'])

    def logic(self, context):
        params = self.get_parameters(context)
        self.check_image(context, params.image)
        with params.image._lock:
            image = params.image._img
            new_size = (params.width, params.height)
            w, h = new_size
            if not w or not h:
                self.throw(b'image.bad-dimensions', (b'Invalid image dimensions ({} x {})').format(params.width, params.height), diagnosis=b'Width and / or height should be supplied, and should be non-zero')
            params.image.replace(image.resize(new_size, _resample_methods[params.resample]))


class ResizeCanvas(ImageElement):
    """Resize the image canvas."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'resize the image canvas'

    image = Attribute(b'Image to show', type=b'expression', default=b'image', evaldefault=True)
    width = Attribute(b'New width', type=b'integer', required=True)
    height = Attribute(b'New height', type=b'integer', required=True)
    color = Attribute(b'Background color', type=b'color', default=b'#000000')

    def logic(self, context):
        image, w, h, color = self.get_parameters(context, b'image', b'width', b'height', b'color')
        self.check_image(context, image)
        with image._lock:
            img = image._img
            mode = img.mode
            if color.a != 1:
                mode = b'RGBA'
            new_img = Image.new(mode, (w, h), color.as_pillow_tuple())
            iw, ih = img.size
            x = (w - iw) // 2
            y = (h - ih) // 2
            new_img.paste(img, (x, y))
            image.replace(new_img)


class Square(ImageElement):
    """Square crop an image."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'square crop an image'

    image = Attribute(b'Image to crop', type=b'expression', default=b'image', evaldefault=True)

    def logic(self, context):
        params = self.get_parameters(context)
        self.check_image(context, params.image)
        with params.image._lock:
            img = params.image._img
            w, h = img.size
            size = min(img.size)
            x = (w - size) // 2
            y = (h - size) // 2
            new_img = Image.new(img.mode, (size, size))
            new_img.paste(img, (-x, -y))
            params.image.replace(new_img)


class Crop(ImageElement):
    """Crop an image to a given area."""
    xmlns = namespaces.image

    class Help:
        synopsis = b'crop an image'

    image = Attribute(b'Image to show', type=b'expression', default=b'image', evaldefault=True)
    box = Attribute(b'Crop size (either [width, height] or [x, y, width, height])', type=b'expression')

    def logic(self, context):
        params = self.get_parameters(context)
        size = params.box
        self.check_image(context, params.image)
        with params.image._lock:
            img = params.image._img
            if len(size) == 2:
                w, h = size
                x = (img.size[0] - w) // 2
                y = (img.size[1] - h) // 2
            elif len(size) == 4:
                x, y, w, h = size
            else:
                self.throw(b'bad-value.box-invalid', (b"parameter 'box' should be  sequence of 2 or 4 parameters (not {})").format(context.to_expr(size)))
            box = (x, y, x + w, y + h)
            params.image.replace(img.crop(box))


class GaussianBlur(ImageElement):
    """Guassian blur an image."""
    xmlns = namespaces.image
    image = Attribute(b'Image to show', type=b'expression', default=b'image', evaldefault=True)
    radius = Attribute(b'Radius of blur', type=b'integer', default=2)

    def logic(self, context):
        params = self.get_parameters(context)
        self.check_image(context, params.image)
        with params.image._lock:
            img = params.image._img
            if img.mode == b'P':
                img = img.convert(b'RGB')
            new_image = img.filter(ImageFilter.GaussianBlur(radius=params.radius))
            params.image.replace(new_image)