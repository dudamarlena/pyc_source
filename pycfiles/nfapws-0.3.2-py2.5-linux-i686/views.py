# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fapws/contrib/views.py
# Compiled at: 2009-08-20 03:05:56
import mimetypes, os.path, time

class Staticfile:
    """ Generic class that you can use to dispatch static files
    You must use it like this:
      static=Staticfile("/rootpath/")
      evhttp.http_cb("/static/",static)
    NOTE: you must be consistent between /rootpath/ and /static/ concerning the ending "/"
    """

    def __init__(self, rootpath='', maxage=None):
        self.rootpath = rootpath
        self.maxage = maxage

    def __call__(self, environ, start_response):
        fpath = self.rootpath + environ['PATH_INFO']
        try:
            f = open(fpath, 'rb')
        except:
            print 'ERROR in Staticfile: file %s not existing' % fpath
            start_response('404 File not found', [])
            return []

        fmtime = os.path.getmtime(fpath)
        if environ.get('HTTP_IF_MODIFIED_SINCE', 'NONE') != str(fmtime):
            headers = []
            if self.maxage:
                headers.append(('Cache-control', 'max-age=%s' % int(self.maxage + time.time())))
            ftype = mimetypes.guess_type(fpath)[0]
            headers.append(('Content-Type', ftype))
            headers.append(('Last-Modified', fmtime))
            headers.append(('Content-Length', os.path.getsize(fpath)))
            start_response('200 OK', headers)
            return f
        else:
            start_response('304 Not Modified', [])
            return []