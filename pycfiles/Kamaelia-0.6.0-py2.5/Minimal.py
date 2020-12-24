# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/HTTP/Handlers/Minimal.py
# Compiled at: 2008-10-19 12:19:52
"""========================
Minimal
========================
A simple HTTP request handler for HTTPServer.
Minimal serves files within a given directory, guessing their
MIME-type from their file extension.

Example Usage
-------------
See HTTPResourceGlue.py for how to use request handlers.
"""
import string, time, dircache, os
from Axon.Ipc import producerFinished, shutdown
from Axon.Component import component
from Kamaelia.File.BetterReading import IntelligentFileReader
import Kamaelia.Protocol.HTTP.MimeTypes as MimeTypes, Kamaelia.Protocol.HTTP.ErrorPages as ErrorPages

def sanitizeFilename(filename):
    output = ''
    for char in filename:
        if char >= '0' and char <= '9':
            output += char
        elif char >= 'a' and char <= 'z':
            output += char
        elif char >= 'A' and char <= 'Z':
            output += char
        elif char == '-' or char == '_' or char == '.':
            output += char

    return output


def sanitizePath(uri):
    outputpath = []
    while uri[0] == '/':
        uri = uri[1:]
        if len(uri) == 0:
            break

    splitpath = string.split(uri, '/')
    for directory in splitpath:
        if directory == '.':
            pass
        elif directory == '..':
            if len(outputpath) > 0:
                outputpath.pop()
        else:
            outputpath.append(directory)

    outputpath = string.join(outputpath, '/')
    return outputpath


class Minimal(component):
    """    A simple HTTP request handler for HTTPServer which serves files within a
    given directory, guessing their MIME-type from their file extension.

    Arguments:
    -- request - the request dictionary object that spawned this component
    -- homedirectory - the path to prepend to paths requested
    -- indexfilename - if a directory is requested, this file is checked for inside it, and sent if found
    """
    Inboxes = {'inbox': 'UNUSED', 
       'control': 'UNUSED', 
       '_fileread': 'File data', 
       '_filecontrol': 'Signals from file reader'}
    Outboxes = {'outbox': 'Response dictionaries', 
       'signal': 'UNUSED', 
       '_fileprompt': 'Get the file reader to do some reading', 
       '_filesignal': 'Shutdown the file reader'}

    def __init__(self, request, indexfilename='index.html', homedirectory='htdocs/'):
        self.request = request
        self.indexfilename = indexfilename
        self.homedirectory = homedirectory
        super(Minimal, self).__init__()

    def main(self):
        """Produce the appropriate response then terminate."""
        filename = sanitizePath(self.request['raw-uri'])
        filetype = MimeTypes.workoutMimeType(filename)
        error = None
        try:
            if os.path.exists(self.homedirectory + filename) and not os.path.isdir(self.homedirectory + filename):
                resource = {'content-type': filetype, 'statuscode': '200'}
                self.send(resource, 'outbox')
            else:
                print 'Error 404, ' + filename + ' is not a file'
                print 'self.homedirectory(%s) , filename(%s)' % (self.homedirectory, filename)
                print 'os.path.exists(self.homedirectory + filename)', os.path.exists(self.homedirectory + filename)
                print 'not os.path.isdir(self.homedirectory + filename)', not os.path.isdir(self.homedirectory + filename)
                error = 404
        except OSError, e:
            error = 404

        if error == 404:
            resource = ErrorPages.getErrorPage(404)
            resource['incomplete'] = False
            self.send(resource, 'outbox')
            self.send(producerFinished(self), 'signal')
            return
        self.filereader = IntelligentFileReader(self.homedirectory + filename, 50000, 10)
        self.link((self, '_fileprompt'), (self.filereader, 'inbox'))
        self.link((self, '_filesignal'), (self.filereader, 'control'))
        self.link((self.filereader, 'outbox'), (self, '_fileread'))
        self.link((self.filereader, 'signal'), (self, '_filecontrol'))
        self.addChildren(self.filereader)
        self.filereader.activate()
        yield 1
        done = False
        while not done:
            yield 1
            while self.dataReady('_fileread') and len(self.outboxes['outbox']) < 3:
                msg = self.recv('_fileread')
                resource = {'data': msg}
                self.send(resource, 'outbox')

            if len(self.outboxes['outbox']) < 3:
                self.send('GARBAGE', '_fileprompt')
            while self.dataReady('_filecontrol') and not self.dataReady('_fileread'):
                msg = self.recv('_filecontrol')
                if isinstance(msg, producerFinished):
                    done = True

            self.pause()

        self.send(producerFinished(self), 'signal')
        return


__kamaelia_components__ = (Minimal,)