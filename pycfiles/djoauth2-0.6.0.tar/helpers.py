# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/peterdowns/Desktop/djoauth2/djoauth2/helpers.py
# Compiled at: 2014-04-04 14:41:32
import random, urlparse
from string import ascii_letters
from string import digits
from urllib import urlencode
BEARER_TOKEN_CHARSET = ascii_letters + digits + '-._~'
AUTHORIZATION_CODE_CHARSET = ascii_letters + digits + '-._~'
CLIENT_KEY_CHARSET = ascii_letters + digits + '-._~'
CLIENT_SECRET_CHARSET = ascii_letters + digits + '-._~'

def random_string(length, charset):
    rand = random.SystemRandom()
    return ('').join(rand.choice(charset) for i in xrange(length))


def make_bearer_token(length):
    return lambda : random_string(length, BEARER_TOKEN_CHARSET)


def make_authorization_code(length):
    return lambda : random_string(length, AUTHORIZATION_CODE_CHARSET)


def make_client_secret(length):
    return lambda : random_string(length, CLIENT_SECRET_CHARSET)


def make_client_key(length):
    return lambda : random_string(length, CLIENT_KEY_CHARSET)


def update_parameters(url, parameters, encoding='utf8'):
    """ Updates a URL's existing GET parameters.

  :param url: a base URL to which to add additional parameters.
  :param parameters: a dictionary of parameters, any mix of
    unicode and string objects as the parameters and the values.
  :parameter encoding: the byte encoding to use when passed unicode
    for the base URL or for keys and values of the parameters dict. This
    isnecessary because `urllib.urlencode` calls the `str()` function on all of
    its inputs.  This raises a `UnicodeDecodeError` when it encounters a
    unicode string with characters outside of the default ASCII charset.
  :rtype: a string URL.
  """
    if isinstance(url, unicode):
        url = url.encode(encoding)
    parsed_url = urlparse.urlparse(url)
    existing_query_parameters = urlparse.parse_qsl(parsed_url.query)
    byte_parameters = []
    for key, value in existing_query_parameters + parameters.items():
        if isinstance(key, unicode):
            key = key.encode(encoding)
        if isinstance(value, unicode):
            value = value.encode(encoding)
        byte_parameters.append((key, value))

    return urlparse.urlunparse((
     parsed_url.scheme,
     parsed_url.netloc,
     parsed_url.path,
     parsed_url.params,
     urlencode(byte_parameters),
     parsed_url.fragment))