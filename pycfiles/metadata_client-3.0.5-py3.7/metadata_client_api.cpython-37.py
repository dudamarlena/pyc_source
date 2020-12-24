# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/metadata_client_api.py
# Compiled at: 2018-03-12 10:00:47
# Size of source mod 2**32: 2230 bytes
"""MetadataClientApi class"""
from oauth2_xfel_client.oauth2_client_backend import Oauth2ClientBackend
from apis.repostory_api import RepositoryApi
from apis.experiment_type_api import ExperimentTypeApi
from apis.data_group_repository_api import DataGroupRepositoryApi
from apis.data_group_type_api import DataGroupTypeApi
from apis.parameter_type_api import ParameterTypeApi
from apis.data_type_api import DataTypeApi
from apis.parameter_api import ParameterApi
from apis.instrument_api import InstrumentApi
from apis.proposal_api import ProposalApi
from apis.sample_api import SampleApi
from apis.experiment_api import ExperimentApi
from apis.run_api import RunApi
from apis.data_group_api import DataGroupApi
from apis.data_file_api import DataFileApi
from apis.user_api import UserApi
from common.config import EMAIL_HEADER, DEF_HEADERS

class MetadataClientApi(ExperimentTypeApi, DataGroupTypeApi, RepositoryApi, ParameterTypeApi, DataTypeApi, ParameterApi, InstrumentApi, ProposalApi, SampleApi, ExperimentApi, RunApi, DataGroupApi, DataFileApi, DataGroupRepositoryApi, UserApi):

    def __init__(self, client_id, client_secret, token_url, refresh_url, auth_url, scope, user_email, base_api_url, session_token=None):
        self.oauth_client = Oauth2ClientBackend(client_id=client_id, client_secret=client_secret,
          scope=scope,
          token_url=token_url,
          refresh_url=refresh_url,
          auth_url=auth_url,
          session_token=session_token)
        self.headers = DEF_HEADERS
        self.headers.update({EMAIL_HEADER: user_email})
        self.headers.update(self.oauth_client.headers)
        self.base_api_url = base_api_url