# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudsearch2/document.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 11630 bytes
import boto.exception
from boto.compat import json
import requests, boto
from boto.cloudsearchdomain.layer1 import CloudSearchDomainConnection

class SearchServiceException(Exception):
    pass


class CommitMismatchError(Exception):
    errors = None


class EncodingError(Exception):
    """EncodingError"""
    pass


class ContentTooLongError(Exception):
    """ContentTooLongError"""
    pass


class DocumentServiceConnection(object):
    """DocumentServiceConnection"""

    def __init__(self, domain=None, endpoint=None):
        self.domain = domain
        self.endpoint = endpoint
        if not self.endpoint:
            self.endpoint = domain.doc_service_endpoint
        self.documents_batch = []
        self._sdf = None
        self.proxy = {}
        self.sign_request = False
        if self.domain and self.domain.layer1:
            if self.domain.layer1.use_proxy:
                self.proxy = {'http': self.domain.layer1.get_proxy_url_with_auth()}
            self.sign_request = getattr(self.domain.layer1, 'sign_request', False)
            if self.sign_request:
                layer1 = self.domain.layer1
                self.domain_connection = CloudSearchDomainConnection(host=self.endpoint, aws_access_key_id=layer1.aws_access_key_id, aws_secret_access_key=layer1.aws_secret_access_key, region=layer1.region, provider=layer1.provider)

    def add(self, _id, fields):
        """
        Add a document to be processed by the DocumentService

        The document will not actually be added until :func:`commit` is called

        :type _id: string
        :param _id: A unique ID used to refer to this document.

        :type fields: dict
        :param fields: A dictionary of key-value pairs to be uploaded .
        """
        d = {'type': 'add',  'id': _id,  'fields': fields}
        self.documents_batch.append(d)

    def delete(self, _id):
        """
        Schedule a document to be removed from the CloudSearch service

        The document will not actually be scheduled for removal until
        :func:`commit` is called

        :type _id: string
        :param _id: The unique ID of this document.
        """
        d = {'type': 'delete',  'id': _id}
        self.documents_batch.append(d)

    def get_sdf(self):
        """
        Generate the working set of documents in Search Data Format (SDF)

        :rtype: string
        :returns: JSON-formatted string of the documents in SDF
        """
        if self._sdf:
            return self._sdf
        return json.dumps(self.documents_batch)

    def clear_sdf(self):
        """
        Clear the working documents from this DocumentServiceConnection

        This should be used after :func:`commit` if the connection will be
        reused for another set of documents.
        """
        self._sdf = None
        self.documents_batch = []

    def add_sdf_from_s3(self, key_obj):
        """
        Load an SDF from S3

        Using this method will result in documents added through
        :func:`add` and :func:`delete` being ignored.

        :type key_obj: :class:`boto.s3.key.Key`
        :param key_obj: An S3 key which contains an SDF
        """
        self._sdf = key_obj.get_contents_as_string()

    def _commit_with_auth(self, sdf, api_version):
        return self.domain_connection.upload_documents(sdf, 'application/json')

    def _commit_without_auth(self, sdf, api_version):
        url = 'http://%s/%s/documents/batch' % (self.endpoint, api_version)
        session = requests.Session()
        session.proxies = self.proxy
        adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=50, max_retries=5)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        resp = session.post(url, data=sdf, headers={'Content-Type': 'application/json'})
        return resp

    def commit(self):
        """
        Actually send an SDF to CloudSearch for processing

        If an SDF file has been explicitly loaded it will be used. Otherwise,
        documents added through :func:`add` and :func:`delete` will be used.

        :rtype: :class:`CommitResponse`
        :returns: A summary of documents added and deleted
        """
        sdf = self.get_sdf()
        if ': null' in sdf:
            boto.log.error('null value in sdf detected. This will probably raise 500 error.')
            index = sdf.index(': null')
            boto.log.error(sdf[index - 100:index + 100])
        api_version = '2013-01-01'
        if self.domain and self.domain.layer1:
            api_version = self.domain.layer1.APIVersion
        if self.sign_request:
            r = self._commit_with_auth(sdf, api_version)
        else:
            r = self._commit_without_auth(sdf, api_version)
        return CommitResponse(r, self, sdf, signed_request=self.sign_request)


class CommitResponse(object):
    """CommitResponse"""

    def __init__(self, response, doc_service, sdf, signed_request=False):
        self.response = response
        self.doc_service = doc_service
        self.sdf = sdf
        self.signed_request = signed_request
        if self.signed_request:
            self.content = response
        else:
            _body = response.content.decode('utf-8')
            try:
                self.content = json.loads(_body)
            except:
                boto.log.error('Error indexing documents.\nResponse Content:\n{0}\n\nSDF:\n{1}'.format(_body, self.sdf))
                raise boto.exception.BotoServerError(self.response.status_code, '', body=_body)

            self.status = self.content['status']
            if self.status == 'error':
                self.errors = [e.get('message') for e in self.content.get('errors', [])]
                for e in self.errors:
                    if 'Illegal Unicode character' in e:
                        raise EncodingError('Illegal Unicode character in document')
                    elif e == 'The Content-Length is too long':
                        raise ContentTooLongError('Content was too long')
                        continue

            else:
                self.errors = []
        self.adds = self.content['adds']
        self.deletes = self.content['deletes']
        self._check_num_ops('add', self.adds)
        self._check_num_ops('delete', self.deletes)

    def _check_num_ops(self, type_, response_num):
        """Raise exception if number of ops in response doesn't match commit

        :type type_: str
        :param type_: Type of commit operation: 'add' or 'delete'

        :type response_num: int
        :param response_num: Number of adds or deletes in the response.

        :raises: :class:`boto.cloudsearch2.document.CommitMismatchError`
        """
        commit_num = len([d for d in self.doc_service.documents_batch if d['type'] == type_])
        if response_num != commit_num:
            if self.signed_request:
                boto.log.debug(self.response)
            else:
                boto.log.debug(self.response.content)
            exc = CommitMismatchError('Incorrect number of {0}s returned. Commit: {1} Response: {2}'.format(type_, commit_num, response_num))
            exc.errors = self.errors
            raise exc