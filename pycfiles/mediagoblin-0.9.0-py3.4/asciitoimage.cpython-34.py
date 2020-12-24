# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/media_types/ascii/asciitoimage.py
# Compiled at: 2013-09-23 12:05:51
# Size of source mod 2**32: 4459 bytes
try:
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
except ImportError:
    import Image, ImageFont, ImageDraw

import logging, pkg_resources, os
_log = logging.getLogger(__name__)

class AsciiToImage(object):
    __doc__ = '\n    Converter of ASCII art into image files, preserving whitespace\n\n    kwargs:\n    - font: Path to font file\n      default: fonts/Inconsolata.otf\n    - font_size: Font size, ``int``\n      default: 11\n    '

    def __init__(self, **kw):
        self._font = kw.get('font', pkg_resources.resource_filename('mediagoblin.media_types.ascii', os.path.join('fonts', 'Inconsolata.otf')))
        self._font_size = kw.get('font_size', 11)
        self._if = ImageFont.truetype(self._font, self._font_size, encoding='unic')
        _log.info('Font set to {0}, size {1}'.format(self._font, self._font_size))
        self._if_dims = self._if.getsize('.')

    def convert(self, text, destination):
        im = self._create_image(text)
        if im.save(destination):
            _log.info('Saved image in {0}'.format(destination))

    def _create_image(self, text):
        """
        Write characters to a PIL image canvas.

        TODO:
        - Character set detection and decoding,
          http://pypi.python.org/pypi/chardet
        """
        _log.debug('Drawing image')
        text = text.decode('utf-8')
        lines = text.split('\n')
        line_lengths = [len(i) for i in lines]
        im_dims = (
         max(line_lengths) * self._if_dims[0],
         len(line_lengths) * self._if_dims[1])
        _log.info('Destination image dimensions will be {0}'.format(im_dims))
        im = Image.new('RGBA', im_dims, (255, 255, 255, 0))
        draw = ImageDraw.Draw(im)
        char_pos = [
         0, 0]
        for line in lines:
            line_length = len(line)
            _log.debug('Writing line at {0}'.format(char_pos))
            for _pos in range(0, line_length):
                char = line[_pos]
                px_pos = self._px_pos(char_pos)
                _log.debug('Writing character "{0}" at {1} (px pos {2})'.format(char.encode('ascii', 'replace'), char_pos, px_pos))
                draw.text(px_pos, char, font=self._if, fill=(0, 0, 0, 255))
                char_pos[0] += 1

            char_pos[0] = 0
            char_pos[1] += 1

        return im

    def _px_pos(self, char_pos):
        """
        Helper function to calculate the pixel position based on
        character position and character dimensions
        """
        px_pos = [
         0, 0]
        for index, val in zip(range(0, len(char_pos)), char_pos):
            px_pos[index] = char_pos[index] * self._if_dims[index]

        return px_pos