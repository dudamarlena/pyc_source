# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/calibration_client_api.py
# Compiled at: 2018-03-12 13:22:50
# Size of source mod 2**32: 1907 bytes
__doc__ = 'CalibrationClientApi class'
from oauth2_xfel_client.oauth2_client_backend import Oauth2ClientBackend
from .apis.calibration_api import CalibrationApi
from .apis.calibration_constant_api import CalibrationConstantApi
from .apis.calibration_constant_version_api import CalibrationConstantVersionApi
from .apis.condition_api import ConditionApi
from .apis.device_type_api import DeviceTypeApi
from .apis.parameter_api import ParameterApi
from .apis.physical_device_api import PhysicalDeviceApi
from .apis.user_api import UserApi
from .common.config import EMAIL_HEADER, DEF_HEADERS

class CalibrationClientApi(CalibrationApi, CalibrationConstantApi, CalibrationConstantVersionApi, ConditionApi, ParameterApi, DeviceTypeApi, PhysicalDeviceApi, UserApi):

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