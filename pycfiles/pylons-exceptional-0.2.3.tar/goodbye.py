# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ben/Programming/Python/pylons/test_files/sample_controllers/controllers/goodbye.py
# Compiled at: 2015-01-02 21:10:30
import logging
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect
from webob import Response
from webob.exc import HTTPNotFound
log = logging.getLogger(__name__)

class Smithy(WSGIController):

    def __init__(self):
        self._pylons_log_debug = True

    def index(self):
        return 'Hello World'


__controller__ = 'Smithy'