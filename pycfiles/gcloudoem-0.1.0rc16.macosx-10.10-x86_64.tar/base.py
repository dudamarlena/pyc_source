# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rstuart/.pyenv/versions/gcloudoem/lib/python2.7/site-packages/gcloudoem/datastore/base.py
# Compiled at: 2015-12-14 06:22:18
"""Base classes."""
from __future__ import absolute_import
import threading, httplib2

class BaseConnection(object):
    """
    A generic connection to Google Cloud Platform.

    Subclasses should understand only the basic types in method arguments, however they should be capable of returning
    advanced types.

    A connection in datastore terms is a combination of gcloud credentials and a dataset id (project id). While its
    possible to use the same same credentials across projects in gcloud, it's rarely done and keeping all these things
    together aligns much better with a traditional database.

    If no value is passed in for ``http``, a :class:`httplib2.Http` object will be created and authorized with the
    ``credentials``. If not, the ``credentials`` and ``http`` need not be related.

    Subclasses may seek to use the private key from ``credentials`` to sign data.

    A custom (non-``httplib2``) HTTP object must have a ``request`` method which accepts the following arguments:

    * ``uri``
    * ``method``
    * ``body``
    * ``headers``

    In addition, ``redirections`` and ``connection_type`` may be used and it must be thread safe.

    Without the use of ``credentials.authorize(http)``, a custom ``http`` object will also need to be able to add a
    bearer token to API requests and handle token refresh on 401 errors.
    """
    API_BASE_URL = 'https://www.googleapis.com'
    USER_AGENT = 'gcloud-datastore-oem'

    def __init__(self, dataset, namespace, credentials=None, http=None):
        """
        :type dataset: str
        :param dataset: The gcloud Datastore dataset identifier.

        :type namespace: str
        :param namespace: The gcloud Datastore namespace to use.

        :type credentials: :class:`oauth2client.client.OAuth2Credentials` or :class:`NoneType`
        :param credentials: The OAuth2 Credentials to use for this connection.

        :type http: :class:`httplib2.Http` or class that defines ``request()``.
        :param http: An optional HTTP object to make requests.
        """
        self._local = threading.local()
        self._dataset = dataset
        self._namespace = namespace
        self._http = http
        self._credentials = credentials

    @property
    def dataset(self):
        return self._dataset

    @property
    def namespace(self):
        return self._namespace

    @property
    def credentials(self):
        """
        Getter for current credentials.

        :rtype: :class:`oauth2client.client.OAuth2Credentials` or :class:`NoneType`
        :returns: The credentials object associated with this connection.
        """
        return self._credentials

    @property
    def http(self):
        """
        A getter for the HTTP transport used in talking to the API.

        :rtype: :class:`httplib2.Http`
        :returns: A Http object used to transport data.
        """
        if self._http is not None:
            return self._http
        else:
            if not hasattr(self._local, 'http'):
                self._local.http = httplib2.Http()
                if self._credentials:
                    self._local.http = self._credentials.authorize(self._local.http)
            return self._local.http