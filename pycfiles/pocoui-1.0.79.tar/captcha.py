# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/captcha.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = "\n    pocoo.utils.captcha\n    ~~~~~~~~~~~~~~~~~~~\n\n    Create Captcha images.\n\n    Typical usage::\n\n        >>> from pocoo.utils.captcha import Captcha\n        >>> c = Captcha()\n        >>> c\n        <Captcha 'FGVZBS'>\n        >>> c.code\n        'FGVZBS'\n        >>> fp = file('output.png', 'w')\n        >>> fp.write(c.generate_image())\n        >>> fp.close()\n        >>> c == 'FGVZBS'\n        True\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n"
import pocoo, os, random
from PIL import Image, ImageFont, ImageDraw
from cStringIO import StringIO
Image = Image.new
Canvas = ImageDraw.Draw
Font = ImageFont.truetype
CAPTCHA_CHARS = 'ABCDEFGHIKLMNPQRSTVWXYZ123456789'

def gen_captcha_key(length=6):
    """
    Generate a captcha key of ``length`` characters.
    """
    result = []
    for _ in xrange(length):
        result.append(random.choice(CAPTCHA_CHARS))

    return ('').join(result)


class Captcha(object):
    """
    Represents a captcha image.
    """
    __module__ = __name__

    def __init__(self, chars=6, code=None):
        if code is None:
            code = gen_captcha_key(chars)
        self.code = code
        return

    def __eq__(self, other):
        if isinstance(other, Captcha):
            return self.code == other.code
        if isinstance(other, basestring):
            return self.code == other
        raise TypeError, "Can't compare Captcha to %r" % other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.code)

    def __str__(self):
        return self.code

    def generate_image(self, width=200, height=70, font_size=50, vlines=6, hlines=10, drawpoints=True, pointdeep=10, bgcolor='#eeeeee', linecolor='#bbbbbb', colors=('#222222', '#444444', '#666666', '#888888'), pointcolor='#ffffff'):
        """
        Create a PNG version of the code image.

        Arguments:

        width
          width in pixel (default: 200)

        height
          height in pixel (default: 70)

        font_size
          font size in pixel (default: 50)

        vlines
          lines crossing the image vertically (default: 6)

        hlines
          lines crossing the image horizontally (default: 10)

        drawpoints
          should the background of the image be dotted? (default: True)

        pointdeep
          number defining amount of dots. (1 - many / 20 - few)
          if you define a number higher than 20 it's the same is setting
          drawpoints to False. (default: 10)

        bgcolor
          hex value of the background color (default: #eeeeee)

        linecolor
          hex value of the line color (default: #bbbbbb)

        colors
          list of colors used for the characters

        pointcolor
          color of the background dots if enabled (default: #ffffff)
        """
        font_path = os.path.dirname(pocoo.__file__) + '/res/captcha.ttf'
        img = Image('RGB', (width, height), bgcolor)
        c = Canvas(img)
        f = Font(font_path, font_size)
        max_len = len(self.code)
        if drawpoints and pointdeep <= 20:
            limes = 20 - pointdeep
            for x in xrange(width):
                for y in xrange(height):
                    if random.randrange(0, 20) > limes:
                        c.point((x, y), fill=pointcolor)

        for (pos, char) in enumerate(self.code):
            color = random.choice(colors)
            point = (int(width / max_len) * pos + 8, random.randrange(-2, height - font_size - 4))
            c.text(point, char, fill=color, font=f)

        for _ in xrange(vlines):
            c.line([(0, random.randrange(0, height + 1)), (width, random.randrange(0, height + 1))], fill=linecolor)

        for _ in xrange(hlines):
            c.line([(random.randrange(0, width + 1), 0), (random.randrange(0, width + 1), height)], fill=linecolor)

        out = StringIO()
        img.save(out, 'PNG')
        return out.getvalue()