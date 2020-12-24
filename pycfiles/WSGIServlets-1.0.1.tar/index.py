# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/index.py
# Compiled at: 2011-11-04 14:49:41
from wsgiservlets import *
from TutorialBase import TutorialBase, markdown

class index(HTMLPage):
    title = 'WSGIServlets Tutorial'
    css_links = ['/tutorial.css']

    def write_content(self):
        dispatcher = self.environ['wsgiservlets.dispatcher']
        self.write(OVERVIEW)
        self.writeln('<table id="toc">')
        for (i, tutorial) in enumerate(TutorialBase.tutorials):
            klass = dispatcher.servlet_mapping[tutorial][0]
            docstring = klass.toc_summary()
            link = ('<a href="/{t}">{t}</a>').format(t=tutorial)
            tr = '<tr class="odd">' if (i + 1) % 2 else '<tr>'
            self.writeln(tr, '<td class="num">', i + 1, '</td>', '<td class="link">', link, '</td>', '<td class="summary">', docstring, '</td></tr>')

        self.writeln('</table>')


OVERVIEW = markdown('\n\n# WSGIServlets Tutorial\n\nWelcome to the WSGIServlets tutorial!\n\nIf you are new to WSGIServlets, start at the beginning with the\n[helloworld](helloworld) tutorial.  Moving in sequence through the\nservlets will introduce ever-more detail, later examples building on\nearlier concepts, so it is recommended you continue straight on\nthrough without skipping around too much.\n\nOnce you go through the tutorial and start writing your own servlets\nyou will find this tutorial (as its author does!) a handy how-to\nreference to return to over and over again.\n\nEach page in this tutorial is a separate servlet with hyperlinks to\nmove forward and backward through the tutorial.  The top of each page\nhas a global index of all servlets, a link back to this page, and a\nlink to the [Reference Manual](/ref).  In the upper left of every page\nis a link to view the source code for the page you are viewing.\n\nNow, on to the tutorial...\n\n## Table of Contents\n\n')