# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/channel/jsapi.py
# Compiled at: 2010-12-12 04:36:57
"""Implementation of a request handler providing the Channel JS API."""
import google.appengine.ext.webapp, google.appengine.ext.webapp.util, logging, os

class ChannelJSAPIHandler(google.appengine.ext.webapp.RequestHandler):

    def get(self):
        js_file = open(os.path.join(os.path.dirname(__file__), 'tae-channel-js.js'), 'rb')
        js_data = js_file.read()
        js_file.close()
        self.response.headers['Content-Type'] = 'application/javascript'
        self.response.out.write(js_data)


app = google.appengine.ext.webapp.WSGIApplication([
 (
  '/_ah/channel/jsapi', ChannelJSAPIHandler)], debug=True)

def main():
    google.appengine.ext.webapp.util.run_wsgi_app(app)


if __name__ == '__main__':
    main()