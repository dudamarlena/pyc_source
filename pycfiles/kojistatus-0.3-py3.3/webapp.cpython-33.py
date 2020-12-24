# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kojistatus/webapp.py
# Compiled at: 2017-01-27 08:21:42
# Size of source mod 2**32: 1051 bytes
from flask import Flask, Response, request
from flask.helpers import NotFound
from requests.exceptions import HTTPError
from .status import status
app = Flask(__name__)

def session(app):
    if 'SESSION' in app.config:
        return app.config['SESSION']


app.__class__.session = session

@app.route('/')
@app.route('/<username>/')
def main(username=None):
    koji = request.args.get('koji')
    if koji == 'centos':
        kojiurl = 'https://cbs.centos.org/'
    else:
        if koji == 'rpmfuison':
            kojiurl = 'http://koji.rpmfusion.org/'
        else:
            kojiurl = None
    try:
        lines = ('{} {}'.format(*s) for s in status(username, session=app.session(), kojiurl=kojiurl))
    except HTTPError:
        raise NotFound()

    return Response('\n'.join(lines), mimetype='text/plain')