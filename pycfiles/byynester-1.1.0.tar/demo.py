# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/byu_ws_sdk/demo.py
# Compiled at: 2013-08-09 21:39:38
from . import core

def setup_demo():
    import httplib
    from httplib import NotConnected
    import array, copy, requests

    def httpConnectionSend(self, data):
        """Send `data' to the server."""
        if self.sock is None:
            if self.auto_open:
                self.connect()
            else:
                raise NotConnected()
        print_data = copy.deepcopy(data)
        print_data = print_data[:-2]
        print '> ' + print_data.replace('\r\n', '\r\n> ')
        print ()
        blocksize = 8192
        if hasattr(data, 'read') and not isinstance(data, array):
            if self.debuglevel > 0:
                print 'sendIng a read()able'
            data_block = data.read(blocksize)
            while data_block:
                self.sock.sendall(data_block)
                data_block = data.read(blocksize)

        else:
            self.sock.sendall(data)
        return

    httplib.HTTPConnection.send = httpConnectionSend

    def requestSendWrapper(sendFunc):
        """
        Wrapper method to call the send method
        and then print the response.
        """

        def wrapper(self, *args, **kwargs):
            sendFunc(self, *args, **kwargs)
            response = self.response
            msg = []
            if response.raw.version == 11:
                version_line = 'HTTP/1.1'
            else:
                version_line = 'HTTP/1.0'
            version_line += ' ' + str(response.raw.status)
            version_line += ' ' + response.raw.reason
            msg.append(version_line)
            for header in response.headers.keys():
                msg.append(header.title() + ': ' + response.headers[header])

            if 'content-length' not in response.headers.keys():
                msg.append('Content-Length: ' + str(len(response.content)))
            msg.append('')
            msg.append(core.get_formatted_response(response.headers, response.content))
            print '< ' + ('\r\n< ').join(msg)
            print ()

        return wrapper

    if requests.models.Request.send.__name__ != 'wrapper':
        requests.models.Request.send = requestSendWrapper(requests.models.Request.send)