# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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