# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/headincludes/headincluder.py
# Compiled at: 2010-03-12 11:12:03
""" wsgi middleware for inserting script and style tags into the <head>
of an html file.  It looks at environ['wsgi.html.head.includes'], which
is a list of the urls to be referenced.  If the url ends in '.js', a script
tag is inserted.  If it ends in ".css", a style tag is inserted.

this filter takes care of creating the 'wsgi.html.head.includes' key; the
application just needs to insert relative or absolute urls for the files that
need to be referenced.  This filter will remove duplicates if the app does
not want to check before adding urls to the list.

urls can be placed in the list at any time that request.environ can be
accessed.  Just append any desired url to the list, e.g.,

  try:
      request.environ['wsgi.html.head.includes'].append('/scripts/my_url.js')
  except KeyError:
      (handle case when the filter is not available)
parameters:
location - where in the head element to place the includes.  'top' is the
           default.  Anything else will place it at the bottom.
"""
from queues import StringQueue

class HeadIncludeIter(object):

    def __init__(self, result, environ, tag, write=65536, read=65536):
        self.readBufferSize = read
        self.writeBufferSize = write
        self.environ = environ
        self.tag = tag
        self.queue = StringQueue()
        self.madeUpdate = False
        if isinstance(result, basestring):
            result = (
             result,)
        self.data = iter(result)
        self.allReceived = False
        self.getData()

    def __iter__(self):
        return self

    def getData(self):
        while len(self.queue) < self.readBufferSize and not self.allReceived:
            self.getIter()

    def getIter(self):
        try:
            s = self.data.next()
            if self.tag in s or self.tag.upper() in s:
                s = self.makeInsertion(s)
            self.queue.write(s)
        except StopIteration:
            self.allReceived = True
            if hasattr(self.data, 'close'):
                self.data.close()
            self.data = None

        return

    def makeInsertion(self, data):
        includes = self.environ.get('wsgi.html.head.includes', '')
        if self.tag.upper() in data:
            self.tag = self.tag.upper()
        if includes:
            s = [
             '<!--start headincludes-->']
            for incfile in includes:
                if isinstance(incfile, unicode):
                    incfile = incfile.encode('ascii')
                if incfile.endswith('.js'):
                    s.append('<script type="text/javascript" src="%s"></script>' % incfile)
                elif incfile.endswith('.css'):
                    s.append('<link rel="stylesheet" type="text/css" href="%s" />' % incfile)

            s.append('<!--end headincludes-->')
            if '/' not in self.tag:
                s.insert(0, self.tag)
            else:
                s.append(self.tag)
            updated = data.replace(self.tag, ('\n').join(s))
        else:
            updated = data
        return updated

    def next(self):
        queueLen = len(self.queue)
        if queueLen == 0 and self.allReceived:
            self.queue.close()
            raise StopIteration
        dataGetSize = min(queueLen, self.writeBufferSize)
        s = self.queue.read(dataGetSize)
        if s == '' and self.allReceived:
            s = self.queue.read(None)
        if not self.allReceived:
            self.getData()
        return s


class middleware(object):

    def __init__(self, application, location='top'):
        self.application = application
        self.location = location
        if location == 'top':
            self.tag = '<head>'
        else:
            self.tag = '</head>'

    def __call__(self, environ, start_response):
        environ['wsgi.html.head.includes'] = []
        response = HeadChangeResponse(start_response, self.location)
        app_iter = self.application(environ, response.initial_decisions)
        if response.doProcessing and len(environ['wsgi.html.head.includes']) > 0:
            app_iter = response.finish_response(app_iter, environ, self.tag)
        return app_iter


class HeadChangeResponse(object):

    def __init__(self, start_response, location):
        self.start_response = start_response
        self.location = location
        self.doProcessing = False

    def initial_decisions(self, status, headers, exc_info=None):
        for (name, value) in headers:
            if name.lower() == 'content-type' and (value.startswith('text/html') or value.startswith('application/xhtml+xml')):
                self.doProcessing = True
                break

        if self.doProcessing:
            headers = [ (name, value) for (name, value) in headers if name.lower() != 'content-length' ]
        return self.start_response(status, headers, exc_info)

    def finish_response(self, app_iter, environ, tag):
        if app_iter:
            try:
                output = HeadIncludeIter(app_iter, environ, tag)
            finally:
                try:
                    app_iter.close()
                except AttributeError:
                    pass

                if len(app_iter) == 1:
                    s = ('').join([ x for x in output ])
                    return (s,)
                return output

        else:
            return app_iter


def filter_factory(global_conf, location='top'):

    def filter(application):
        return middleware(application, location)

    return filter