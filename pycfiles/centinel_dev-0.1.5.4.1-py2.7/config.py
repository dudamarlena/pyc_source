# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/config.py
# Compiled at: 2015-10-26 01:10:45
import getpass, json, logging, os, centinel

class Configuration:

    def __init__(self):
        self.params = {}
        version_info = {}
        version_info['version'] = centinel.__version__
        self.params['version'] = version_info
        user_info = {}
        user_info['current_user'] = getpass.getuser()
        user_home = os.path.expanduser('~' + user_info['current_user'])
        user_info['centinel_home'] = os.path.join(user_home, '.centinel')
        user_info['is_vpn'] = False
        self.params['user'] = user_info
        dirs = {}
        dirs['experiments_dir'] = os.path.join(self.params['user']['centinel_home'], 'experiments')
        dirs['data_dir'] = os.path.join(self.params['user']['centinel_home'], 'data')
        dirs['results_dir'] = os.path.join(self.params['user']['centinel_home'], 'results')
        self.params['dirs'] = dirs
        for dir_key in self.params['dirs']:
            directory = self.params['dirs'][dir_key]
            if not os.path.exists(directory):
                os.makedirs(directory)

        results = {}
        results['delete_after_sync'] = True
        results['files_per_archive'] = 10
        results['record_pcaps'] = True
        results['upload_pcaps'] = True
        self.params['results'] = results
        self.params['log'] = {}
        self.params['log']['log_level'] = logging.INFO
        self.params['log']['log_file'] = os.path.join(self.params['user']['centinel_home'], 'centinel.log')
        self.params['log']['log_format'] = '%(asctime)s %(filename)s(line %(lineno)d) %(levelname)s: %(message)s'
        experiments = {}
        experiments['tcpdump_params'] = [
         '-i', 'any']
        self.params['experiments'] = experiments
        servers = {}
        servers['server_url'] = 'https://server.iclab.org:8082'
        servers['login_file'] = os.path.join(self.params['user']['centinel_home'], 'login')
        servers['total_timeout'] = 300
        servers['req_timeout'] = 15
        servers['verify'] = True
        self.params['server'] = servers
        proxy = {}
        proxy['proxy_type'] = None
        proxy['proxy_url'] = None
        proxy['proxy'] = None
        if proxy['proxy_type']:
            proxy['proxy'] = {proxy['proxy_type']: proxy['proxy_url']}
        self.params['proxy'] = proxy
        return

    def parse_config(self, config_file):
        """Given a configuration file, read in and interpret the results"""
        with open(config_file, 'r') as (f):
            config = json.load(f)
        self.params = config
        if self.params['proxy']['proxy_type']:
            self.params['proxy'] = {self.params['proxy']['proxy_type']: self.params['proxy']['proxy_url']}

    def write_out_config(self, config_file):
        """Write out the configuration file

        Note: this will erase all comments from the config file

        """
        with open(config_file, 'w') as (f):
            json.dump(self.params, f, indent=2, separators=(',', ': '))