# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sam/Documents/fall17/mathviz/mathviz_hopper/src/test.py
# Compiled at: 2017-11-28 23:03:57
"""
Author: Sam Helms
Date: Nov 8

Playing around with ipython settings

"""
from IPython.display import display, HTML
from helpers import get_cur_path
import os, re, shutil
HTML_PATH = '/viz'

class Test:

    def __init__(self):
        print 'creating test instance'
        self.cur_path = os.path.dirname(os.path.abspath(__file__))

    def __del__(self):
        shutil.rmtree('viz')

    def print_html(self):
        """
        "prints" a javascript visualization that can be run in the browser
        (or TODO: a jupyter notebook cell) and initializes listening on a
        port to serve data to the viz.
        """
        try:
            shutil.rmtree('viz')
        except:
            None

        shutil.copytree('/Users/sam/Documents/fall17/mathviz/mathviz_hopper/webpage/mathviz-js-components/build/', 'viz')
        pth = 'viz/index.html'
        html = open(pth).read()
        display(HTML(html))
        return