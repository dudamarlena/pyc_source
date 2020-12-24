# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/tikz.py
# Compiled at: 2019-04-17 16:48:53
# Size of source mod 2**32: 4631 bytes
"""
Created on Sun Oct 25 19:05:18 2015

@author: hugo

Class to manage tikz image for beampy
"""
from beampy import document
from beampy.functions import gcs, latex2svg
from beampy.modules.core import beampy_module
from bs4 import BeautifulSoup

class tikz(beampy_module):
    __doc__ = "\n    Add Tikz/pgf graphic to the slide. \n\n    Parameters\n    ----------\n\n    tikzcmd : string\n        String containing the main Tikz commands contained between\n        \\begin{tikzpicture} and \\end{}tikzpicture}.\n\n    x : int or float or {'center', 'auto'} or str, optional\n        Horizontal position for the Tikz graphic (the default theme set this to\n        0). See positioning system of Beampy.\n\n    y : int or float or {'center', 'auto'} or str, optional\n        Vertical position for the Tikz graphic (the default theme sets this to 0).\n        See positioning system of Beampy.\n\n    tikz_header : str or None, optional\n        Add extra Tiks/pgf libraries and style (Tiks commands \\usetikzlibrary\n        and \\tickstyle), everything that is included befor \x08egin{document}\n        (the default theme sets this to None).\n\n    tex_packages : list of string or None, optional\n        Add extra Tex packages that are included using the \\usepackages (the\n        default theme set this to None). The list should only contains the name\n        of tex packages as strings.\n\n        >>> tex_packages = ['xolors','tikz-3dplot']\n\n    figure_options : string or None,\n        Tikz options added just after: \x08egin{tikzpicture}[options] (the default\n        theme sets this to None).\n\n    figure_anchor : {'top_left' or 'top_right' or 'bottom_left' or 'bottom_right' }, optional\n        Anchor of the svg produced by Tikz.\n\n    "

    def __init__(self, tikzcmd, **kwargs):
        self.type = 'svg'
        self.content = tikzcmd
        self.check_args_from_theme(kwargs)
        self.args_for_cache_id = [
         'figure_options', 'tex_packages', 'tikz_header']
        self.register()

    def render(self):
        """
            Latex -> dvi -> svg for tikz image
        """
        tikzcommands = self.content
        tex_pt_to_px = 1.3283520132835203
        tiktikzcommands = tikzcommands.replace('\\slidewidth', '%ipt' % (0.75 * document._slides[gcs()].curwidth))
        if getattr(self, 'tex_packages', False):
            extra_tex_packages = '\n'.join(['\\usepackages{%s}' % pkg for pkg in self.tex_packages])
        else:
            extra_tex_packages = ''
        if getattr(self, 'tikz_header', False):
            extra_tex_packages += '\n%s' % self.tikz_header
        if getattr(self, 'figure_options', False):
            tikz_fig_opts = '[' + self.figure_options + ']'
        else:
            tikz_fig_opts = ''
        pretex = '\n        \\documentclass[tikz,svgnames]{standalone}\n        \\usepackage[utf8x]{inputenc}\n\n        %s\n\n        \\begin{document}\n            \\begin{tikzpicture}%s\n            %s\n            \\end{tikzpicture}\n        \\end{document}\n        ' % (extra_tex_packages, tikz_fig_opts, tikzcommands)
        svgout = latex2svg(pretex, write_tmpsvg=True)
        if svgout != '':
            soup = BeautifulSoup(svgout, 'xml')
            svgsoup = soup.find('svg')
            g = soup.find('g')
            xinit, yinit, tikz_width, tikz_height = svgsoup.get('viewBox').split()
            tikz_width = float(tikz_width) * tex_pt_to_px
            tikz_height = float(tikz_height) * tex_pt_to_px
            dx = -float(xinit)
            dy = -float(yinit)
            if 'bottom' in self.figure_anchor:
                self.positionner.y['anchor'] = 'bottom'
            if 'right' in self.figure_anchor:
                self.positionner.x['anchor'] = 'right'
            newmatrix = 'scale(%0.3f) translate(%0.1f,%0.1f)' % (tex_pt_to_px, dx, dy)
            g['transform'] = newmatrix
            output = str(svgsoup.renderContents())
        else:
            output = ''
            tikz_height = 0
            tikz_width = 0
        self.update_size(tikz_width, tikz_height)
        self.svgout = output
        self.rendered = True