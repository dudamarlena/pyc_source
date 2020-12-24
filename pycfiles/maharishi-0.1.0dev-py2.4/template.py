# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/maharishi/controllers/template.py
# Compiled at: 2006-08-30 12:30:23
from maharishi.lib.base import *

class TemplateController(BaseController):
    __module__ = __name__

    def view(self, url):
        """
        This is the last place which is tried during a request to try to find a 
        file to serve. It could be used for example to display a template::
        
            def view(self, url):
                return render_response(url+'.myt')
        
        The default is just to abort the request with a 404 File not found
        status message.
        """
        abort(404)