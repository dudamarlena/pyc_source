# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ablog_api/doc.py
# Compiled at: 2016-08-24 12:22:33
__doc__ = '\n    Module ablog_api.login\n'
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