# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/controllers/home.py
# Compiled at: 2007-10-23 19:11:32
from gazest.lib.base import *

class HomeController(BaseController):
    __module__ = __name__

    def home(self):
        return render('/home.mako')

    def about(self):
        return render('/about.mako')

    def contact(self):
        c.title = 'Contact'
        return render('/contact.mako')