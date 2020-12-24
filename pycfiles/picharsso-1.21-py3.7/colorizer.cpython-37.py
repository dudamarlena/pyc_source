# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/picharsso/colorizer.py
# Compiled at: 2019-11-08 16:27:15
# Size of source mod 2**32: 1272 bytes
from numpy import ones, vectorize
from numpy.lib.recfunctions import unstructured_to_structured
from cv2 import filter2D
from sty import fg

class Colorizer:
    __doc__ = 'A wrapper for colorizing text\n    '

    def colorize(self):
        """Colors text obtained from processing
        """
        if self.args.color:
            hr = int(round(self.image.shape[0] / self.text.shape[0]))
            wr = int(round(self.image.shape[1] / self.text.shape[1]))
            kernel = ones((hr, wr), dtype=float) / (hr * wr)
            colors = unstructured_to_structured(filter2D(self.image, -1, kernel)[::hr, ::wr, :]).astype('O')
            self.text = vectorize(self.color)(self.text, colors)

    def color(self, text, color):
        """Colors text
        
        Parameters
        ----------
        text : str
            Text to be colored
        color : tuple
            RGB values
        
        Returns
        -------
        str
            Colored text
        """
        output = {'ansi':lambda x, y: f"{fg(*y)}{x}{fg.rs}", 
         'html':lambda x, y: f'<span style="color : rgb{tuple(y)};">{x}</span>'}
        return output.get(self.args.output_type)(text, color)