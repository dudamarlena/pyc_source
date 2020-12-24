# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/castro/lib/pyvnc2swf/image.py
# Compiled at: 2011-03-28 15:09:52
import sys
lowerbound = max
upperbound = min
IMG_SOLID = 1
IMG_RAW = 2
IMG_LOSSLESS = 3
IMG_VIDEOPACKET = 4

def bgr2rgb(data):
    return ('').join([ data[(i + 2)] + data[(i + 1)] + data[i] for i in xrange(0, len(data), 3) ])


try:
    import pygame
    pygame.init()
    try:
        pygame.mixer.quit()
    except NotImplementedError:
        pass

    def imgsize(img):
        return img.get_size()


    def create_image(w, h):
        return pygame.Surface((w, h), 0, 32)


    def create_image_from_string_rgb(w, h, data):
        return pygame.image.fromstring(data, (w, h), 'RGB')


    def create_image_from_string_rgbx(w, h, data):
        return pygame.image.fromstring(data, (w, h), 'RGBX')


    def create_image_from_string_xrgb(w, h, data):
        return pygame.image.fromstring(data[1:] + 'x', (w, h), 'RGBX')


    def create_image_from_string_argb(w, h, data):
        data = ('').join([ data[(i + 1)] + data[(i + 2)] + data[(i + 3)] + data[i] for i in xrange(0, len(data), 4) ])
        return pygame.image.fromstring(data, (w, h), 'RGBA')


    def create_image_from_string_rgb_flipped(w, h, data):
        return pygame.image.fromstring(data, (w, h), 'RGB', 1)


    def crop_image(img, (x, y, w, h)):
        (wm, hm) = img.get_size()
        return img.subsurface((x, y, upperbound(wm - x, w), upperbound(hm - y, h)))


    def paste_image(dest, src, (x0, y0)):
        return dest.blit(src, (x0, y0))


    def save_image(img, fname):
        if not fname.endswith('.bmp'):
            print >> sys.stderr, 'Warning: this format not supported by pygame, raw rgb is used instead.'
        return pygame.image.save(img, fname)


    def convert_image_to_string_rgb_flipped(img):
        return pygame.image.tostring(img, 'RGB', 1)


    def convert_image_to_string_rgb(img):
        return pygame.image.tostring(img, 'RGB')


    def convert_image_to_string_xrgb(img):
        return pygame.image.tostring(img, 'ARGB')


    def solid_fill(dest, rect, color):
        return dest.fill(color, rect)


    def scale_image(img, scaling):
        return pygame.transform.rotozoom(img, 0, scaling)


except ImportError:
    pygame = None
    try:
        import Image
    except ImportError:
        print >> sys.stderr, 'Either Pygame or Python Imaging Library is required.'
        sys.exit(1)
    else:
        print >> sys.stderr, 'Using PIL', Image.VERSION

        def imgsize(img):
            return img.size


        def create_image(w, h):
            return Image.new('RGB', (w, h))


        def create_image_from_string_rgb(w, h, data):
            return Image.fromstring('RGB', (w, h), data, 'raw', 'RGB')


        def create_image_from_string_rgbx(w, h, data):
            return Image.fromstring('RGB', (w, h), data, 'raw', 'RGBX')


        def create_image_from_string_xrgb(w, h, data):
            return Image.fromstring('RGB', (w, h), data[1:] + 'x', 'raw', 'RGBX')


        def create_image_from_string_argb(w, h, data):
            return Image.fromstring('RGBA', (w, h), data, 'raw', 'ARGB')


        def create_image_from_string_rgb_flipped(w, h, data):
            return Image.fromstring('RGB', (w, h), data, 'raw', 'RGB').transpose(Image.FLIP_TOP_BOTTOM)


        def crop_image(img, (x0, y0, w, h)):
            (wm, hm) = img.size
            return img.crop((x0, y0, upperbound(x0 + w, wm), upperbound(y0 + h, hm)))


        def paste_image(dest, src, (x0, y0)):
            return dest.paste(src, (x0, y0))


        def save_image(img, fname):
            return img.save(fname)


        def convert_image_to_string_rgb_flipped(img):
            return img.transpose(Image.FLIP_TOP_BOTTOM).tostring('raw', 'RGB')


        def convert_image_to_string_rgb(img):
            return img.tostring('raw', 'RGB')


        def convert_image_to_string_xrgb(img):
            return img.tostring('raw', 'XRGB')


        def solid_fill(dest, (x0, y0, w, h), color):
            return dest.paste(color, (x0, y0, x0 + w, y0 + h))


        def scale_image(img, scaling):
            img = img.copy()
            (w, h) = img.size
            img.thumbnail((int(w * scaling), int(h * scaling)), resample=1)
            return img