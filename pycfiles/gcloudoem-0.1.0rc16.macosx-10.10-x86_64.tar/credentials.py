# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rstuart/.pyenv/versions/gcloudoem/lib/python2.7/site-packages/gcloudoem/datastore/credentials.py
# Compiled at: 2016-10-04 00:20:35
"""A simple wrapper around the OAuth2 credentials library."""
from __future__ import absolute_import, division, print_function, unicode_literals
import base64, calendar, datetime
from oauth2client import client
import pytz, six
from six.moves.urllib.parse import urlencode

def get_credentials():
    """
    Gets credentials implicitly from the current environment.

    .. note::
      You should not need to use this function directly. Instead, use the helper method
      :func:`gcloudoem.datastore.__init__.get_connection` which uses this method under the hood.

    Checks environment in order of precedence:

    * Google App Engine (production and testing)
    * Environment variable GOOGLE_APPLICATION_CREDENTIALS pointing to a file with stored credentials information.
    * Stored "well known" file associated with ``gcloud`` command line tool.
    * Google Compute Engine production environment.

    The file referred to in GOOGLE_APPLICATION_CREDENTIALS is expected to contain information about credentials that are
    ready to use. This means either service account information or user account information with a ready-to-use refresh
    token::

      {                                       {
          'type': 'authorized_user',              'type': 'service_account',
          'client_id': '...',                     'client_id': '...',
          'client_secret': '...',       OR        'client_email': '...',
          'refresh_token': '...,                  'private_key_id': '...',
      }                                           'private_key': '...',
                                              }

    The second of these is simply a JSON key downloaded from the Google APIs console. The first is a close cousin of the
    "client secrets" JSON file used by ``oauth2client.clientsecrets`` but differs in formatting.

    :rtype: :class:`oauth2client.client.GoogleCredentials`,
            :class:`oauth2client.appengine.AppAssertionCredentials`,
            :class:`oauth2client.gce.AppAssertionCredentials`,
            :class:`oauth2client.service_account._ServiceAccountCredentials`
    :returns: A new credentials instance corresponding to the implicit environment.
    """
    return client.GoogleCredentials.get_application_default()


def _get_signed_query_params(credentials, expiration, string_to_sign):
    """Gets query parameters for creating a signed URL.
    :type credentials: :class:`oauth2client.client.AssertionCredentials`
    :param credentials: The credentials used to create a private key
                        for signing text.
    :type expiration: int or long
    :param expiration: When the signed URL should expire.
    :type string_to_sign: string
    :param string_to_sign: The string to be signed by the credentials.
    :raises AttributeError: If :meth: sign_blob is unavailable.
    :rtype: dict
    :returns: Query parameters matching the signing credentials with a
              signed payload.
    """
    if not hasattr(credentials, b'sign_blob'):
        auth_uri = b'http://google-cloud-python.readthedocs.io/en/latest/google-cloud-auth.html#setting-up-a-service-account'
        raise AttributeError(b'you need a private key to sign credentials.the credentials you are currently using %s just contains a token. see %s for more details.' % (
         type(credentials), auth_uri))
    _, signature_bytes = credentials.sign_blob(string_to_sign)
    signature = base64.b64encode(signature_bytes)
    service_account_name = credentials.service_account_email
    return {b'GoogleAccessId': service_account_name, 
       b'Expires': str(expiration), 
       b'Signature': signature}


def _utcnow():
    """Returns current time as UTC datetime.

    NOTE: on the module namespace so tests can replace it.
    """
    return datetime.datetime.utcnow()


def _get_expiration_seconds(expiration):
    """
    Convert 'expiration' to a number of seconds in the future.

    :type expiration: int, long, datetime.datetime, datetime.timedelta
    :param expiration: When the signed URL should expire.

    :rtype: int
    :returns: a timestamp as an absolute number of seconds.
    """
    if isinstance(expiration, datetime.timedelta):
        now = _utcnow().replace(tzinfo=pytz.utc)
        expiration = now + expiration
    if isinstance(expiration, datetime.datetime):
        if expiration.tzinfo:
            expiration = expiration.astimezone(pytz.utc)
        else:
            expiration = expiration.replace(tzinfo=pytz.utc)
        expiration = int(calendar.timegm(expiration.timetuple()))
    if not isinstance(expiration, six.integer_types):
        raise TypeError(b'Expected an integer timestamp, datetime, or timedelta. Got %s' % type(expiration))
    return expiration


def generate_signed_url(credentials, resource, expiration, api_access_endpoint=b'', method=b'GET', content_md5=None, content_type=None):
    """Generate signed URL to provide query-string auth'n to a resource.

    :type credentials: :class:`oauth2client.appengine.AppAssertionCredentials`
    :param credentials: Credentials object with an associated private key to sign text.

    :param str resource: A pointer to a specific resource (typically, ``/bucket-name/path/to/blob.txt``).

    :type expiration: int, long, datetime.datetime, datetime.timedelta
    :param expiration: When the signed URL should expire.

    :param str api_access_endpoint: Optional URI base. Defaults to empty string.

    :param str method: The HTTP verb that will be used when requesting the URL.

    :param str content_md5: The MD5 hash of the object referenced by ``resource``.

    :param str content_type: The content type of the object referenced by ``resource``.

    :rtype: string
    :returns: A signed URL you can use to access the resource until expiration.
    """
    expiration = _get_expiration_seconds(expiration)
    signature_string = (b'\n').join([
     method,
     content_md5 or b'',
     content_type or b'',
     str(expiration),
     resource])
    query_params = _get_signed_query_params(credentials, expiration, signature_string)
    return (b'{endpoint}{resource}?{querystring}').format(endpoint=api_access_endpoint, resource=resource, querystring=urlencode(query_params))