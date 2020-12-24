# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/abenkevich/defender/alertlogic-cli/alertlogic/auth.py
# Compiled at: 2019-03-14 08:35:10
__doc__ = '\n    alertlogic.auth\n    ~~~~~~~~~~~~~~\n    alertlogic authentication/authorization\n'
import requests, pyotp

class AuthenticationException(Exception):

    def __init__(self, message):
        super(AuthenticationException, self).__init__(('authentication error: {}').format(message))


class Session:
    """
    Authenticates against alertlogic aims service and stores session information (token and account id),
    additionally objects of this class can be used as auth modules for the requests lib, more info:
    http://docs.python-requests.org/en/master/user/authentication/#new-forms-of-authentication
    """

    def __init__(self, region, username, password, mfa_secret=None):
        """
        :param region: a Region object
        :param username: your alertlogic cloudinsight username
        :param password: your alertlogic cloudinsight password
        """
        self.region = region
        self._authenticate(username, password, mfa_secret)

    def _authenticate(self, username, password, mfa_secret=None):
        """
        Authenticates against alertlogic Access and Identity Management Service (AIMS)
        more info:
        https://console.cloudinsight.alertlogic.com/api/aims/#api-AIMS_Authentication_and_Authorization_Resources-Authenticate
        """
        try:
            auth = requests.auth.HTTPBasicAuth(username, password)
            if mfa_secret:
                totp = pyotp.TOTP(mfa_secret)
                mfa_code = totp.now()
                body = {'mfa_code': mfa_code}
                response = requests.post(self.region.get_api_endpoint() + '/aims/v1/authenticate', json=body, auth=auth)
            else:
                response = requests.post(self.region.get_api_endpoint() + '/aims/v1/authenticate', auth=auth)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise AuthenticationException(('invalid http response {}').format(e.message))

        try:
            self._token = response.json()['authentication']['token']
        except (KeyError, TypeError, ValueError):
            raise AuthenticationException('token not found in response')

        try:
            self.account_id = response.json()['authentication']['account']['id']
        except (KeyError, TypeError, ValueError):
            raise AuthenticationException('account id not found in response')

    def __call__(self, r):
        """
        requests lib auth module callback
        """
        r.headers['x-aims-auth-token'] = self._token
        return r