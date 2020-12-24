# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dvdje/vbulletin.py
# Compiled at: 2013-10-29 23:55:39
# Size of source mod 2**32: 4512 bytes
"""VBulletin requests helper."""
import hashlib, http.cookiejar, logging, urllib.parse, urllib.request
logger = logging.getLogger(__name__)

class Requests(object):
    __doc__ = 'Various functions to make reading stuff from VBulletin forums easier.\n    '

    def __init__(self, base_url, login_url='login.php'):
        self.url = base_url
        self.login_url = login_url
        self.jar = http.cookiejar.CookieJar()

    def request(self, url, data=None, extra_headers=None, timeout=30):
        """Sends a request and returns the response object.

        Required arguments:
        url -- the absolute or relative URL to send the request to

        Optional arguments:
        data -- a bytes string or mapping of POST data
        extra_headers -- a mapping of HTTP headers and values
        timeout -- seconds to wait for a response before giving up (default 30)

        """
        if '://' not in url:
            url = '/'.join((self.url, url))
        logger.debug('Building request to %s', url)
        if data:
            if not isinstance(data, bytes):
                data = urllib.parse.urlencode(data).encode('utf8', errors='ignore')
        headers = {'User-Agent': 'Mozilla/5.0',  'Accept-Language': 'en-us,en', 
         'Referer': url}
        if extra_headers:
            headers.update(extra_headers)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        opener.addheaders = headers.items()
        if data:
            logger.debug('Sending request to %s with data: %s', url, repr(data))
        else:
            logger.debug('Sending request to %s', url)
        return opener.open(url, data, timeout=timeout)

    def html(self, url, data=None, extra_headers=None, timeout=30):
        """Sends a request and returns the HTML body of the response.

        Required Arguments:
        url -- the absolute or relative URL to send the request to

        Optional arguments:
        data -- a mapping of POSTDATA fields and values
        extra_headers -- a mapping of HTTP header fields and values
        timeout -- seconds to wait for a response before giving up (default 30)

        """
        response = self.request(url, data, extra_headers, timeout)
        return response.read().decode('utf8', errors='ignore')

    def login(self, username, password):
        """Logs into a VBulletin forum as a specified user.

        The log-in cookie is stored in a class instance cookie jar.

        Required keywords:
        username -- user to log in as
        password -- user's password

        Exceptions:
        ValueError -- if log-in fails

        """
        logger.debug('Attempting to log in as %s', username)
        if not isinstance(password, bytes):
            password = password.encode('utf8', errors='ignore')
        password = hashlib.md5(password).hexdigest()
        postdata = {'do': 'login', 
         's': '', 
         'security_token': 'guest', 
         'vb_login_md5password': password, 
         'vb_login_md5password_utf': password, 
         'vb_login_username': username}
        html = self.html(self.login_url, postdata)
        if '<!-- BEGIN TEMPLATE: STANDARD_ERROR -->' in html:
            msg = 'Failed to log in as {}'.format(username)
            logger.error(msg)
            raise ValueError(msg)
        logger.debug('Successfully logged in as %s', username)