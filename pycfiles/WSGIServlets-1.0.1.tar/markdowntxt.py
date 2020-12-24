# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/markdowntxt.py
# Compiled at: 2011-10-12 15:04:35
from TutorialBase import *

class markdowntxt(HTMLPage):
    """A note about using markdown in the tutorial."""
    title = 'Using Markdown'

    def write_content(self):
        self.writeln(OVERVIEW)


OVERVIEW = make_overview("\n{divstart}\n\nA note about the generated HTML for this tutorial.  The text you are\nreading throughout this tutorial is written in\n[Markdown](http://daringfireball.net/projects/markdown/).  From\nMarkdown's website:\n\n> *Markdown is a text-to-HTML conversion tool for web\n> writers. Markdown allows you to write using an easy-to-read,\n> easy-to-write plain text format, then convert it to structurally\n> valid XHTML (or HTML).*\n\nThis tutorial is written assuming the Markdown [python\npackage](http://pypi.python.org/pypi/Markdown) is installed on\nthe host machine running this tutorial and is available to import.  If\nthe package is not found[^1], you will see readable, albeit plain, text.\n(And that folks is the beauty of markdown.)\n\n[^1]:\n    And apparently it **{markdownfound}** found on this server!\n    \n{divend}\n\nAnd one final comment about the text you see: when viewing the source\ncode (via the links on each tutorial page), to make the source code as\nreadable as possible, I have moved the markdown text processing to the\nbottom of the files, so when you see this:\n\n        # -*-*- DOC -*-*-\n\nyou should know that what follows is uninteresting text processing.\n")
DIVSTART = '<div style="background-color:gold;margin:50px;padding:5px;border-style:solid">'
DIVEND = '</div>'
OVERVIEW = OVERVIEW.format(divstart=DIVSTART, divend=DIVEND, markdownfound='is' if USEMARKDOWN else 'is not')