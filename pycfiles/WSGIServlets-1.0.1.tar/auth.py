# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/auth.py
# Compiled at: 2011-11-02 16:41:15
from TutorialBase import *

class auth(HTMLPage):
    """Basic HTTP authentication, Part I."""
    title = 'Basic HTTP Authentication (1 of 2)'

    def write_content(self):
        self.writeln(OVERVIEW)


OVERVIEW = make_overview('\nWSGIServlets offers methods to assist in managing Basic HTTP\nAuthentication.  The next servlet will demonstrate this functionality.\nThis servlet exists in the tutorial to give you the username and\npassword you will need for the next servlet:\n\n> **username:** wsgi  \n> **password:** servlets\n\n\n* * *\n\n**Note:** if this tutorial is being served by apache mod_wsgi, the\nnext servlet will not work unless the following mod_wsgi directive is\nset for the containing directory:\n\n        WSGIPassAuthorization On\n\nSee mod_wsgi documentation for details.        \n')