# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/croppingimagefield/fields.py
# Compiled at: 2009-07-20 20:54:42
from cStringIO import StringIO
from Products.Archetypes.Field import ImageField, HAS_PIL
from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from ZODB.POSException import ConflictError
if HAS_PIL:
    import PIL
_marker = []
RESIZE_SCALE = 0
RESIZE_ZOOM = 1
RESIZE_CROP = 2

class CroppingImageField(ImageField):
    """
    See README.txt for documentation and example
    """
    __module__ = __name__
    _properties = ImageField._properties.copy()
    _properties.update({'original_crop': False})
    __implements__ = ImageField.__implements__
    security = ClassSecurityInfo()
    security.declareProtected(permissions.ModifyPortalContent, 'rescaleOriginal')

    def rescaleOriginal(self, value, **kwargs):
        """rescales the original image and sets the data

        for self.original_size or self.max_size
        
        value must be an OFS.Image.Image instance
        """
        data = str(value.data)
        if not HAS_PIL:
            return data
        mimetype = kwargs.get('mimetype', self.default_content_type)
        if self.original_size or self.max_size:
            if not value:
                return self.default
            w = h = s = r = 0
            if self.max_size:
                if value.width > self.max_size[0] or value.height > self.max_size[1]:
                    factor = min(float(self.max_size[0]) / float(value.width), float(self.max_size[1]) / float(value.height))
                    w = int(factor * value.width)
                    h = int(factor * value.height)
            elif self.original_size:
                w = self.original_size[0]
                h = self.original_size[1]
                if len(self.original_size) > 2:
                    r = self.original_size[2]
            if w and h:
                __traceback_info__ = (
                 self, value, w, h, r)
                (fvalue, format) = self.resize(data, w, h, r)
                data = fvalue.read()
        else:
            data = str(value.data)
        return data

    security.declareProtected(permissions.ModifyPortalContent, 'createScales')

    def createScales(self, instance, value=_marker):
        """creates the scales and save them
        """
        sizes = self.getAvailableSizes(instance)
        if not HAS_PIL or not sizes:
            return
        if value is _marker:
            img = self.getRaw(instance)
            if not img:
                return
            data = str(img.data)
        else:
            data = value
        if not data:
            return
        filename = self.getFilename(instance)
        for (n, size) in sizes.items():
            if size[:2] == (0, 0):
                continue
            w = size[0]
            h = size[1]
            if len(size) > 2:
                r = size[2]
            else:
                r = 0
            id = self.getName() + '_' + n
            __traceback_info__ = (self, instance, id, w, h, r)
            try:
                (imgdata, format) = self.resize(data, w, h, r)
            except (ConflictError, KeyboardInterrupt):
                raise
            except:
                if not self.swallowResizeExceptions:
                    raise
                else:
                    log_exc()
                    continue

            mimetype = 'image/%s' % format.lower()
            image = self._make_image(id, title=self.getName(), file=imgdata, content_type=mimetype, instance=instance)
            image.filename = filename
            try:
                delattr(image, 'title')
            except (KeyError, AttributeError):
                pass

            self.getStorage(instance).set(id, instance, image, mimetype=mimetype, filename=filename)

    security.declarePrivate('resize')

    def resize(self, data, w, h, r, default_format='PNG'):
        """ resize image (with material from ImageTag_Hotfix)"""
        size = (
         int(w), int(h))
        original_file = StringIO(data)
        image = PIL.Image.open(original_file)
        original_mode = image.mode
        if original_mode == '1':
            image = image.convert('L')
        elif original_mode == 'P':
            image = image.convert('RGBA')
        resize = int(r)
        (iw, ih) = image.size
        (dw, dh) = size
        ir = float(iw) / float(ih)
        dr = float(dw) / float(dh)
        wr = float(dw) / float(iw)
        hr = float(dh) / float(ih)
        if resize == RESIZE_ZOOM:
            if ir > dr:
                size = (
                 int(iw * hr), dh)
            else:
                size = (
                 dw, int(ih * wr))
            image = image.resize(size, self.pil_resize_algo)
        elif resize == RESIZE_CROP:
            l = t = 0
            if ir > dr:
                osize = (
                 int(iw * hr), dh)
                l = int((iw * hr - dw) / 2)
            else:
                osize = (
                 dw, int(ih * wr))
                t = int((ih * wr - dh) / 2)
            image = image.resize(osize, self.pil_resize_algo)
            image = image.crop((l, t, l + dw, t + dh))
        else:
            if ir > dr:
                size = (
                 dw, int(ih * wr))
            else:
                size = (
                 int(iw * hr), dh)
            image = image.resize(size, self.pil_resize_algo)
        format = image.format and image.format or default_format
        if original_mode == 'P' and format == 'GIF':
            image = image.convert('P')
        thumbnail_file = StringIO()
        image.save(thumbnail_file, format, quality=self.pil_quality)
        thumbnail_file.seek(0)
        return (thumbnail_file, format.lower())

    security.declarePrivate('scale')
    scale = resize