# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/gohttp/__main__.py
# Compiled at: 2016-05-23 22:50:39
from . import route, run
if __name__ == '__main__':

    @route('/')
    def index(w, req):
        w.write('%s %s %s\n' % (req.method, req.host, req.url))
        w.write('Hello, world.\n')


    run()