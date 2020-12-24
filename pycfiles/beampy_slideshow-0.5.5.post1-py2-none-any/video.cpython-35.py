# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/video.py
# Compiled at: 2019-04-18 17:10:33
# Size of source mod 2**32: 6268 bytes
"""
Created on Sun Oct 25 19:05:18 2015

@author: hugo

Class to manage text for beampy
"""
from beampy import document
from beampy.modules.core import beampy_module, gcs
import base64, os
try:
    from cStringIO import StringIO
except:
    from io import BytesIO as StringIO

from PIL import Image
import sys, subprocess

class video(beampy_module):
    __doc__ = "\n    Include a figure to the current slide. Figure formats could be (**svg**,\n    **pdf**, **png**, **jpeg**, **matplotib figure**, and **bokeh figure**)\n\n    Parameters\n    ----------\n\n    content : str or matplotlib.figure or bokeh.figure\n        Figure input source. To load file, `content` is the path to the file.\n        For matplotlib and bokeh, `content` is the python object figure of\n        either matplotlib or bokeh.\n\n    ext : {'svg','jpeg','png','pdf','bokeh','matplotlib'} or None, optional\n       Image format defined as string (the default value is None, which implies\n       that the image format is guessed from file or python object name.\n\n    x : int or float or {'center', 'auto'} or str, optional\n        Horizontal position for the figure (the default is 'center').\n\n    y : int or float or {'center', 'auto'} or str, optional\n        Vertical position for the figure (the default is 'auto', which implies\n        equal blank width between 'auto' positioned elements)\n\n    width : int or float or None, optional\n        Width of the figure (the default is None, which implies that the width\n        is width of the image).\n\n    "

    def __init__(self, videofile, **kwargs):
        """
        Add video in webm/ogg/mp4 format

        arguments
        ---------

        width = None -> document._width
        heigh = None -> document._height

        x ['center']: x position
        y ['auto']: y position

        autoplay [False]: To launch video when slide appears

        control [True]: Display video control bar

        still_image_time [0]: extract the still image for pdf export at the given still_image_time in second
        """
        self.type = 'html'
        self.check_args_from_theme(kwargs)
        if self.width is None:
            self.width = document._slides[gcs()].curwidth
        self.ext = None
        if '.webm' in videofile.lower():
            self.ext = 'webm'
        else:
            if '.ogg' in videofile.lower() or '.ogv' in videofile.lower():
                self.ext = 'ogg'
            else:
                if '.mp4' in videofile.lower():
                    self.ext = 'mp4'
                else:
                    print('Video need to be in webm/ogg/mp4(h.264) format!')
                    sys.exit(0)
        if self.ext is not None:
            self.content = videofile
        self.args_for_cache_id = [
         'width', 'still_image_time', 'embedded']
        fdate = str(os.path.getmtime(self.content))
        self.args['filedate'] = fdate
        self.filedate = fdate
        self.args_for_cache_id += ['filedate']
        self.register()

    def render(self):
        """
        Render video (webm) encoded in base64 in svg command

        Render Need to produce an html and an svg
        """
        if self.embedded:
            with open(self.content, 'rb') as (fin):
                videob64 = base64.b64encode(fin.read()).decode('utf8')
        size, imgframe = self.video_image()
        _, _, vidw, vidh = size
        scale_x = (self.width / float(vidw)).value
        width = self.width
        if self.height.value is None:
            height = vidh * scale_x
            print('Video size might be buggy, estimated height %ipx' % height)
        else:
            height = self.height.value
        if self.embedded:
            videosrc = 'data:video/{ext};base64, {b64data}'.format(ext=self.ext, b64data=videob64)
        else:
            videosrc = self.content
        output = '<video id=\'video\' width="{width}px" {otherargs}><source type="video/{ext}" src="{src}"></video>'
        otherargs = ''
        if self.autoplay == True:
            otherargs += ' autoplay'
        if self.control == True:
            otherargs += ' controls="controls"'
        else:
            otherargs += ' onclick="this.paused?this.play():this.pause();"'
        output = output.format(width=width, otherargs=otherargs, ext=self.ext, src=videosrc)
        self.htmlout = output
        imgframe = base64.b64encode(imgframe).decode('utf8')
        output = '<image x="0" y="0" width="%s" height="%s" xlink:href="data:image/jpg;base64, %s" />' % (str(width), str(height), imgframe)
        self.svgout = output
        self.update_size(width, height)
        self.rendered = True

    def video_image(self):
        """
            Function used to get the first image of a video

            It use FFMPEG to extract one image
        """
        FFMPEG_CMD = document._external_cmd['video_encoder']
        FFMPEG_CMD += ' -loglevel 8 -i "%s" -f image2 -ss %0.3f -vframes 1 -; exit 0' % (self.content, self.still_image_time)
        run_ffmpeg = subprocess.check_output(str(FFMPEG_CMD), shell=True)
        img_out = run_ffmpeg
        img = StringIO(img_out)
        out = Image.open(img)
        size = out.getbbox()
        outimg = StringIO()
        out.save(outimg, 'JPEG')
        out.close()
        strimg = outimg.getvalue()
        outimg.close()
        img.close()
        return (
         size, strimg)