# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/controllers/error.py
# Compiled at: 2016-09-19 13:27:02
"""Contains the :class:`ErrorController`.

.. module:: error
   :synopsis: Contains the error controller.

"""
import cgi
from paste.urlparser import PkgResourcesParser
from pylons import request, response
from pylons.controllers.util import forward
from pylons.middleware import error_document_template
from webhelpers.html.builder import literal
import simplejson as json
from onlinelinguisticdatabase.lib.base import BaseController

class ErrorController(BaseController):
    """Generate JSON error objects as required.

    The ``StatusCodeRedirect`` middleware forwards to ``ErrorController`` when
    error-related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ``StatusCodeRedirect`` middleware in the ``config/middleware.py`` file.

    """

    def document(self):
        """Return a JSON object representing the error.

        Instead of returning an HTML error document (the Pylons default),
        return the JSON object that the controller has specified for the
        response body.  If the response body is not valid JSON, then it has been
        created by Routes; make it into valid JSON.

        """
        resp = request.environ.get('pylons.original_response')
        if resp.status_int == 404:
            try:
                JSONResp = json.loads(resp.body)
            except json.decoder.JSONDecodeError:
                resp.body = json.dumps({'error': 'The resource could not be found.'})

        elif resp.status_int == 500:
            try:
                JSONResp = json.loads(resp.body)
            except json.decoder.JSONDecodeError:
                resp.body = json.dumps({'error': 'Internal Server Error'})

        return resp.body