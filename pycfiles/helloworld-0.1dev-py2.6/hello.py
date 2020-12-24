# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\helloworld\controllers\hello.py
# Compiled at: 2010-12-05 16:58:13
import logging
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from helloworld.lib.base import BaseController, render
log = logging.getLogger(__name__)

class HelloController(BaseController):

    def index(self):
        return 'Hello World'