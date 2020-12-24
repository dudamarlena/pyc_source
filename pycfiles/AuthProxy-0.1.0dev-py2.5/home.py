# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/controllers/home.py
# Compiled at: 2005-08-12 03:13:28
import logging
from authproxy.lib.base import *
log = logging.getLogger(__name__)

class HomeController(BaseController):

    def index(self):
        return render('genshi', 'index')