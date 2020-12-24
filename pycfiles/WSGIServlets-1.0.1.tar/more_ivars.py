# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/more_ivars.py
# Compiled at: 2011-10-27 22:53:13
import random
from TutorialBase import *

class more_ivars(HTMLPage):
    """Further discussion about special attributes."""

    def title(self):
        E = '!' * random.randint(1, 5)
        return 'More Special Attributes%s' % E

    css_links = [
     '/more_ivars.css']
    js = "\n    function go() {\n       alert('Hello, World!');\n    }\n    "
    shortcut_icon = 'python.ico'

    def write_content(self):
        self.writeln(OVERVIEW)


OVERVIEW = make_overview('\nThere are many other attributes you can set in your servlets to\ncontrol the generated HTML.  Here are a few, see the reference\ndocumentation for a complete list.\n\nAttribute         | Description\n----------------- | --------------------------------------\n**css_links**     | In the previous servlet we inserted CSS by setting the `css` attribute.  This created a STYLE element in the HEAD.  You can also refer to CSS in an external document by setting the `css_links` attribute.  The external CSS document refered to by this servlet sets the background color to lightgrey, sets other table border and alignment attributes, and places a border around H1 tags.\n**js**            | You can insert javascript by setting the `js` attribute. {button}\n**shortcut_icon** | You can specify a shortcut icon by setting this attribute.  For this servlet, I have borrowed the python icon.\n**title**         | You have already seen how the title of the document can be set with the `title` attribute.  It can also be callable to generate dynamic titles! Reload this page and watch the title change.\n\n      \n')
OVERVIEW = OVERVIEW.format(button='<button onclick="go()">Click Me!</button>')