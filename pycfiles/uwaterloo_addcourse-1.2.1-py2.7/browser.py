# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/addcourse/browser.py
# Compiled at: 2015-04-26 11:03:29
"""The QuestBrowser class that manages interactions with QUEST."""
import urllib, urllib2, bs4
from .error import *

class QuestBrowser:
    """An opener for browsing QUEST."""
    req = None

    def __init__(self, questid, password):
        self.opener = urllib2.build_opener()
        self.opener.add_handler(urllib2.HTTPSHandler())
        self.opener.add_handler(urllib2.HTTPRedirectHandler())
        self.opener.add_handler(urllib2.HTTPCookieProcessor())
        self.questid = questid.upper()
        self.login(password)

    def open(self, req):
        """Open a request req to QUEST via self.opener."""
        if isinstance(req.data, str):
            req.data = req.data.encode('ascii')
        return self.opener.open(req)

    def add_data(self, data):
        """Add data to self.req."""
        if self.req is None:
            raise Error('request cannot be None')
        self.req.data = data
        return

    def get_page(self, req=None):
        """Return a BeautifulSoup instance for url."""
        if req is None:
            if self.req is None:
                raise Error('request cannot be None')
            req = self.req
            if self.data:
                req.data = urllib.urlencode(self.data)
                self.data = None
        f = self.open(req)
        self.page = f.read()
        f.close()
        if req is self.req:
            self.req = None
        self.page = bs4.BeautifulSoup(self.page)
        return self.page

    def make_request(self, page, query={}):
        """Make a Request object for a QUEST page."""
        self.data = {}
        self.req = urllib2.Request(proto + '://' + quest_url + page + ('?' + urllib.urlencode(query) if query != {} else ''))

    def add_header(self, key, val):
        """Add key and val to the header of self.req."""
        self.req.add_header(key, val)

    def add_form(self, key, val):
        """Add key=val to the data field of self.req."""
        if not isinstance(self.data, dict):
            raise Error('Need to call self.make_request before calling self.add_form.')
        if not isinstance(key, str):
            key = str(key)
        if not isinstance(val, str):
            val = str(val)
        self.data[key] = val

    def add_forms(self, d):
        """Add key, value pairs from d to self.data."""
        for k, v in d.items():
            self.add_form(k, v)

    def login(self, password):
        """Login to QUEST."""
        assert password is not None
        self.make_request('/psc/AS/', {'cmd': 'login', 'languageCd': 'ENG'})
        self.add_forms({'userid': self.questid, 'pwd': password, 
           'httpPort': '', 
           'timezoneOffset': '240', 
           'Submit': 'Sign+in'})
        self.get_page()
        if self.page.find(text=invalid_id_pass_msg):
            raise BadLogin(invalid_id_pass_msg)
        return


proto = 'https'
quest_url = 'quest.pecs.uwaterloo.ca'
invalid_id_pass_msg = 'Your User ID and/or Password are invalid.'