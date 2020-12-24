# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/handlers/devnull.py
# Compiled at: 2010-12-12 04:36:57
"""Dev null handler."""
import google.appengine.ext.webapp, google.appengine.ext.webapp.util

class DevNullHandler(google.appengine.ext.webapp.RequestHandler):
    """ """

    def get(self):
        pass

    def post(self):
        pass


app = google.appengine.ext.webapp.WSGIApplication([
 (
  '/_ah/dev/null', DevNullHandler)], debug=True)

def main():
    google.appengine.ext.webapp.util.run_wsgi_app(app)


if __name__ == '__main__':
    main()