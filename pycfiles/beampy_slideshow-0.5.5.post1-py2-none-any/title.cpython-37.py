# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/beampy_git/beampy/modules/title.py
# Compiled at: 2019-05-17 13:59:39
# Size of source mod 2**32: 1059 bytes
"""
Created on Sun Oct 25 19:05:18 2015

@author: hugo

Class to manage text for beampy
"""
from beampy import document
from beampy.functions import gcs
import beampy.modules.text as text

class title(text):

    def __init__(self, titlein, **kwargs):
        """
            Add a title to a slide
        """
        self.type = 'text'
        self.check_args_from_theme(kwargs)
        self.content = titlein
        self.svgtext = ''
        self.load_extra_args('text')
        self.args_for_cache_id = [
         'color', 'size']
        if self.width == None:
            self.width = document._width
        self.height = None
        self.register()
        document._slides[self.slide_id].title = self