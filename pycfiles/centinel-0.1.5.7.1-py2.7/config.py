# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/config.py
# Compiled at: 2016-09-16 12:23:42
import getpass, json, logging, os, centinel

class Configuration:

    def __init__(self):
        self.params = {}
        version_info = {'version': centinel.__version__}
        self.params['version'] = version_info
        user_info = {'current_user': getpass.getuser()}
        user_home = os.path.expanduser('~' + user_info['current_user'])
        user_info['centinel_home'] = os.path.join(user_home, '.centinel')
        user_info['is_vpn'] = False
        self.params['user'] = user_info
        dirs = {'experiments_dir': os.path.join(self.params['user']['centinel_home'], 'experiments'), 
           'data_dir': os.path.join(self.params['user']['centinel_home'], 'data'), 
           'results_dir': os.path.join(self.params['user']['centinel_home'], 'results')}
        self.params['dirs'] = dirs
        for dir_key in self.params['dirs']:
            directory = self.params['dirs'][dir_key]
            if not os.path.exists(directory):
                os.makedirs(directory)

        results = {'delete_after_sync': True, 'files_per_archive': 10, 
           'record_pcaps': True, 
           'upload_pcaps': True}
        self.params['results'] = results
        self.params['log'] = {}
        self.params['log']['log_level'] = logging.INFO
        self.params['log']['log_file'] = os.path.join(self.params['user']['centinel_home'], 'centinel.log')
        self.params['log']['log_format'] = '%(asctime)s %(filename)s(line %(lineno)d) %(levelname)s: %(message)s'
        experiments = {'tcpdump_params': ['-i', 'any']}
        self.params['experiments'] = experiments
        servers = {'server_url': 'https://server.iclab.cs.stonybrook.edu:8082', 'login_file': os.path.join(self.params['user']['centinel_home'], 'login'), 
           'total_timeout': 1800, 
           'req_timeout': 15, 
           'verify': True}
        self.params['server'] = servers
        proxy = {'proxy_type': None, 'proxy_url': None, 
           'proxy': None}
        if proxy['proxy_type']:
            proxy['proxy'] = {proxy['proxy_type']: proxy['proxy_url']}
        self.params['proxy'] = proxy
        return

    def parse_config(self, config_file):
        """
        Given a configuration file, read in and interpret the results

        :param config_file:
        :return:
        """
        with open(config_file, 'r') as (f):
            config = json.load(f)
        self.params = config
        if self.params['proxy']['proxy_type']:
            self.params['proxy'] = {self.params['proxy']['proxy_type']: self.params['proxy']['proxy_url']}

    def update(self, old, backup_path=None):
        """
        Update the old configuration file with new values.

        :param old: old configuration to update.
        :param backup_path: path to write a backup of the old config file.

        :return:
        """
        for category in old.params.keys():
            for parameter in old.params[category].keys():
                if category in self.params and parameter in self.params[category] and old.params[category][parameter] != self.params[category][parameter] and category != 'version':
                    print "Config value '%s.%s' in old configuration is different from the new version\n[old value] = %s\n[new value] = %s" % (
                     category, parameter,
                     old.params[category][parameter],
                     self.params[category][parameter])
                    answer = raw_input('Do you want to overwrite? ([y]/n) ')
                    while answer.lower() not in ('y', 'yes', 'n', 'no'):
                        answer = raw_input("Answer not recongnized. Enter 'y' or 'n'. ")

                    if answer in ('n', 'no'):
                        old_value = old.params[category][parameter]
                        self.params[category][parameter] = old_value
                elif not (category in self.params and parameter in self.params[category]):
                    print "Deprecated config option '%s.%s' has been removed." % (
                     category, parameter)

        if backup_path is not None:
            old.write_out_config(backup_path)
            print 'Backup saved in %s.' % backup_path
        return

    def write_out_config(self, config_file):
        """
        Write out the configuration file

        :param config_file:
        :return:

        Note: this will erase all comments from the config file

        """
        with open(config_file, 'w') as (f):
            json.dump(self.params, f, indent=2, separators=(',', ': '))