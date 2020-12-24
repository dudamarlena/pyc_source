# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tracdeveloper/javascript.py
# Compiled at: 2011-09-06 06:16:46
from trac.core import *
from trac.web.api import IRequestFilter

class JavascriptDeveloperModule(Component):
    """Developer functionality for JavaScript in Trac."""
    implements(IRequestFilter)

    def pre_process_request(self, req, handler):
        if req.session.get('developer.js.enable_debug') == '1' and req.path_info == '/chrome/common/js/jquery.js':
            req.args['prefix'] = 'developer'
            req.args['filename'] = 'js/jquery-1.2.6.js'
        return handler

    def post_process_request(self, req, template, content_type):
        return (
         template, content_type)