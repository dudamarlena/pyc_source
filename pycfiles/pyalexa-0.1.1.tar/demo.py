# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyaler/demo.py
# Compiled at: 2010-07-24 11:44:38
import os
from pyaler import app
from bottle import request, send_file

@app.route('/')
def index():
    image = request.environ['pyaler.app_config']['image']
    return '<html><head>\n    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>\n    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.js"></script>\n    <script type="text/javascript" src="/static/demo.js"></script>\n    </head><body><img src="/static/%(image)s" /><div id="control"></div></body></html>' % locals()


@app.route('/static/:filename')
def static_file(filename):
    if filename.endswith('.js'):
        send_file(os.path.basename(filename), root=os.path.dirname(__file__))
    else:
        image = request.environ['pyaler.app_config']['image']
        send_file(os.path.basename(image), root=os.path.dirname(image))