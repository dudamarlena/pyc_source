# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/maharishi/controllers/hello.py
# Compiled at: 2006-08-30 12:47:58
from maharishi.lib.base import *

class HelloController(BaseController):
    __module__ = __name__

    def index(self):
        return Response('hello world')

    def serverinfo(self):
        session['name'] = 'George'
        session.save()
        return render_response('/serverinfo.myt')