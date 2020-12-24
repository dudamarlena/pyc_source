# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Content sent for Cloud Search indexing was incorrectly encoded.\n\n    This usually happens when a document is marked as unicode but non-unicode\n    characters are present.\n    '


class ContentTooLongError(Exception):
    __doc__ = '\n    Content sent for Cloud Search indexing was too long\n\n    This will usually happen when documents queued for indexing add up to more\n    than the limit allowed per upload batch (5MB)\n\n    '


class DocumentServiceConnection(object):
    __doc__ = '\n    A CloudSearch document service.\n\n    The DocumentServiceConection is used to add, remove and update documents in\n    CloudSearch. Commands are uploaded to CloudSearch in SDF (Search Document\n    Format).\n\n    To generate an appropriate SDF, use :func:`add` to add or update documents,\n    as well as :func:`delete` to remove documents.\n\n    Once the set of documents is ready to be index, use :func:`commit` to send\n    the commands to CloudSearch.\n\n    If there are a lot of documents to index, it may be preferable to split the\n    generation of SDF data and the actual uploading into CloudSearch. Retrieve\n    the current SDF with :func:`get_sdf`. If this file is the uploaded into S3,\n    it can be retrieved back afterwards for upload into CloudSearch using\n    :func:`add_sdf_from_s3`.\n\n    The SDF is not cleared after a :func:`commit`. If you wish to continue\n    using the DocumentServiceConnection for another batch upload of commands,\n    you will need to :func:`clear_sdf` first to stop the previous batch of\n    commands from being uploaded again.\n\n    '

    def __init__(self, domain=None, endpoint=None):
        self.domain = domain
        self.endpoint = endpoint
        if not self.endpoint:
            self.endpoint = domain.doc_service_endpoint
        self.documents_batch = []
        self._sdf = None
        self.proxy = {}
        self.sign_request = False
        if self.domain:
            if self.domain.layer1:
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
        if self.domain:
            if self.domain.layer1:
                api_version = self.domain.layer1.APIVersion
        if self.sign_request:
            r = self._commit_with_auth(sdf, api_version)
        else:
            r = self._commit_without_auth(sdf, api_version)
        return CommitResponse(r, self, sdf, signed_request=self.sign_request)


class CommitResponse(object):
    __doc__ = 'Wrapper for response to Cloudsearch document batch commit.\n\n    :type response: :class:`requests.models.Response`\n    :param response: Response from Cloudsearch /documents/batch API\n\n    :type doc_service: :class:`boto.cloudsearch2.document.DocumentServiceConnection`\n    :param doc_service: Object containing the documents posted and methods to\n        retry\n\n    :raises: :class:`boto.exception.BotoServerError`\n    :raises: :class:`boto.cloudsearch2.document.SearchServiceException`\n    :raises: :class:`boto.cloudsearch2.document.EncodingError`\n    :raises: :class:`boto.cloudsearch2.document.ContentTooLongError`\n    '

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