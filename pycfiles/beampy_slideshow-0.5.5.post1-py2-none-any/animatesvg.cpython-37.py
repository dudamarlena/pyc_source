# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/animatesvg.py
# Compiled at: 2018-12-06 13:33:31
# Size of source mod 2**32: 5180 bytes
"""
Created on Sun Oct 25 19:05:18 2015

@author: hugo

Class to manage text for beampy
"""
from beampy import document
import beampy.modules.figure as figure
from beampy.modules.core import beampy_module
from beampy.functions import convert_unit, gcs
import glob, re, sys

class animatesvg(beampy_module):
    __doc__ = "\n    Create svg animation from a folder containing svg files (or any files that\n    figure function can handle) or a list of matplotlib figures.\n\n    Parameters\n    ----------\n\n    files_in : str or list of matplotlib figures or list of file names\n        List of figures to animate. List could be generated using a string\n        containing UNIX willcard like '/my/folder/*.svg', or using a list of\n        file names or matplotlib figure object.\n\n    x : int or float or {'center', 'auto'} or str, optional\n        Horizontal position for the animation (the default theme sets this to\n        'center'). See positioning system of Beampy.\n\n    y : int or float or {'center', 'auto'} or str, optional\n        Vertical position for the animation (the default theme sets this to\n        'auto'). See positioning system of Beampy.\n\n    start : integer, optional\n        Start position of the image sequence (the default theme sets this to\n        0).\n\n    end : int or 'end', optional\n        End position of the image sequence (the default theme sets this to\n        'end', which implies that the animation end at the last item of the\n        files_in ).\n\n    width : int or float or None, optional\n        Width of the figure (the default is None, which implies that the width\n        is width of the image).\n\n    fps : int, optional\n        Animation frame-rate (the default theme sets this to 25).\n\n    autoplay : boolean, optional\n        Automatically start the animation when the slide is shown on screen\n        (the default theme sets this to False).\n\n    "

    def __init__(self, files_in, **kwargs):
        self.type = 'animatesvg'
        self.check_args_from_theme(kwargs)
        self.cache = False
        slide = document._slides[gcs()]
        self.anim_num = slide.cpt_anim
        slide.cpt_anim += 1
        input_width = self.width
        if self.width is None:
            self.width = slide.curwidth
        if isinstance(files_in, str):
            svg_files = glob.glob(files_in)
            svg_files = sorted(svg_files, key=(lambda x: int(''.join(re.findall('\\d+', x)))))
        else:
            if isinstance(files_in, list):
                svg_files = files_in
                if input_width is None:
                    width_inch, height_inch = files_in[0].get_size_inches()
                    self.width = convert_unit('%fin' % width_inch)
            else:
                print('Unknown input type for files_folder')
                sys.exit(0)
        if self.end == 'end':
            self.end = len(svg_files)
        self.content = svg_files[self.start:self.end]
        self.register()

    def render(self):
        """
            Render several images as an animation in html
        """
        svgcontent = []
        output = []
        fig_args = {'width':self.width.value, 
         'height':self.height.value, 
         'x':0, 
         'y':0}
        if len(self.content) > 0:
            if document._output_format == 'html5':
                for iframe, svgfile in enumerate(self.content):
                    img = figure(svgfile, **fig_args)
                    img.positionner = self.positionner
                    img.call_cmd = str(iframe) + '->' + self.call_cmd.strip()
                    img.call_lines = self.call_lines
                    img.run_render()
                    if iframe == 0:
                        self.update_size(img.width, img.height)
                    tmpout = '<g id="frame_%i">%s</g>' % (iframe, img.svgout)
                    output += [tmpout]
                    img.delete()

                self.animout = output
            else:
                img = figure((self.content[0]), **fig_args)
                img.positionner = self.positionner
                img.render()
                self.update_size(img.width, img.height)
                self.svgout = img.svgout
                img.delete()
            self.rendered = True
        else:
            print('nothing found')