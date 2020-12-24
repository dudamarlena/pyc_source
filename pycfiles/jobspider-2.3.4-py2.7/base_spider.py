# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\jobspider\baseclass\base_spider.py
# Compiled at: 2016-03-20 20:41:25
import urllib, urllib2, requests, json, re, os, ConfigParser
from bs4 import BeautifulSoup
from cStringIO import StringIO
import cookielib, xml.etree.ElementTree as ET
from .utils.get_user_agent import get_user_agent
from .config import ByrCfg, Job51Cfg, ZhiCfg, LgCfg, DjCfg

class Base_Spider(object):

    def __init__(self, sitename, *args):
        """
        it's the name of the website that you'll visit,
        it's used to get config info from config file
        """
        self.sitename = sitename
        self.setHeaders(*args)

    def setHeaders(self, *args):
        """
        add header in order to model explorer,including:
        User-Agent,Referer,Host
        :return:None
        """
        self.headers = {}
        self.headers.setdefault('User-Agent', get_user_agent())
        for key in args[0]:
            self.get_cfg(self.headers, key)

    def get_cfg(self, field, key):
        SiteCfg = {'byr': ByrCfg(), 'lagou': LgCfg(), 'zhilian': ZhiCfg(), '51job': Job51Cfg(), 'dajie': DjCfg()}
        self.cfg = SiteCfg[self.sitename]
        if key == 'X-Requested-With':
            field[key] = getattr(self.cfg, 'X_Requested_With')
        else:
            field[key] = getattr(self.cfg, key)

    def build_opener(self, save=False):
        if not save:
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler)
        else:
            cj = cookielib.MozillaCookieJar()
            cj.save('cookie.txt', ignore_discard=True, ignore_expires=True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        return opener

    def login(self, posturl, postdata):
        """
        self.build_opener()
        postdata = urllib.urlencode(postdata)
        request = urllib2.Request(url=posturl,data=postdata,headers=self.headers)
        #print self.opener.open(request)
        resp = urllib2.urlopen(request).read()
        print resp
        """
        self.session = requests.Session()
        r = self.session.post(posturl, data=postdata)
        if not isinstance(r.cookies, dict):
            return dict(r.cookies)
        return r.cookies

    def get_content(self, url, url_type='html', cookies=None):
        if 'X-Requested-With' not in self.headers.keys():
            content = requests.get(url, headers=self.headers)
            try:
                content = content.content
            except UnicodeEncodeError:
                content = content.text.encode('utf-8')
            except UnicodeDecodeError:
                print 'test'
                content = content.text

        else:
            opener = self.build_opener()
            header_list = []
            for key in self.headers.keys():
                header_list.append((key, self.headers[key]))

            opener.addheaders = header_list
            content = opener.open(url).read()
            try:
                if not isinstance(content, basestring and unicode):
                    content = content.decode('GBK').encode('utf8')
            except UnicodeDecodeError:
                pass

        content = StringIO(content)
        if url_type == 'json':
            return json.load(content)
        else:
            if url_type == 'xml':
                return ET.parse(content)
            return BeautifulSoup(content, 'html5lib')

    def login_get_content(self, url, url_type='html', cookies=None):
        content = self.session.get(url, timeout=15) if cookies is None else self.session.get(url, cookies=cookies)
        try:
            content = content.content
        except UnicodeEncodeError:
            content = content.text.encode('utf-8')
        except UnicodeDecodeError:
            print 'test'
            content = content.text

        content = StringIO(content)
        if url_type == 'json':
            return json.load(content)
        else:
            if url_type == 'xml':
                return ET.parse(content)
            else:
                return BeautifulSoup(content, 'html5lib')

            return

    def store(self):
        pass

    def upload_file(self, url, filename):
        with file(filename, 'rb') as (f):
            requests.post(url, data=f)

    def download(self, imgurl, filename):
        resp = requests.get(imgurl)
        with file(filename, 'wb') as (f):
            f.write(resp.content)


if __name__ == '__main__':
    spider = Base_Spider('lagou', ['Host'])
    print spider.headers