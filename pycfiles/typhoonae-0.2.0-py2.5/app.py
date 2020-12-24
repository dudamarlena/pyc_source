# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/tests/sample/app.py
# Compiled at: 2010-12-12 04:36:57
import wsgiref.handlers
from google.appengine.ext import webapp

class MyRequestHandler(webapp.RequestHandler):

    def get(self):
        self.response.out.write('<html><body>Hello, World!</body></html>')


application = webapp.WSGIApplication([
 (
  '/', MyRequestHandler)], debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    main()