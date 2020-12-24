# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/figure.py
# Compiled at: 2019-07-06 06:47:04
"""
Created on Sun Oct 25 19:05:18 2015

@author: hugo
"""
from beampy import document
from beampy.functions import convert_unit, optimize_svg, gcs, make_global_svg_defs, getsvgwidth, getsvgheight, convert_pdf_to_svg, guess_file_type
from beampy.modules.core import beampy_module
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO, StringIO
import hashlib, base64, tempfile, os, sys
try:
    import bokeh
    print 'found bokeh version %s' % bokeh.__version__
    from bokeh.embed import components
except:
    pass

class figure(beampy_module):
    """
    Include a figure to the current slide. Figure formats could be (**svg**,
    **pdf**, **png**, **jpeg**, **gif**, **matplotib figure**, 
    and **bokeh figure**)

    Parameters
    ----------

    content : str or matplotlib.figure or bokeh.figure
        Figure input source. To load file, `content` is the path to the file.
        For matplotlib and bokeh, `content` is the python object figure of
        either matplotlib or bokeh.

    ext : {'svg','jpeg','png','pdf', 'gif', 'bokeh','matplotlib'} or None, optional 
       Image format defined as string (the default value is None,
       which implies that the image format is guessed from file or
       python object name.

    x : int or float or {'center', 'auto'} or str, optional
        Horizontal position for the figure (the default is 'center').

    y : int or float or {'center', 'auto'} or str, optional
        Vertical position for the figure (the default is 'auto', which implies
        equal blank width between 'auto' positioned elements)

    width : int or float or None, optional
        Width of the figure (the default is None, which implies that the width
        is width of the image).

    """

    def __init__(self, content, ext=None, **kwargs):
        self.type = 'svg'
        self.check_args_from_theme(kwargs)
        self.ext = ext
        self.content = content
        self.args_for_cache_id = [
         'width', 'ext']
        if isinstance(self.content, str):
            self.ext = guess_file_type(self.content, self.ext)
        else:
            if 'bokeh' in str(type(self.content)):
                self.ext = 'bokeh'
            if 'matplotlib' in str(type(self.content)):
                self.ext = 'matplotlib'
        if self.ext is None:
            print "figure format can't be guessed."
            sys.exit(1)
        if self.ext == 'bokeh':
            self.type = 'html'
            if self.width is None:
                self.width = int(self.content.plot_width)
            if self.height is None:
                self.height = int(self.content.plot_height)
            self.cache = False
        if self.ext == 'matplotlib':
            from matplotlib.pyplot import close
            close(self.content)
            if self.width is None:
                width_inch, height_inch = self.content.get_size_inches()
                self.width = convert_unit('%fin' % width_inch)
            with BytesIO() as (tmpb):
                self.content.canvas.print_jpg(tmpb)
                tmpb.seek(0)
                md5t = hashlib.md5(tmpb.read()).hexdigest()
            self.args['mpl_fig_hash'] = md5t
            self.mpl_fig_hash = md5t
            self.args_for_cache_id += ['mpl_fig_hash']
        if self.ext not in ('matplotlib', 'bokeh'):
            fdate = str(os.path.getmtime(self.content))
            self.args['filedate'] = fdate
            self.filedate = fdate
            self.args_for_cache_id += ['filedate']
            if self.width is None:
                self.width = document._slides[gcs()].curwidth
        self.register()
        return

    def render(self):
        """
            function to render figures
        """
        if self.ext in ('svg', 'pdf', 'matplotlib'):
            if self.ext == 'pdf':
                figurein = convert_pdf_to_svg(self.content)
            elif self.ext == 'matplotlib':
                with StringIO() as (tmpf):
                    self.content.savefig(tmpf, bbox_inches='tight', format='svg')
                    tmpf.seek(0)
                    figurein = tmpf.read().encode('utf-8')
            elif os.path.isfile(self.content):
                with open(self.content, 'r') as (f):
                    figurein = f.read()
            else:
                figurein = self.content
            if document._optimize_svg:
                figurein = optimize_svg(figurein)
            soup = BeautifulSoup(figurein, 'xml')
            soup = make_global_svg_defs(soup)
            if document._resize_raster:
                imgs = soup.findAll('image')
                if imgs:
                    for img in imgs:
                        width, height = int(float(img['width'])), int(float(img['height']))
                        img_ratio = height / float(width)
                        b64content = img['xlink:href']
                        try:
                            in_img = BytesIO(base64.b64decode(b64content.split(';base64,')[1]))
                            tmp_img = Image.open(in_img)
                            out_img = resize_raster_image(tmp_img, max_width=self.positionner.width.value)
                            out_b64 = base64.b64encode(out_img.read()).decode('utf8')
                            img['xlink:href'] = 'data:image/%s;base64, %s' % (tmp_img.format.lower(), out_b64)
                        except:
                            print 'Unable to reduce the image size'

            svgtag = soup.find('svg')
            svg_viewbox = svgtag.get('viewBox')
            tmph = svgtag.get('height')
            tmpw = svgtag.get('width')
            if tmph is None or tmpw is None:
                with tempfile.NamedTemporaryFile(mode='w', prefix='beampytmp', suffix='.svg') as (f):
                    try:
                        f.write(figurein)
                    except Exception as e:
                        f.write(figurein.encode('utf8'))

                    f.file.flush()
                    tmph = getsvgheight(f.name)
                    tmpw = getsvgwidth(f.name)
            svgheight = convert_unit(tmph)
            svgwidth = convert_unit(tmpw)
            if svg_viewbox is not None:
                svgheight = svg_viewbox.split(' ')[3]
                svgwidth = svg_viewbox.split(' ')[2]
            scale_x = (self.positionner.width / float(svgwidth)).value
            good_scale = scale_x
            tmpfig = svgtag.renderContents().decode('utf8')
            tmphead = '\n<g transform="scale(%0.5f)">' % good_scale
            output = tmphead + tmpfig + '</g>\n'
            figure_height = float(svgheight) * good_scale
            figure_width = self.width.value
            self.update_size(figure_width, figure_height)
            self.svgout = output
        if self.ext == 'bokeh':
            self.content.sizing_mode = 'scale_both'
            figscript, figdiv = components(self.content, wrap_script=False)
            tmp = figscript.splitlines()
            goodscript = ('\n').join(['["load_bokeh"] = function() {'] + tmp[1:-1] + ['};\n'])
            self.htmlout = "<div id='bk_resizer' width='{width}px' height='{height}px' style='width: {width}px; height: {height}px; transform-origin: left top 0px;'> {html} </div>"
            self.htmlout = self.htmlout.format(width=self.positionner.width, height=self.positionner.height, html=figdiv)
            self.jsout = goodscript
        if self.ext in ('png', 'jpeg', 'gif'):
            tmp_img = Image.open(self.content)
            _, _, tmpwidth, tmpheight = tmp_img.getbbox()
            scale_x = (self.positionner.width / float(tmpwidth)).value
            figure_height = float(tmpheight) * scale_x
            figure_width = self.positionner.width.value
            if document._resize_raster:
                if self.ext == 'gif':
                    print 'Gif are not resized, the original size is taken!'
                    with open(self.content, 'rb') as (f):
                        figurein = base64.b64encode(f.read()).decode('utf8')
                else:
                    out_img = resize_raster_image(tmp_img, max_width=self.positionner.width.value)
                    figurein = base64.b64encode(out_img.read()).decode('utf8')
                    out_img.close()
            else:
                with open(self.content, 'rb') as (f):
                    figurein = base64.b64encode(f.read()).decode('utf8')
            tmp_img.close()
            if self.ext == 'png':
                output = '<image x="0" y="0" width="%s" height="%s" xlink:href="data:image/png;base64, %s" />' % (figure_width,
                 figure_height,
                 figurein)
            if self.ext == 'jpeg':
                output = '<image x="0" y="0" width="%s" height="%s" xlink:href="data:image/jpg;base64, %s" />' % (figure_width,
                 figure_height,
                 figurein)
            if self.ext == 'gif':
                output = '<image x="0" y="0" width="%s" height="%s" xlink:href="data:image/gif;base64, %s" />' % (figure_width,
                 figure_height,
                 figurein)
            self.update_size(figure_width, figure_height)
            self.svgout = output
        self.rendered = True
        return


def resize_raster_image(PILImage, max_width=document._width, jpegqual=96):
    """
    Function to reduce the size of a given image keeping it's aspect ratio
    """
    img_w, img_h = PILImage.size
    img_ratio = img_h / float(img_w)
    if img_w > document._width:
        print 'Image resized from (%ix%i)px to (%ix%i)px' % (img_w, img_h, max_width, max_width * img_ratio)
        width = int(max_width)
        height = int(max_width * img_ratio)
        tmp_resized = PILImage.resize((width, height), Image.ANTIALIAS)
    else:
        tmp_resized = PILImage
    if tmp_resized.mode == 'RGBA':
        Amin, Amax = tmp_resized.getextrema()[(-1)]
        if Amin == Amax:
            print 'Remove useless Alpha layer'
            tmp_resized = tmp_resized.convert(mode='RGB')
    out_img = BytesIO()
    tmp_resized.save(out_img, PILImage.format, quality=jpegqual, optimize=True)
    out_img.seek(0)
    return out_img