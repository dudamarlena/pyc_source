# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.6/site-packages/bottle_api_json_formatting/test_app.py
# Compiled at: 2013-11-30 16:16:57
__doc__ = ' Specialized app for testing bottle_api_json_formatting '
from bottle import Bottle
from bottle import run
from bottle import abort
from bottle import request
from bottle_api_json_formatting import JsonFormatting
APP = Bottle()
APP.install(JsonFormatting())

@APP.route('/')
def index():
    """ Basic result """
    return 'test'


@APP.route('/error')
def error():
    """ Cause a common HTTP error """
    abort(401, 'Access denied')


@APP.route('/failure')
def failure():
    """ Cause an app failure """
    raise Exception('test failure')


@APP.route('/uninstall')
def uninstall():
    """ Uninstall the module and return a basic result """
    APP.uninstall('json_formatting')
    return 'uninstalled'


@APP.route('/switchmediatypes', method='POST')
def typetest():
    """ Test supported types """
    mediatypes = request.forms.get('mediatypes')
    APP.uninstall('json_formatting')
    if mediatypes:
        supported_types = mediatypes.split(',')
        APP.install(JsonFormatting(supported_types=supported_types))
    else:
        APP.install(JsonFormatting())


if __name__ == '__main__':
    run(APP, host='0.0.0.0', port=8080, debug=True)