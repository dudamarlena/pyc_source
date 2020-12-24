# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/zif/jsmin/jsmin.py
# Compiled at: 2006-12-16 06:43:22
"""
WSGI middleware

does js and css minimization.
"""
import css, javascript

class middleware(object):
    __module__ = __name__

    def __init__(self, application, compress_level='full', compress_types='css js', exclude=''):
        self.application = application
        self.compress_level = compress_level
        self.compress_types = compress_types.split()
        self.excludes = exclude.split()

    def __call__(self, environ, start_response):
        response = MinResponse(start_response, self.compress_level, self.compress_types)
        app_iter = self.application(environ, response.initial_decisions)
        myGet = environ.get('PATH_INFO')
        for filename in self.excludes:
            if filename in myGet:
                response.doProcessing = False

        if response.doProcessing:
            app_iter = response.finish_response(app_iter)
        return app_iter


class MinResponse(object):
    __module__ = __name__

    def __init__(self, start_response, compress_level, compress_types):
        self.start_response = start_response
        self.compress_level = compress_level
        self.compress_types = compress_types
        self.doProcessing = False
        self.compress_type = None
        return

    def initial_decisions(self, status, headers, exc_info=None):
        ct = None
        ce = None
        for (name, value) in headers:
            name = name.lower()
            if name == 'content-type':
                ct = value
            elif name == 'content-encoding':
                ce = value

        self.doProcessing = False
        if ct and ('javascript' in ct or 'ecmascript' in ct or 'css' in ct):
            self.doProcessing = True
            if 'css' in ct:
                self.compress_type = 'css'
            else:
                self.compress_type = 'js'
        if ce:
            self.doProcessing = False
        if self.compress_type not in self.compress_types:
            self.doProcessing = False
        if self.doProcessing:
            headers = [ (name, value) for (name, value) in headers if name.lower() != 'content-length' ]
        return self.start_response(status, headers, exc_info)

    def finish_response(self, app_iter):
        theString = ('').join([ x for x in app_iter ])
        if self.doProcessing:
            if self.compress_type == 'js':
                compress = javascript.compress
            else:
                compress = css.compress
        output = compress(theString, self.compress_level)
        if hasattr(app_iter, 'close'):
            app_iter.close()
        return (
         output,)


def filter_factory(global_conf, compress_level='safe', compress_types='js css', exclude=''):

    def filter(application):
        return middleware(application, compress_level, compress_types, exclude)

    return filter