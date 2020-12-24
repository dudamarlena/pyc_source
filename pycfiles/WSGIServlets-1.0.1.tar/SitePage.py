# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/SitePage.py
# Compiled at: 2011-11-02 16:42:49
from TutorialBase import *

class SitePage(HTMLPage):
    simulate_modification = False

    def write_body_parts(self):
        if self.simulate_modification:
            self.writeln('<div id="banner">')
            self.write_banner()
            self.writeln('</div>')
        self.writeln('<div id="sidebar">')
        self.write_sidebar()
        self.writeln('</div>')
        self.writeln('<div id="content">')
        self.write_content()
        self.writeln('</div>')

    def write_sidebar(self):
        self.writeln('<ol>')
        for tutorial in TutorialBase.tutorials:
            if tutorial == self.__class__.__name__:
                li = tutorial
            else:
                li = ('<a href=/{t}>{t}</a>').format(t=tutorial)
            self.writeln(('<li>{li}</li>').format(li=li))

        self.writeln('</ol>')

    def write_banner(self):
        self.writeln('WSGIServlets Tutorial')