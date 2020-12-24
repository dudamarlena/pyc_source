# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/picharsso/processor.py
# Compiled at: 2019-11-08 16:27:15
# Size of source mod 2**32: 1779 bytes
from numpy import zeros, resize, vectorize, ascontiguousarray, array
from cv2 import cvtColor, COLOR_RGB2GRAY, normalize, NORM_MINMAX
PATTERN = {(0, 0):1, 
 (0, 1):8,  (1, 0):2, 
 (1, 1):16,  (2, 0):4, 
 (2, 1):32,  (3, 0):64, 
 (3, 1):128}

class Processor:
    __doc__ = 'A wrapper for processing the image\n    '

    def art(self):
        """Processes image and extracts values for text art
        """
        self.load_image()
        self.resize_image()
        if self.args.color:
            canvas = cvtColor(self.image, COLOR_RGB2GRAY)
        else:
            canvas = self.image
        run = {'braille':self.braille, 
         'ascii':self.ascii}
        run.get(self.args.art)(canvas)
        self.colorize()
        self.display()

    def braille(self, canvas):
        """Processes image and extracts values for Braille based text art
        """
        canvas = canvas.astype(int)
        text = zeros((canvas[::4, ::2].shape), dtype=int)
        for y in range(4):
            for x in range(2):
                text += resize((canvas[y::4, x::2] > self.args.threshold) * PATTERN.get((y, x)), text.shape)

        text = vectorize(lambda x: chr(ord('⠀') + x))(text)
        text = ascontiguousarray(text)
        self.text = text

    def ascii(self, canvas):
        """Processes image and extracts values for ASCII based text art
        """
        charset = self.configuration.charsets[self.args.charset]
        if self.args.negative:
            charset = charset[::-1]
        canvas = normalize(canvas, None, 0, len(charset) - 1, NORM_MINMAX)
        self.text = vectorize(lambda x: charset[x])(canvas)