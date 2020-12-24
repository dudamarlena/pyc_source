# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/matanui/inout.py
# Compiled at: 2011-01-01 18:09:46
"""Provides a structure for input/output context with web server."""
__author__ = 'Guy K. Kloss <Guy.Kloss@aut.ac.nz>'

class InOut(object):
    """
    Provides a container object that holds context for input/output with the
    web server.
    """

    def __init__(self, environment=None):
        """
        Constructor.
        
        @param environment: WSGI server environment to initialise the container
            items.
        @type environment: C{dict}
        """
        self.output = None
        self.content_length = 0
        self.response_headers = [
         ('Content-type', 'text/plain')]
        self.input_stream = None
        self.output_stream_factory = None
        if 'wsgi.input' in environment:
            self.input_stream = environment['wsgi.input']
        if 'wsgi.file_wrapper' in environment:
            self.output_stream_factory = environment['wsgi.file_wrapper']
        return

    def set_output_stream(self, data, block_size=None):
        """
        Assigns the output stream L{output} of the object to use for the
        response with the parameter C{data}, using the WSGI C{file_wrapper}.
        The C{file_wrapper} can be specified with an optional C{block_size} for
        the output.
        
        @param data: Data object to use for linking to the output stream.
        @type data: "File like" object.
        @param block_size: Size of blocks to use for transfer.
        @type block_size: C{int}
        """
        if self.output_stream_factory:
            self.output = self.output_stream_factory(data, block_size)
        else:
            self.output = data