# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smilectl/api.py
# Compiled at: 2018-09-22 01:53:44
"""API Client for NB Cluster."""
import base64, os, re
from getpass import getpass, getuser
import requests, simplejson as json
from smile import logging
import six
from six.moves import input

def login_prompt(default_user=''):
    """Prompt for user login."""
    username = default_user or input('Username (%s): ' % getuser())
    username = username or getuser()
    password = getpass()
    return (username, password)


class NBAPI(object):
    """API Client for NB Cluster."""
    DEFAULT_API_HOST = 'http://nb.smile.cvpr.science/'

    def __init__(self, username, password, api_host=''):
        """Init function for NBAPI."""
        self._api_host = api_host or self.DEFAULT_API_HOST
        _auth_code = base64.b64encode(six.b('%s:%s' % (username, password)))
        self._auth_header = 'Basic %s' % _auth_code.decode()

    def api_call(self, api_endpoint, data_obj, safe=True):
        """Abstract api_call function for all the api calls."""
        api_path = os.path.join(self._api_host, api_endpoint)
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 
           'Authorization': self._auth_header}
        form_data = ('&').join([ '%s=%s' % (str(k), str(v)) for k, v in six.iteritems(data_obj) ])
        res = requests.post(api_path, data=form_data, headers=headers)
        if res.status_code == 200:
            return json.loads(res.content)
        else:
            if res.status_code == 401:
                logging.error('Login failed.')
            else:
                if res.status_code > 500:
                    logging.error('Server error. %s' % res.content)
                else:
                    logging.error('HTTP %d error.' % res.status_code)
                    logging.debug(res.content)
                if safe:
                    return
            raise IOError('NBAPICallError: %s' % res.content)
            return

    def login(self):
        """Test if the login is successful. Return None if failed."""
        return self.api_call('api/auth', dict())

    def create_job(self, job_obj):
        """Create job on NB cluster. Return None if failed."""
        if any(x not in job_obj for x in ['name', 'cmd']):
            logging.error('Name or cmd missing in job config.')
            return
        else:
            if re.match('^[a-z0-9-]+$', job_obj['name']) is None:
                logging.error("Invalid job name. Job name should contain only lower-case letter, numbers or '-'.")
                return
            post_data = {'name': job_obj['name'], 
               'command': json.dumps(job_obj['cmd'])[1:-1]}
            post_data['gpus'] = job_obj.get('gpus', 1)
            post_data['image'] = job_obj.get('image', 'utasmile/tensorflow:latest-gpu')
            return self.api_call('api/job/create', post_data)