# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/dlblocks/HTMLReport.py
# Compiled at: 2018-12-11 12:52:10
import base64, cv2

class HTMLReport:
    """docstring for HTMLReport"""

    def __init__(self):
        self.htmlBody = ''

    def addHead(self, txt, h='h1'):
        self.htmlBody += '<%s> %s </%s>  ' % (h, txt, h)

    def addHR(self):
        self.htmlBody += '<hr> '

    def addBR(self):
        self.htmlBody += '<br> '

    def addImg(self, imgPath, resizeTo=None):
        img = cv2.imread(imgPath)
        if resizeTo is not None:
            img = cv2.resize(img, resizeTo)
        cnt = cv2.imencode('.jpg', img)[1]
        b64 = base64.encodestring(cnt)
        self.htmlBody += "<img src='data:image/jpg;base64," + b64 + "'> <br>"
        return

    def addCVImg(self, img, resizeTo=None):
        if resizeTo is not None:
            img = cv2.resize(img, resizeTo)
        cnt = cv2.imencode('.jpg', img)[1]
        b64 = base64.encodestring(cnt)
        self.htmlBody += "<img src='data:image/jpg;base64," + b64 + "'> <br>"
        return

    def addText(self, txt):
        txt = str(txt)
        txt = txt.split('\n')
        txt = '<pre>' + ('</pre> <br>\n<pre>').join(txt) + '</pre> <br>\n'
        self.htmlBody += txt

    def save(self, fname):
        completeHTML = '<html> <body> ' + self.htmlBody + '</html> </body> '
        open(fname, 'wb').write(completeHTML)