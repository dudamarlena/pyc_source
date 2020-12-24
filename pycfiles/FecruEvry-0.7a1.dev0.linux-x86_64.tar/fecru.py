# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/e210990/bin/python26/lib/python2.6/site-packages/fecru.py
# Compiled at: 2014-06-25 09:42:53
import json, requests, httplib

class FecruServer(object):
    """Fecru server authentication object."""

    def __init__(self, fecru_url, app_name, app_pass):
        self.fecru_url = fecru_url
        self.app_name = app_name
        self.app_pass = app_pass
        self.rest_url = fecru_url.rstrip('/') + '/rest-service/auth-v1/login'
        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPBasicAuth(app_name, app_pass)
        self.session.headers.update({'Content-type': 'application/json', 
           'Accept': 'application/json'})

    def __str__(self):
        return 'Crowd Server at %s' % self.crowd_url

    def __repr__(self):
        return "<CrowdServer('%s', '%s', %s')>" % (
         self.crowd_url, self.app_name, self.app_pass)

    def _get(self, *args, **kwargs):
        """Wrapper around Requests for GET requests

        Returns:
            Response:
                A Requests Response object
        """
        req = self.session.get(*args, **kwargs)
        return req

    def _post(self, *args, **kwargs):
        """Wrapper around Requests for POST requests

        Returns:
            Response:
                A Requests Response object
        """
        req = self.session.post(*args, **kwargs)
        return req

    def _delete(self, *args, **kwargs):
        """Wrapper around Requests for DELETE requests

        Returns:
            Response:
                A Requests Response object
        """
        req = self.session.delete(*args, **kwargs)
        return req

    def auth_ping(self):
        """Test that application can authenticate to Fecru.

        Attempts to authenticate the application user against
        the Fecru server. In order for user authentication to
        work, an application must be able to authenticate.

        Returns:
            bool:
                True if the application authentication succeeded.
        """
        url = self.rest_url + '/non-existent/location'
        response = self._get(url)
        if response.status_code == 401:
            return False
        else:
            if response.status_code == 404:
                return True
            return False

    def get_server_info(self):
        """Return server info.

        Args:
            None

        Returns:
            dict:
                Server information data
                

            None: If failure.
        """
        response = self._get(self.fecru_url + '/rest-service-fecru/server-v1')
        if not response.ok:
            return None
        else:
            return response.content

    def create_repository(self, repo_name, descr, scmurl, scmpath, enabled='false'):
        """Add a new repository

        Args:
            group: Repository name

        Returns:
 
            None: If failed.
        """
        rtnStr = 'Success'
        params = {'type': 'SUBVERSION', 
           'name': repo_name, 
           'description': descr, 
           'url': scmurl, 
           'path': scmpath, 
           'username': 'continuum', 
           'password': 'ECOoSTFTjxm67w2Uw6nSmOMxvwuj3jh81fE4FwbvLucw91SmvG8UG6j6mNh5Or5'}
        response = self._post(self.fecru_url + '/rest-service-fecru/admin/repositories-v1', data=json.dumps(params))
        if not response.ok:
            rtnStr = 'Error : ' + str(response.status_code)
        else:
            rtnStr = rtnStr + ' : ' + str(response.status_code)
        return rtnStr

    def check_repository_exists(self, name):
        """List all repositories

        Args:
            limit: page limit

        Returns:
 
            None: If failed.
        """
        params = {'name': name}
        print params
        response = self._get(self.fecru_url + '/rest-service-fecru/admin/repositories-v1', data=json.dumps(params))
        print dir(response)
        print response.status_code
        print response.text
        if not response.ok:
            return False
        return response.text