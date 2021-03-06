# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/downloader.py
# Compiled at: 2011-05-10 14:38:51
import logging
logger = logging.getLogger('downloader')
import connection

class FileDownloader:
    USER_AGENT = 'User-Agent: Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.12) Gecko/2009070811  Windows NT Firefox/3.1'
    opener_installed = False

    def __init__(self, username, password, cookiefile, login_callback):
        self.username = username
        self.password = password
        self.cookiefile = cookiefile
        self.logged_in = False
        from socket import setdefaulttimeout
        setdefaulttimeout(30)
        self.opener_installed = False
        self.login_callback = login_callback

    def update_userdata(self, username, password):
        from os import path, remove
        self.username = username
        self.password = password
        self.logged_in = False
        if path.exists(self.cookiefile):
            try:
                remove(self.cookiefile)
            except:
                logger.info('Could not remove cookie file?!')

    def login(self):
        if connection.offline:
            raise Exception("Can't connect in offline mode.")
        if self.username == '' or self.password == '':
            raise Exception('Please configure your username/password and restart the application')
        logger.info('Checking Login status')
        from cookielib import LWPCookieJar
        cj = LWPCookieJar(self.cookiefile)
        if not self.opener_installed:
            from urllib2 import build_opener, install_opener, HTTPCookieProcessor
            opener = build_opener(HTTPCookieProcessor(cj))
            install_opener(opener)
            self.opener_installed = True
        try:
            cj.load()
            logger.info('Loaded cookie file')
        except IOError, e:
            logger.info("Couldn't load cookie file")
        else:
            logger.info('Checking if still logged in...')
            url = 'http://www.geocaching.com/seek/nearest.aspx'
            page = self.get_reader(url, login=False)
            for line in page:
                if 'Hello, ' in line:
                    self.logged_in = True
                    logger.info("Seems as we're still logged in")
                    page.close()
                    return
                elif 'Welcome, Visitor!' in line:
                    logger.info('Nope, not logged in anymore')
                    page.close()
                    break

            logger.info('Logging in')
            (url, values) = self.login_callback(self.username, self.password)
            page = self.get_reader(url, values, login=False)
            for line in page:
                if 'You are logged in as' in line:
                    break
                elif 'Welcome, Visitor!' in line or 'combination does not match' in line:
                    raise Exception('Wrong password or username!')
            else:
                logger.info('Seems as if the language is set to something other than english')
                raise Exception('Please go to geocaching.com and set the website language to english!')

            logger.info('Great success.')
            self.logged_in = True
            try:
                cj.save()
            except Exception, e:
                logger.info('Could not save cookies: %s' % e)

    def get_reader(self, url, values=None, data=None, login=True):
        if connection.offline:
            raise Exception("Can't connect in offline mode.")
        from urllib import urlencode
        from urllib2 import Request, urlopen
        if login and not self.logged_in:
            self.login()
        if values == None and data == None:
            req = Request(url)
            self.add_headers(req)
            return urlopen(req)
        else:
            if data == None:
                if isinstance(values, dict):
                    values = urlencode(values)
                req = Request(url, values)
                self.add_headers(req)
                return urlopen(req)
            if values == None:
                (content_type, body) = data
                req = Request(url)
                req.add_header('Content-Type', content_type)
                req.add_header('Content-Length', len(str(body)))
                self.add_headers(req)
                req.add_data(body)
                return urlopen(req)
            return

    def encode_multipart_formdata(self, fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)

        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)

        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return (
         content_type, body)

    @staticmethod
    def get_content_type(filename):
        import mimetypes
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def add_headers(self, req):
        req.add_header('User-Agent', self.USER_AGENT)
        req.add_header('Cache-Control', 'no-cache')
        req.add_header('Pragma', 'no-cache')