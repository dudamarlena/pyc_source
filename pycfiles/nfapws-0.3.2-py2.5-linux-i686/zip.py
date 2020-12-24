# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fapws/contrib/zip.py
# Compiled at: 2009-08-20 03:05:56
try:
    import cStringIO as StringIO
except:
    import StringIO

import gzip

class Gzip:

    def __call__(self, f):

        def func(environ, start_response):
            content = f(environ, start_response)
            if 'gzip' in environ.get('HTTP_ACCEPT_ENCODING', ''):
                if type(content) == type([]):
                    content = ('').join(content)
                else:
                    content = content.read()
                sio = StringIO.StringIO()
                comp_file = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=sio)
                comp_file.write(content)
                comp_file.close()
                start_response.add_header('Content-Encoding', 'gzip')
                res = sio.getvalue()
                start_response.add_header('Content-Length', len(res))
                return [res]
            else:
                return content

        return func