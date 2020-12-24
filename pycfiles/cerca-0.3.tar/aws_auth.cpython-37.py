# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cerberus/aws_auth.py
# Compiled at: 2019-10-31 01:58:57
# Size of source mod 2**32: 2946 bytes
__doc__ = '\nCopyright 2016-present Nike, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nYou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n      http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and* limitations under the License.*\n'
from __future__ import print_function
from botocore import session, awsrequest, auth
import logging, sys
from . import CerberusClientException, CLIENT_VERSION
from .util import throw_if_bad_response, post_with_retry
from collections import OrderedDict
logger = logging.getLogger(__name__)

class AWSAuth(object):
    """AWSAuth"""
    HEADERS = {'Content-Type':'application/json', 
     'X-Cerberus-Client':'CerberusPythonClient/' + CLIENT_VERSION}

    def __init__(self, cerberus_url, region, aws_session=None, verbose=None):
        self.cerberus_url = cerberus_url
        self.region = region
        self.aws_session = aws_session
        self.verbose = verbose

    def _get_v4_signed_headers(self):
        """Returns V4 signed get-caller-identity request headers"""
        if self.aws_session is None:
            boto_session = session.Session()
            creds = boto_session.get_credentials()
        else:
            creds = self.aws_session.get_credentials()
        if creds is None:
            raise CerberusClientException('Unable to locate AWS credentials')
        readonly_credentials = creds.get_frozen_credentials()
        data = OrderedDict((('Action', 'GetCallerIdentity'), ('Version', '2011-06-15')))
        url = 'https://sts.{}.amazonaws.com/'.format(self.region)
        request_object = awsrequest.AWSRequest(method='POST', url=url, data=data)
        signer = auth.SigV4Auth(readonly_credentials, 'sts', self.region)
        signer.add_auth(request_object)
        return request_object.headers

    def get_token(self):
        """Returns a client token from Cerberus"""
        signed_headers = self._get_v4_signed_headers()
        for header in self.HEADERS:
            signed_headers[header] = self.HEADERS[header]

        resp = post_with_retry((self.cerberus_url + '/v2/auth/sts-identity'), headers=signed_headers)
        throw_if_bad_response(resp)
        token = resp.json()['client_token']
        iam_principal_arn = resp.json()['metadata']['aws_iam_principal_arn']
        if self.verbose:
            print(('Successfully authenticated with Cerberus as {}'.format(iam_principal_arn)), file=(sys.stderr))
        logger.info('Successfully authenticated with Cerberus as {}'.format(iam_principal_arn))
        return token