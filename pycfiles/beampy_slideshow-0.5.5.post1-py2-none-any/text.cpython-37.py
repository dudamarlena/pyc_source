# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/text.py
# Compiled at: 2019-07-07 12:54:09
# Size of source mod 2**32: 15720 bytes
"""
Created on Sun Oct 25 19:05:18 2015

@author: hugo

Class to manage text for beampy
"""
from beampy import document
from beampy.functions import gcs, color_text, getsvgwidth, getsvgheight, small_comment_parser, latex2svg
from beampy.modules.core import beampy_module
import tempfile, os
from bs4 import BeautifulSoup
import sys, hashlib, logging

class text(beampy_module):
    __doc__ = "\n    Add text to the current slide. Input text is by default processed using\n    Latex and could use Latex syntax.\n\n    Parameters\n    ----------\n\n    textin : str, optional\n        Text to add. Could contain latex syntax with protected slash either by\n        using double slash or by using the python **r** before string.\n\n        >>> text(r'\\sqrt{x}')\n\n    x : int or float or {'center', 'auto'} or str, optional\n        Horizontal position for the text container (the default is 'center').\n        See positioning system of Beampy.\n\n    y : int or float or {'center', 'auto'} or str, optional\n        Vertical position for the text container (the default is 'auto'). See\n        positioning system of Beampy.\n\n    width : int or float or None, optional\n       Width of the text container (the default is None, which implies that the\n       width is the parent group with).\n\n    size : int, optional\n        The font size (the default theme sets this value to 20).\n\n    font : str, optional\n        The Tex font (the default theme sets this value to\n        'CMR'). **THIS IS NOT YET IMPLEMENTED!**\n\n    color : str, optional\n        The text color (the default theme set this value to '#000000'). Color\n        could be html hex values or SVG-COLOR-NAMES.\n\n    usetex : bool, optional\n        Use latex to render text (the default value is true). Latex render\n        could be turned off using `usetex`=False, then the text is rendered as\n        svg.\n\n    va : {'','baseline'}, optional\n       Vertical text alignment (the default value is '', which implies that the\n       alignment reference is the top-left corner of text). When\n       `va`='baseline', the base-line of the first text row is computed and\n       used as alignment reference (baseline-left).\n\n    extra_packages : list of string, optional\n        Add latex packages to render the text, like\n        [r'\\usepackage{name1}', r'\\usepackage{name2}']\n\n\n    Example\n    -------\n\n    >>> text('this is my text', x='20', y='20')\n\n    "

    def __init__(self, textin=None, **kwargs):
        self.type = 'text'
        self.check_args_from_theme(kwargs)
        self.content = textin
        self.svgtext = ''
        self.height = None
        if self.width is None:
            self.width = document._slides[gcs()].curwidth
        else:
            self.initial_width = self.width
            self.args_for_cache_id = ['initial_width', 'color', 'size', 'align', 'opacity']
            if 'svg_glyphs' not in document._contents:
                document._contents['svg_glyphs'] = {}
            if self.extra_packages != []:
                auto_render = True
            else:
                auto_render = False
        self.register(auto_render=auto_render)

    def process_with(self):
        """
        Process the text inside the width
        """
        source = document._source_code.source(start=(self.start_line), stop=(self.stop_line))
        input_texts = small_comment_parser(source)
        self.content = '\\\\'.join(['%s' % t for t in input_texts])

    def pre_render(self):
        """
        Prepare the latex render of the text 
        """
        if self.usetex:
            if hasattr(self, 'color'):
                textin = color_text(self.content, self.color)
            else:
                textin = self.content
            if 'center' in self.align:
                texalign = '\\centering'
            else:
                if 'right' in self.align:
                    texalign = '\\flushright'
                else:
                    texalign = ''
            template = '\\begin{varwidth}{%ipt}\n            %s\n            \\fontsize{%i}{%i}\\selectfont %s\n\n            \\end{varwidth}'
            self.latex_text = template % (self.width.value * 0.7528125,
             texalign, self.size,
             self.size + self.size * 0.1,
             textin)
        else:
            self.latex_text = ''

    def local_render(self):
        """Function to render only on text of this module. 

        It's slower than writing all texts to one latex file and then
        render it to dvi then svg.
        """
        if self.latex_text != '':
            pretex = '\n            \\documentclass[crop=true]{standalone}\n            \\usepackage[utf8x]{inputenc}\n            \\usepackage{fix-cm}\n            \\usepackage[hypertex]{hyperref}\n            \\usepackage[svgnames]{xcolor}\n            \\renewcommand{\\familydefault}{\\sfdefault}\n            \\usepackage{varwidth}\n            \\usepackage{amsmath}\n            \\usepackage{amsfonts}\n            \\usepackage{amssymb}\n            '
            pretex += '\n'.join(self.extra_packages + document._latex_packages)
            pretex += '\\begin{document}'
            pretex += self.latex_text
            pretex += '\\end{document}'
            self.svgtext = latex2svg(pretex)
        else:
            self.svgtext = ''

    def render(self):
        """
            Text is rendered using latex if self.usetex = True if not use simple svg
        """
        if self.usetex:
            if self.svgtext == '':
                self.local_render()
                if self.svgtext == '':
                    print('Latex Compilation Error')
                    print('Beampy Input:')
                    print(self.content)
                    sys.exit(0)
            else:
                soup = BeautifulSoup(self.svgtext, 'xml')
                svgsoup = soup.find('svg')
                xinit, yinit, text_width, text_height = svgsoup.get('viewBox').split()
                text_width = float(text_width)
                text_height = float(text_height)
                if 'path' not in document._global_counter:
                    document._global_counter['path'] = 0
                svgsoup = self.parse_dvisvgm_svg(svgsoup)
                links = svgsoup.find_all('a')
                style = ' '.join(['%s:%s;' % (str(key), str(value)) for key, value in list(document._theme['link'].items())])
                for link in links:
                    link['style'] = style

                try:
                    uses = svgsoup.find_all('use')
                except:
                    print(soup)

            if len(uses) > 0:
                baseline = 0
                for use in uses:
                    if use.has_attr('y'):
                        baseline = float(use.get('y'))
                        break

                if baseline == 0:
                    print('No Baseline found in TeX and is put to 0')
                g = svgsoup.find('g')
                transform_matrix = g.get('transform')
                if getattr(self, 'va', False) and self.va == 'baseline':
                    yoffset = -float(baseline)
                    xoffset = -float(xinit)
                    oldyinit = yinit
                    yinit = -float(baseline) + float(yinit)
                    baseline = -float(oldyinit) + float(baseline)
                else:
                    yoffset = -float(yinit)
                    xoffset = -float(xinit)
                    baseline = -float(yinit) + float(baseline)
                    yinit = 0
                tex_pt_to_px = 1.3283520132835203
                newmatrix = 'scale(%0.3f) translate(%0.1f,%0.1f)' % (tex_pt_to_px, xoffset, yoffset)
                g['transform'] = newmatrix
                text_width = text_width * tex_pt_to_px
                text_height = text_height * tex_pt_to_px
                baseline = baseline * tex_pt_to_px
                yinit = yinit * tex_pt_to_px
                g['opacity'] = self.opacity
            output = svgsoup.renderContents().decode('utf8', errors='replace')
            if document._text_box:
                boxed = '<g transform="translate(%0.1f,%0.1f)">\n                <line x1="0" y1="0" x2="%i" y2="0" style="stroke: red"/>\n                <line x1="%i" y1="0" x2="%i" y2="%i" style="stroke: red"/>\n                <line x1="%i" y1="%i" x2="0" y2="%i" style="stroke: red"/>\n                <line x1="0" y1="%i" x2="0" y2="0" style="stroke: red"/>\n                <line x1="0" y1="%i" x2="%i" y2="%i" style="stroke: green"/>\n                </g>'
                output += boxed % (0, float(yinit),
                 text_width,
                 text_width, text_width, text_height,
                 text_width, text_height, text_height,
                 text_height,
                 baseline, text_width, baseline)
        else:
            textin = self.content
            style = ''
            if hasattr(self, 'color'):
                style += 'color:%s' % self.color
            output = '<text style="%s">%s</text>' % (style, textin.decode('utf-8'))
            tmpsvg = '<svg xmlns="http://www.w3.org/2000/svg" version="1.2" baseProfile="tiny" xmlns:xlink="http://www.w3.org/1999/xlink">%s</svg>' % output
            with tempfile.NamedTemporaryFile(mode='w', suffix='.svt', prefix='beampytmp') as (f):
                f.write(tmpsvg)
                f.file.flush()
                text_width = getsvgwidth(f.name)
                text_height = getsvgheight(f.name)
        self.update_size(text_width, text_height)
        logging.debug(type(output))
        self.svgout = output
        self.rendered = True

    def parse_dvisvgm_svg(self, soup_data):
        """
        Function to transform the svg produced by dvisvgm. 
        Make a global glyph store to use them as defs in svg 
        to reduce the size off the global presentation.

        soup_data: BeautifulSoup parsed svg

        return: soup_data (without the defs part)
        """
        if 'glyphs' not in document._global_store:
            document._global_store['glyphs'] = {}
        defs = soup_data.find_all('defs')[0].extract()
        for path in defs.find_all('path'):
            path_id = path['id']
            path_d = path['d']
            try:
                hash_id = hashlib.md5(path_d).hexdigest()
            except:
                hash_id = hashlib.md5(path_d.encode('utf8')).hexdigest()

            if hash_id not in document._global_store['glyphs']:
                uniq_id = 'g_' + str(len(document._global_store['glyphs']))
                new_svg = "<path d='%s' id='%s'/>" % (path_d, uniq_id)
                document._global_store['glyphs'][hash_id] = {'old_id':path_id,  'd':path_d,  'id':uniq_id,  'svg':new_svg}
            else:
                data_store = document._global_store['glyphs'][hash_id]
                uniq_id = data_store['id']
            for tag in soup_data.find_all('use', {'xlink:href': '#%s' % path_id}):
                tag['xlink:href'] = '#%s' % uniq_id

            for use in defs.find_all('use', {'xlink:href': '#%s' % path_id}):
                u_id = use['id']
                use_id = 'g_' + str(len(document._global_store['glyphs']))
                use['id'] = use_id
                use['xlink:href'] = '#%s' % uniq_id
                document._global_store['glyphs'][use_id] = {'old_id':u_id,  'id':use_id,  'svg':str(use)}
                for tag in soup_data.find_all('use', {'xlink:href': '#%s' % u_id}):
                    tag['xlink:href'] = '#%s' % use_id

        for tag in soup_data.findAll(lambda x: x.name != 'a' and x is not None and x.has_attr('xlink:href')):
            if '-' in tag['xlink:href']:
                print('A svg reference is not defined:')
                print(tag)
                print('This is a bug in multipage of your dvisvgm version (bug fix in dvisvgm version > 2.7.2)')
                print('Run a single render for this text and parse it again! this should fix missings')
                self.local_render()
                self.render()

        return soup_data