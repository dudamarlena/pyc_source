# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/controllers/index.py
# Compiled at: 2008-07-29 02:14:33
import logging
from divimon.lib.base import *
log = logging.getLogger(__name__)

class IndexController(BaseController):

    def index(self):
        return render('/blank.mako')