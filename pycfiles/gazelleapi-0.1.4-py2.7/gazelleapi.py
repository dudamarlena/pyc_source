# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazelleapi/gazelleapi.py
# Compiled at: 2016-12-20 08:39:16
"""
A generic API that can be used to access trackers that operate on the gazelle platform
(assuming they haven't customized it too much, such as adding a CAPTCHA to their login).

After initializing the API connection, the main two functions are going to be request
and request_html. The available actions for request (and the needed parameters) can be
found at https://github.com/WhatCD/Gazelle/wiki/JSON-API-Documentation. request_html
just returns the html of any specific php page that you would want. An example would be
if you wanted to get the rules for the site, you would do request_html('rules') and it
would return the html content for the page /rules.php. There are other general functions
available as well provided for convinence.

This API is based off https://github.com/isaaczafuta/whatapi and
https://github.com/rguedes/xanaxbetter repositories, with some modifications to make them
cross python version usable.
"""
from __future__ import print_function, unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import str
import configparser, time, requests
HEADERS = {b'Connection': b'keep-alive', 
   b'Cache-Control': b'max-age=0', 
   b'User-Agent': b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11', 
   b'Accept': b'text/html,application/xhtml+xml,application/xml;q=0.9 ,*/*;q=0.8', 
   b'Accept-Encoding': b'gzip,deflate,sdch', 
   b'Accept-Language': b'en-US,en;q=0.8', 
   b'Accept-Charset': b'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}

class LoginException(Exception):
    """
    Exception for when we hit an error logging in (either bad page response, or
    invalid login credentials)
    """
    pass


class RequestException(Exception):
    """
    Exception for when we hit a page error when making a request to the ajax.php page
    """
    pass


class GazelleAPI(object):
    """
    Generic API object that should work across trackers assuming that they haven't
    diverged that much from the base (like disable ajax.php). This API can be used
    with a config file (that can be read through configparser) or through using
    direct arguments, but not both. We also allow a combination of https for either
    site or tracker as some trackers just aren't there yet.

    Attributes:
        username (str): username used to log into the site
        password (str): password used to log into the site
        site_url (str): formed URL for accessing the tracker site
        announce_url (str): formed URL (including port) for the announce URL in the torrent files
        last_request (int): When was the last request made using the API
        rate_limit (float): How often (in seconds) are requests allowed through the API
        session (requests.Session): stored session object to run requests through to maintain login
        user_id (int): user id on the site
        authkey (str): authkey given to you from the site
        passkey (str): passkey given to you from the site
    """

    def __init__(self, config_file=None, username=None, password=None, site_url=None, announce_url=None, cookies=None):
        """
        Constructor for the API, setups the various attributes so that we can then connect
        to the tracker using connect() (which we call at the end of this function).

        :param config_file: path to a config file (readable by configparser) that contains all
                            other variables to be used. If defined, all other arguments can be
                            left blank
        :param username: usernamed for site
        :param password: password for the site
        :param site_url: url for the site (including schema)
        :param announce_url: url for announce (but not including the passkey or anything after)
        :param cookies: optional flag to use cookie store for authentication on session
        """
        if config_file:
            config = configparser.ConfigParser()
            config.read(config_file)
            self.username = config.get(b'login', b'username')
            self.password = config.get(b'login', b'password')
            self.site_url = config.get(b'site', b'site_url')
            self.announce_url = config.get(b'site', b'announce_url')
        else:
            self.username = username
            self.password = password
            self.site_url = site_url
            self.announce_url = announce_url
        if not isinstance(self.site_url, str) or not isinstance(self.announce_url, str):
            raise ValueError(b'The urls should be strings')
        self.site_url = self.site_url.rstrip(b'/')
        self.announce_url = self.announce_url.rstrip(b'/')
        self.last_request = time.time()
        self.rate_limit = 2.0
        self.session = None
        self.user_id = None
        self.authkey = None
        self.passkey = None
        self.connect(cookies=cookies)
        return

    def connect(self, cookies=None):
        """
        Connects to the tracker site using either the cookie store (if available) or by going
        through the login page

        :param cookies:
        """
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        if cookies:
            self.session.cookies = cookies
            try:
                self.auth()
            except RequestException:
                self.login()

        else:
            self.login()
        self.announce_url += b'/' + self.passkey + b'/announce'

    def request(self, action, **kwargs):
        """
        Makes an AJAX request against the server to ajax.php to interact with the Gazelle "API".
        The available actions are located on WhatCD's github page for gazelle located at
        https://github.com/WhatCD/Gazelle/wiki/JSON-API-Documentation. Some sites may have added
        additional endpoints, changed the ones that are documented, or completely disabled AJAX
        feature (like PTP). If the request fails for whatever reason, a RequestException is raised.

        :param action:
        :param kwargs:
        :return: dictionary representing json response
        :raises: RequestException
        """
        self._rate_limit()
        ajax_url = self.site_url + b'/ajax.php'
        params = {b'action': action}
        if self.authkey:
            params[b'auth'] = self.authkey
        params.update(kwargs)
        req = self.session.get(ajax_url, params=params, allow_redirects=False)
        try:
            json_response = req.json()
            if json_response[b'status'] != b'success':
                raise RequestException(b'Failed ajax request for ' + action)
            return json_response[b'response']
        except ValueError:
            raise RequestException(b'Failed ajax request for ' + action)

    def request_html(self, action, **kwargs):
        """
        Some pages/features are not available through the AJAX requests (such as better.php),
        making it necessary to make a request directly to the page and then returning the html
        from the page (assuming we could get the page, as we'll raise an exception if we cannot).

        :param action:
        :param kwargs:
        :return: text containing html of the page (to be parsed by beautifulsoup or something)
        :raises: RequestException
        """
        requested_page = (b'{}/{}.php').format(self.site_url, action)
        if self.authkey:
            kwargs[b'authkey'] = self.authkey
        req = self.session.get(requested_page, params=kwargs, allow_redirects=False)
        if req.status_code != 200 or not req.url.startswith(requested_page):
            raise RequestException(b'Failed html request for ' + action)
        return req.content

    def auth(self):
        """
        Test Authentication for a user against the "index" API which gives us some basic user data
        or would fail (which means we aren't authenticated).

        :raises: RequestException
        """
        account_info = self.request(b'index')
        self.user_id = account_info[b'id']
        self.authkey = account_info[b'authkey']
        self.passkey = account_info[b'passkey']

    def login(self):
        """
        Logs the user into the tracker by going through the login page. This assumes that we do not
        have anything more complex on the login page than just username/password field as we'll
        fall over if there's some sort of CAPTCHA (such as PTP's "what's the name of this movie?")

        :raises: LoginException
        """
        login_url = self.site_url + b'/login.php'
        data = {b'username': self.username, b'password': self.password}
        req = self.session.post(login_url, data=data)
        if req.status_code != 200:
            raise LoginException(b'Issue communicating with the server...')
        elif req.url == login_url:
            raise LoginException(b'Could not authenticate that username/password combo')
        account_info = self.request(b'index')
        self.user_id = account_info[b'id']
        self.authkey = account_info[b'authkey']
        self.passkey = account_info[b'passkey']

    def logout(self):
        """
        Logs the user out of the tracker, killing their ongoing session, and resetting thier
        various keys needed for interacting with the site. If you wanted to keep using this
        API instance, you'd have to reconnect using the connect() method.

        :return:
        """
        params = {b'auth': self.authkey}
        self.session.get(self.site_url + b'/logout.php', params=params, allow_redirects=False)
        self.session.close()
        self.user_id = None
        self.authkey = None
        self.passkey = None
        return

    def download_torrent(self, torrent_id):
        """
        Given the id of a torrent, download it from the tracker, returning the content of the file,
        which is left to the user to save. The recommended method would be:

        >>> from future import standard_library
        >>> standard_library.install_aliases()
        >>> from io import StringIO
        >>> api = GazelleAPI(username="user", password="user", hostname="site.com")
        >>> t = api.download_torrent(123456)
        >>> with open("file.torrent", "wb") as open_file:
        ...     open_file.write(StringIO(t))

        :param torrent_id:
        :return:
        """
        self._rate_limit()
        params = {b'action': b'download', b'id': torrent_id}
        if self.authkey:
            params[b'authkey'] = self.authkey
            params[b'torrent_pass'] = self.passkey
        req = self.session.get(self.site_url + b'/torrents.php', params=params, allow_redirects=False)
        if req.status_code == 200 and b'application/x-bittorent' in req.headers[b'content-type']:
            return req.content
        else:
            return

    def get_artist(self, artist_id=None, torrent_format=None, best_seeded=True):
        """
        Gets the artist data from API and returns the torrrents that match our format criteria (if
        defined). Generally, we only want the best seeded versions of a torrent, but we could
        respond with all versions as well if best_seeded is false.

        :param artist_id:
        :param torrent_format:
        :param best_seeded:
        :return:
        """
        self._rate_limit()
        res = self.request(b'artist', id=artist_id)
        torrent_groups = res[b'torrentgroup']
        keep_releases = []
        for release in torrent_groups:
            torrents = release[b'torrent']
            best_torrent = torrents[0]
            keep_torrents = []
            for torrent in torrents:
                if torrent_format and torrent[b'format'] == torrent_format:
                    if best_seeded:
                        if torrent[b'seeders'] > best_torrent[b'seeders']:
                            keep_torrents = [
                             torrent]
                            best_torrent = torrent
                    else:
                        keep_torrents.append(torrent)

            release[b'torrent'] = list(keep_torrents)
            if len(release[b'torrent']):
                keep_releases.append(release)

        res[b'torrentgroup'] = keep_releases
        return res

    def _rate_limit(self):
        """
        Helper method to prevent this script from hammering the server with a ton of requests
        putting undue stress on the server. The amount of time that we're delayed is relatively
        inconsequential in the grand scheme of things (default is 2 seconds).

        :return:
        """
        time_between = time.time() - self.last_request
        if time_between < self.rate_limit:
            time.sleep(time_between)
        self.last_request = time.time()