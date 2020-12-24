# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/fini.py
# Compiled at: 2011-11-02 16:42:14
from TutorialBase import *

class fini(HTMLPage):
    """Proselytizing with an example."""
    title = 'Fini'
    js_src = [
     '/fini.js']
    css_links = ['/fini.css']

    def write_content(self):
        self.writeln(OVERVIEW)
        self.writeln('<div id="thumbnails">')
        for tut in TutorialBase.tutorials[:-1]:
            self.write(IMG.format(t=tut))

        self.writeln('</div>')


OVERVIEW = make_overview('\nI wrote WSGIServlets because I believe strongly in the power of object\noriented programming, generally, and how it can be applied to web\napplication programming, specifically.  Combining OOP techniques with\nweb technologies which promote separation of form (css) and logic\n(javascript) from content, WSGIServlets offers a very powerful tool to\nquickly prototype and develop rich web applications.\n\nAs a small example of this power I leave you with this servlet which\nshows every other servlet in this tutorial.  Click on one of the\nimages and a popup will appear running that servlet.  View the source\nof this page...excluding the textual content and underlying\ncss/javascript, there are about 10 lines of python code.  \n\n<hr>\n\n<div id="mask">\n    <div id="container">\n        <span id="close" onclick="popUpClose()">X</span>\n        <iframe src="about:blank" id="popup"></iframe>\n    </div>\n</div>\n')
IMG = '<IMG width="350" height="200" onclick="popUp(\'brief_{t}\')" src=/thumbnails/{t}.png/ alt="{t} thumbnail">'