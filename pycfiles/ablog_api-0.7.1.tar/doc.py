# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ablog_api/doc.py
# Compiled at: 2016-08-24 12:22:33
"""
    Module ablog_api.login
"""
import os
from flask_autodoc import Autodoc

class Doc:

    def __init__(self, app, base_url='/'):
        if base_url[(-1)] != '/':
            base_url = base_url + '/'
        self.doc = Autodoc(app)
        try:
            from docutils import core
            RESTIFY = True
        except:
            RESTIFY = False

        def rsttohtml(rst):
            if not rst:
                rst = ''
            if RESTIFY:
                return core.publish_parts(rst, writer_name='html')['html_body']
            return '<div class="document">%s</div>' % rst

        @app.route('%sdoc' % base_url)
        def doc():
            return app.doc.html(template='myautodoc.html', rsttohtml=rsttohtml)