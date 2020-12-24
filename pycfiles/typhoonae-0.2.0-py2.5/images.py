# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/handlers/images.py
# Compiled at: 2010-12-12 04:36:57
"""Images handler."""
import google.appengine.ext.webapp, google.appengine.ext.webapp.util, logging, os

class ImagesHandler(google.appengine.ext.webapp.RequestHandler):
    """Images handler takes care of image resizing and cropping on blobs."""

    def get(self):
        image_file = open(os.path.join(os.path.dirname(__file__), 'dummy.png'), 'rb')
        image_data = image_file.read()
        image_file.close()
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(image_data)


app = google.appengine.ext.webapp.WSGIApplication([
 (
  '/_ah/img(?:/.*)?', ImagesHandler)], debug=True)

def main():
    google.appengine.ext.webapp.util.run_wsgi_app(app)


if __name__ == '__main__':
    main()