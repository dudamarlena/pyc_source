# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\packages\base\feeds.py
# Compiled at: 2013-02-15 13:24:24
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import cookielib, urllib2, os, PySide.QtCore as _qc, PySide.QtGui as _qg, feedparser, banta, banta.db, banta.packages

class Reader(_qc.QThread):
    newsFetched = _qc.Signal(list)

    def __init__(self):
        _qc.QThread.__init__(self)
        self.feeds = []
        self.messages = []
        self.last = -1
        self.feed_url = b'http://www.moongate.com.ar/feeds/posts/default'
        self.html = b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body>%s</body></html>'

    def __downloadAndConvertImage(self, url):
        """Downloads an image and encodes it at base64 to use when creating the message string
                notice all this info is handled on memory
                this method is private to this class (notice the __)
                idea from syrius @ irc.freenode.net
                """
        try:
            u = urllib2.urlopen(url)
            im = u.read()
            return im.encode(b'base64')
        except:
            return b''

    def __getCookies(self):
        cjk = b'cookies'
        cookiejar = cookielib.CookieJar()
        if cjk in banta.db.DB.root:
            map(cookiejar.set_cookie, banta.db.DB.root[cjk])
            cookiejar.clear_expired_cookies()
        return cookiejar

    def __saveCookies(self, cookiejar):
        cjk = b'cookies'
        banta.db.DB.root[cjk] = list(cookiejar)
        banta.db.DB.commit()

    def getVersion(self):
        p = os.name
        if p == b'nt':
            osn = b'Windows NT 5.1'
        elif p == b'posix':
            osn = b'Linux'
        elif p == b'mac':
            osn = b'Mac OS X'
        else:
            osn = p
        s = _qc.QLocale.system()
        country = s.countryToString(s.country())
        lang = s.name()
        bua = b'Opera/%s (%s; %s; %s)'
        ua = bua % (banta.__version__, osn, country, lang)
        ref = b'http://www.google.com/?q=banta%s' % banta.__version__
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(), urllib2.HTTPHandler(debuglevel=0), urllib2.HTTPSHandler(debuglevel=0))
        opener.addheaders = [
         (
          b'User-agent', ua),
         ('Accept', '*/*'),
         (
          b'Accept-Language', lang),
         (
          b'Referer', ref)]
        url = b'http://www.shinystat.com/cgi-bin/shinystat.cgi?USER=moongate'
        r = opener.open(url)
        code = r.code
        headers = r.info()
        r.read()

    def run(self, *args, **kwargs):
        self.feeds = feedparser.parse(self.feed_url)
        basestr = self.html % b'Novedades:<a href="%s"><img src="data:image/jpeg;base64,%s" width=25 height=25 />  <span style=" font-size:8pt; text-decoration: underline; color:#aaaaff;">%s</span></a> (%s) "%s..."'
        for i in self.feeds.entries:
            dp = i.date_parsed
            d = _qc.QDateTime(dp.tm_year, dp.tm_mon, dp.tm_mday, dp.tm_hour, dp.tm_min, dp.tm_sec)
            text = i.summary
            im = b''
            if b'media_thumbnail' in i and len(i.media_thumbnail) > 0:
                im = self.__downloadAndConvertImage(i.media_thumbnail[0][b'url'])
            msg = basestr % (i.link, im, i.title, d.toString(), text)
            self.messages.append(msg)

        self.newsFetched.emit(self.messages)
        if not banta.db.CONF.DEBUG:
            self.getVersion()


class Feeds(banta.packages.GenericModule):
    REQUIRES = []
    NAME = b'feeds'
    last_message = 0
    reader = None

    def load(self):
        self.goe = _qg.QGraphicsOpacityEffect()
        self.app.window.l_news.setGraphicsEffect(self.goe)
        animation = _qc.QPropertyAnimation(self.goe, b'opacity')
        animation.setDuration(2000)
        animation.setStartValue(0)
        animation.setEndValue(1)
        self.a = animation
        self.timer = _qc.QTimer(self.app)
        self.timer.timeout.connect(self.showMessage)
        self.reader = Reader()
        self.reader.newsFetched.connect(self.addNews, _qc.Qt.QueuedConnection)
        self.reader.finished.connect(self.term)
        self.reader.start()

    @_qc.Slot()
    def showMessage(self):
        """This signal shows a message stored on self.news on the status bar,
                runs on the main thread.
                This is triggered by the self.timer"""
        if not self.news:
            return
        msg = self.news[self.last_message]
        self.last_message += 1
        self.last_message %= len(self.news)
        self.app.window.l_news.setText(msg)
        self.a.start()

    @_qc.Slot(str)
    def addNews(self, news):
        """This slot is called from the runner thread, when the runner has finished.
                news is a list with all the messages (can be html)"""
        self.news = news
        self.last_message = 0
        self.showMessage()
        self.timer.start(60000)

    @_qc.Slot()
    def term(self):
        pass

    def wait(self):
        if self.reader:
            self.reader.wait(5000)


a = b'NOTE ABOUT QTHREADS!!\nDONT add slots to a QThread subclass:\nthey’ll be invoked from the “wrong” thread, that is, not the one the QThread object is managing, but the one that object is living in,\n forcing you to specify a direct connection and/or to use moveToThread(this).\n\n QThread objects are not threads; they’re control objects around a thread, therefore meant to be used from another thread\n  (usually, the one they’re living in).\nA good way to achieve the same result is splitting the “working” part from the “controller” part, that is, writing a\n QObject subclass and using QObject::moveToThread() to change its affinity:\n\nclass Worker : public QObject\n{\n    Q_OBJECT\npublic slots:\n    void doWork() {\n        /* ... */\n    }\n};\n/* ... */\n\nQThread *thread = new QThread;\nWorker *worker = new Worker;\nconnect(obj, SIGNAL(workReady()), worker, SLOT(doWork()));\nworker->moveToThread(thread);\nthread->start();\n'