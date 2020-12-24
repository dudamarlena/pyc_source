# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/digenpyweb/__init__.py
# Compiled at: 2013-04-16 14:07:45
from flask import Flask, render_template, abort, Response, request
import Digenpy_, json
from Digenpy_ import *
app = Flask(__name__)
app.config['DEBUG'] = False

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/get/<country>/<company>/<mac>/<essid>')
def do_digenpy(country, company, mac, essid):
    method = request.environ['REQUEST_METHOD']
    result = getattr(getattr(Digenpy_, country), company)(['', mac, essid]).dictionary
    if not result:
        abort(404)
    if method == 'POST':
        return json.dumps(result)
    if method == 'GET':
        return ('\n').join(result)


@app.route('/get_file/<country>/<company>/<mac>/<essid>')
def download_file(country, company, mac, essid):
    return Response(do_digenpy(country, company, mac, essid), mimetype='application/x-digenpy-dic')


def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022)


if __name__ == '__main__':
    server()