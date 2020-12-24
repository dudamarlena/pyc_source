# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/ivars.py
# Compiled at: 2011-10-27 23:05:34
from TutorialBase import *

class ivars(HTMLPage):
    """Introduction to special attributes that can control HTML generation."""
    title = 'Setting Special Instance Data Attributes'
    css = '\n    DIV.ivars {\n        margin: 50px 25%;\n        padding: 10px;\n        background: #F0EBE2;\n    }\n\n    H1 {\n        color:blue\n    }\n    '

    def write_content(self):
        self.writeln('<DIV class="ivars">', OVERVIEW, '</DIV>')


OVERVIEW = make_overview("\nBy setting various attributes in your servlet you can control the\nHTML.  In this servlet we have set the `css` attribute to specify the\nbackground color of this text's containing DIV element to be lightgrey\nwith margins set to center the text in the middle of the window and\nthe color of text in H1 elements (the title) to be blue.\n\nView the python source.  The `css` attribute can be set to any object\nthat can be converted into a string or it can be a sequence (list,\ntuple) of strings, in which case, the strings will be joined.\n")