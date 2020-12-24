# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/ref.py
# Compiled at: 2011-11-08 14:30:23
from wsgiservlets import *
import os.path
RELPATH_TO_MAN = '../doc/build/html'

class ref(WSGIServlet):
    use_form = False
    use_session = False

    def _lifecycle(self):
        pi = self.path_info
        if pi:
            pi = pi[1:]
        if not pi:
            self.redirect('/ref/index.html')
        path = os.path.join(RELPATH_TO_MAN, pi)
        if not os.path.exists(path):
            raise HTTPNotFound('Could not find: ' + path)
        self.send_file(path)