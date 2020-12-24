# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialauth/lib/oauthtwitter.py
# Compiled at: 2010-06-28 10:33:16
"""A class the inherits everything from python-twitter and allows oauth based access

Requires:
  python-twitter
  simplejson
  oauth
"""
__author__ = 'Hameedullah Khan <hameed@hameedkhan.net>'
__version__ = '0.1'
from twitter import Api, User
try:
    import json as simplejson
except:
    from django.utils import simplejson

from oauth import oauth
REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'http://twitter.com/oauth/authorize'
SIGNIN_URL = 'http://twitter.com/oauth/authenticate'

class OAuthApi(Api):

    def __init__(self, consumer_key, consumer_secret, access_token=None):
        if access_token:
            Api.__init__(self, access_token.key, access_token.secret)
        else:
            Api.__init__(self)
        self._Consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self._signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self._access_token = access_token

    def _GetOpener(self):
        opener = self._urllib.build_opener()
        return opener

    def _FetchUrl(self, url, post_data=None, parameters=None, no_cache=None):
        """Fetch a URL, optionally caching for a specified time.
    
        Args:
          url: The URL to retrieve
          post_data: 
            A dict of (str, unicode) key/value pairs.  If set, POST will be used.
          parameters:
            A dict whose key/value pairs should encoded and added 
            to the query string. [OPTIONAL]
          no_cache: If true, overrides the cache on the current request
    
        Returns:
          A string containing the body of the response.
        """
        extra_params = {}
        try:
            if self._default_params:
                extra_params.update(self._default_params)
        except AttributeError:
            pass

        if parameters:
            extra_params.update(parameters)
        if post_data:
            http_method = 'POST'
            extra_params.update(post_data)
        else:
            http_method = 'GET'
        req = self._makeOAuthRequest(url, parameters=extra_params, http_method=http_method)
        self._signRequest(req, self._signature_method)
        opener = self._GetOpener()
        if post_data:
            encoded_post_data = req.to_postdata()
            url = req.get_normalized_http_url()
        else:
            url = req.to_url()
            encoded_post_data = ''
        no_cache = True
        if encoded_post_data or no_cache:
            if encoded_post_data:
                url_data = opener.open(url, encoded_post_data).read()
            else:
                url_data = opener.open(url).read()
            opener.close()
        else:
            if self._username:
                key = self._username + ':' + url
            else:
                key = url
            last_cached = self._cache.GetCachedTime(key)
            if not last_cached or time.time() >= last_cached + self._cache_timeout:
                url_data = opener.open(url).read()
                opener.close()
                self._cache.Set(key, url_data)
            else:
                url_data = self._cache.Get(key)
        return url_data

    def _makeOAuthRequest(self, url, token=None, parameters=None, http_method='GET'):
        """Make a OAuth request from url and parameters
        
        Args:
          url: The Url to use for creating OAuth Request
          parameters:
             The URL parameters
          http_method:
             The HTTP method to use
        Returns:
          A OAauthRequest object
        """
        if not token:
            token = self._access_token
        request = oauth.OAuthRequest.from_consumer_and_token(self._Consumer, token=token, http_url=url, parameters=parameters, http_method=http_method)
        return request

    def _signRequest(self, req, signature_method=oauth.OAuthSignatureMethod_HMAC_SHA1()):
        """Sign a request
        
        Reminder: Created this function so incase
        if I need to add anything to request before signing
        
        Args:
          req: The OAuth request created via _makeOAuthRequest
          signate_method:
             The oauth signature method to use
        """
        req.sign_request(signature_method, self._Consumer, self._access_token)

    def getAuthorizationURL(self, token, url=AUTHORIZATION_URL, callback_url=None):
        """Create a signed authorization URL
        
        Returns:
          A signed OAuthRequest authorization URL 
        """
        if callback_url:
            parameters = {'oauth_callback': callback_url}
        else:
            parameters = {}
        req = self._makeOAuthRequest(url, token=token, parameters=parameters)
        self._signRequest(req)
        return req.to_url()

    def getSigninURL(self, token, url=SIGNIN_URL, callback_url=None):
        """Create a signed Sign-in URL
        
        Returns:
          A signed OAuthRequest Sign-in URL 
        """
        signin_url = self.getAuthorizationURL(token, url, callback_url)
        return signin_url

    def getAccessToken(self, url=ACCESS_TOKEN_URL):
        token = self._FetchUrl(url, no_cache=True)
        return oauth.OAuthToken.from_string(token)

    def getRequestToken(self, url=REQUEST_TOKEN_URL):
        """Get a Request Token from Twitter
        
        Returns:
          A OAuthToken object containing a request token
        """
        resp = self._FetchUrl(url, no_cache=True)
        token = oauth.OAuthToken.from_string(resp)
        return token

    def GetUserInfo(self, url='https://twitter.com/account/verify_credentials.json'):
        """Get user information from twitter
        
        Returns:
          Returns the twitter.User object
        """
        json = self._FetchUrl(url)
        data = simplejson.loads(json)
        self._CheckForTwitterError(data)
        return User.NewFromJsonDict(data)