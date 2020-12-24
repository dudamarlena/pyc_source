# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/controllers/hello.py
# Compiled at: 2008-09-22 07:43:53
import logging
from frla.lib.base import *
log = logging.getLogger(__name__)

class HelloController(BaseController):
    __module__ = __name__

    def index(self):
        return 'Hello World'