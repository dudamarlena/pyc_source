# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/matanui/service.py
# Compiled at: 2011-01-19 20:35:52
"""Main service implementation."""
__author__ = 'Guy K. Kloss <Guy.Kloss@aut.ac.nz>'
__date__ = '$Date: $'
import sys, io
from httplib import responses
from matanui import request
from matanui import inout
from matanui import operations
from matanui.exceptions import MataNuiServiceException

class MataNuiService(object):
    """
    Service object that handles the implementation of the RESTful operations.
    """

    def __init__(self, environ):
        """
        Constructor.
        
        @param environ: Web server environment.
        @type environ: C{dict}
        """
        self.environment = environ
        self.status = (200, '')
        self.request = None
        self.inout = None
        self.error_logger = None
        if 'wsgi.errors' in self.environment:
            self.error_logger = self.environment['wsgi.errors']
        else:
            self.error_logger = sys.stderr
        return

    def invoke(self):
        """
        Invokes the service implementation. This is the method called by the
        WSGI server stub script.
        """
        self.inout = inout.InOut(self.environment)
        try:
            self.request = request.Request(self.environment)
            my_storer = operations.StorageOperations(self.request, self.inout)
            storage_operation = self.dispatch(my_storer)
            self.status = storage_operation()
        except MataNuiServiceException, err:
            self.status = err.status
            output_string = 'Service error %s %s, reason: %s/%s' % (
             err.status[0], responses[err.status[0]],
             err.status[1], err.message)
            self.inout.output = io.BytesIO(str(output_string))
            self.inout.content_length = len(self.inout.output.getvalue())
            self.error_logger.write(output_string)

        self.inout.response_headers.append(('Content-Length',
         str(self.inout.content_length)))
        if self.status[1]:
            status = '%s %s: %s' % (self.status[0],
             responses[self.status[0]],
             self.status[1])
        else:
            status = '%s %s' % (self.status[0], responses[self.status[0]])
        return (self.inout.response_headers, status, self.inout.output)

    def dispatch(self, storer):
        """
        Dispatches the service call to the designated handler methods.
        
        @param storer: The storer providing the required storage operations.
        @type storer: L{matanui.operations.StorageOperations}
        """
        if self.request.content_request == request.INFO:
            return storer.get_info
        actions = {('GET', request.CONTENT): storer.get_content, ('GET', request.METADATA): storer.get_metadata, 
           ('GET', request.LIST): storer.list_resources, 
           ('PUT', request.METADATA): storer.put_metadata, 
           ('POST', request.CONTENT): storer.post_content, 
           ('DELETE', request.CONTENT): storer.delete_file}
        http_method = self.environment['REQUEST_METHOD'].upper()
        try:
            action = actions[(http_method, self.request.content_request)]
        except KeyError:
            message = '%s request for Accept header %s not defined.' % (
             http_method, self.environment.get('HTTP_ACCEPT', '*/*'))
            status = (501, '')
            raise MataNuiServiceException(message, status)

        return action