# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Programming/Python/pylons/test_files/sample_controllers/controllers/hello.py
# Compiled at: 2015-01-02 21:10:30
import logging
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect
from pylons.templating import render_mako
from webob import Response
from webob.exc import HTTPNotFound
log = logging.getLogger(__name__)

class HelloController(WSGIController):

    def __init__(self):
        self._pylons_log_debug = True

    def index(self):
        return 'Hello World'

    def oops(self):
        raise Exception('oops')

    def abort(self):
        abort(404)

    def intro_template(self):
        return render_mako('/hello.html')

    def time_template(self):
        return render_mako('/time.html', cache_key='fred', cache_expire=20)


def special_controller(environ, start_response):
    return HTTPNotFound()


def empty_wsgi(environ, start_response):
    pass


def a_view(request):
    return Response('A View')