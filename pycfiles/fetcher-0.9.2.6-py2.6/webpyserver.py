# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\webpyserver.py
# Compiled at: 2010-12-30 09:18:26
__created__ = '2009/09/27'
__author__ = 'xlty.0512@gmail.com'
__author__ = '牧唐 杭州'
import web
urls = ('/upload', 'Upload')

class Upload:

    def GET(self):
        return '<html><head></head><body>\n<form method="POST" enctype="multipart/form-data" action="">\n<input type="file" name="myfile" />\n<br/>\n<input type="submit" />\n</form>\n</body></html>'

    def POST(self):
        print '>>>>>>>>>>>>>>', web.input()
        x = web.input(myfile={})
        web.debug(x['myfile'].filename)
        web.debug(x['myfile'].value)
        web.debug(x['myfile'].file.read())
        print '<<<<<<<<<<<<<<<', web.input().x, web.input().ty, '>>>>>>>>>>>>>>>'
        raise web.seeother('/upload')


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()