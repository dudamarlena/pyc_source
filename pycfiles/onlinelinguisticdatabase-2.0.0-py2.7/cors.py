# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/controllers/cors.py
# Compiled at: 2016-09-19 13:27:02
"""Contains the :class:`CorsController` and its auxiliary functions.

.. module:: cors
   :synopsis: Contains the controller for responding to CORS preflight OPTIONS
   requests

"""
import logging
from pylons import request, response, session, app_globals, config
from onlinelinguisticdatabase.lib.base import BaseController
import onlinelinguisticdatabase.lib.helpers as h
log = logging.getLogger(__name__)

class CorsController(BaseController):
    """Generate responses to requests on form resources.

    REST Controller styled on the Atom Publishing Protocol.

    """

    @h.restrict('OPTIONS')
    def proceed(self):
        response.status_int = 204