# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/overriding2.py
# Compiled at: 2011-11-02 16:42:39
from SitePage import *

class overriding2(SitePage):
    """Continuing discussions of overriding HTMLPage methods"""
    simulate_modification = True
    title = 'Overriding HTMLPage Methods (Revisited)'

    def write_content(self):
        self.writeln(OVERVIEW)

    def write_sidebar(self):
        SitePage.write_sidebar(self)
        self.writeln(MORESIDEBAR)


OVERVIEW = make_overview('\n\n###### &uarr;&uarr;&uarr; Look!  A banner! &uarr;&uarr;&uarr;\n\nSo, after some time with a sidebar & content page layout you decide you\nreally need to have a banner as well:\n    \n\n    ---------------------------------------------------\n    |                                                 |\n    |                   BANNER                        |\n    |                                                 |\n    ---------------------------------------------------\n    |            |                                    |\n    | SIDEBAR    |  CONTENT                           |\n    |            |                                    |\n    |            |                                    |\n    |            |                                    |\n    |            |                                    |\n    ---------------------------------------------------\n\nAll you need to do is tweak the code in `SitePage.write_body_parts` to\nadd a DIV and call a method, say, `write_banner`, inside the DIV:\n\n\n    def write_body_parts(self):\n\n        self.writeln(\'<div id="banner">\')  ###\n        self.write_banner()                ###\n        self.writeln(\'</div>\')             ###\n        self.writeln(\'<div id="sidebar">\')\n        self.write_sidebar()\n        self.writeln(\'</div>\')\n        self.writeln(\'<div id="content">\')\n        self.write_content()\n        self.writeln(\'</div>\')\n\n\n[Note: The three lines marked with trailing **###** are the only\nchanges from the sample code in the previous servlet.]\n\n\nThis is what we have done with this servlet.  Well, you didn\'t\nactually edit `SitePage.py`, we have simulated modifying\n`SitePage.write_body_parts` by turning on a flag,\n`simulate_modification`; look at the code in [SitePage.py](SitePage.py) for\ndetails.  (Note: This also demonstrates how page layout can be\ncomputed dynamically on the fly!)  Now, every servlet subclassing\n`SitePage` will get the change.\n\n##### &larr; Notice, too, how the sidebar has been extended!\n')
MORESIDEBAR = markdown('\n____\n\n\nWe have extended the sidebar by calling the superclass method and then\nadding a horizontal rule and this text.  View the python source for\ndetails.  ')