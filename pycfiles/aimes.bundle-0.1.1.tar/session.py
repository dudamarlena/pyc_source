# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grad03/fengl/AIMES_project/aimes.bundle/src/aimes/bundle/session.py
# Compiled at: 2015-09-21 12:06:44
import os, glob, logging
from aimes.bundle import BundleException
from aimes.bundle.db import DBException
from aimes.bundle.db import Session as dbSession
from aimes.bundle.bundle_manager import BundleManager
from aimes.bundle.agent import BundleAgent
import radical.utils as ru

class Session(ru.Daemon):
    """Session class
    """

    def __init__(self, database_url=None, database_name='aimes_bundle', uid=None):
        self._database_url = database_url
        self._database_name = database_name
        self._uid = uid
        self._resource_list = {}
        self._dbs = None
        self._dbs_metadata = None
        self._dbs_connection_info = None
        self._agent_list = None
        if not self._database_url:
            self._database_url = os.getenv('AIMES_BUNDLE_DBURL', None)
        if not self._database_url:
            raise BundleException('no database URL (set AIMES_BUNDLE_DBURL)')
        if uid is None:
            print 'Initializing AIMES.Bundle session:'
            print 'Step (1 of 4): setup database session               ...',
            try:
                self._uid = ru.generate_id('aimes_bundle.session', mode=ru.ID_PRIVATE)
                self._dbs, self._dbs_metadata, self._dbs_connection_info = dbSession.new(sid=self._uid, db_url=self._database_url, db_name=database_name)
            except Exception as e:
                print 'Failed'
                raise BundleException(str(e))

            print 'Success'
            print 'Step (2 of 4): process resource configuration files ...',
            config_file = os.getenv('AIMES_BUNDLE_CONFIG', None)
            if not config_file:
                module_path = os.path.dirname(os.path.abspath(__file__))
                default_cfgs = ('{}/configs/*.conf').format(module_path)
                config_files = glob.glob(default_cfgs)
            else:
                config_files = [
                 config_file]
            for config_file in config_files:
                try:
                    rcs = self.load_resource_config_file(config_file=config_file)
                except Exception as e:
                    print ('skip config file {}: {}').format(str(config_file), str(e))
                    continue

                for rc in rcs:
                    self._resource_list[rc] = rcs[rc]

            if len(self._resource_list) == 0:
                print 'Failed'
                raise BundleException('No resource config file detected')
            self._dbs.add_resource_list(resource_list=self._resource_list)
            print 'Success'
            print 'Step (3 of 4): start bundle agents                  ...'
            for rc in self._resource_list:
                print ('adding {}').format(rc)
                self.add_agent(self._resource_list[rc])
                print ('{} added').format(rc)

            print 'Step (3 of 4): start bundle agents                  ...',
            print 'Success'
            print 'Step (4 of 4): enter service mode                   ...',
            print 'Success'
        else:
            return
        return

    def __del__(self):
        self.close()

    def close(self, cleanup=True, terminate=True, delete=None):
        pass

    @property
    def service_name(self):
        return ('{}/{}.{}').format(self._database_url, self._databasename, self._uid)

    def load_resource_config_file(self, config_file):
        """Load all resource logins from one config file to a dict.
        """
        _cred = {}
        _valid_p = [
         'cluster_type', 'login_server', 'username',
         'password', 'key_file']
        _mandatory_p = ['cluster_type', 'login_server', 'username']
        _file = open(config_file, 'r')
        for _l in _file:
            _l = _l.strip()
            if _l and not _l.startswith('#'):
                _c = {}
                for _p in _l.split():
                    _k, _v = _p.split('=')
                    _k = _k.strip()
                    if _k not in _valid_p:
                        logging.error(("Invalid key '{}': skip '{}'").format(_k, _l))
                        continue
                    _c[_k.strip()] = _v.strip()

                _missing_key = False
                for _k in _mandatory_p:
                    if _k not in _c:
                        logging.error(("Missing mandatory key '{}': {}").format(_k, _l))
                        _missing_key = True
                        break

                if not _missing_key:
                    if not BundleAgentController.support_resource_type(_c['cluster_type']):
                        logging.error(("Unsupported resource type '{}': {}").format(_c['cluster_type'], _l))
                        continue
                    _cred[_c['login_server']] = _c
                else:
                    logging.error(("Skip '{}'").format(_l))

        return _cred

    def add_resource(self, rc):
        """Add a new resource to the current session
        """
        pass

    def add_agent(self, rc):
        """Create a new BundleAgent instance
        """
        if rc['login_server'] in self._agent_list:
            print ('BundleAgent for {} already exists, try remove first').format(rc['login_server'])
        try:
            self._agent_list[rc['login_server']] = BundleAgent.create(resource_config=rc, dbSession=self._dbs)
        except Exception as e:
            print ('Failed to creat new BundleAgent for {}:\n{}\n{}').format(rc['login_server'], str(e.__class__), str(e))

    def remove_agent(self, rc):
        """Stop/Delete BundleAgent instance
        """
        if rc['login_server'] not in self._agent_name_list:
            print ("BundleAgent {} doesn't exists").format(rc['login_server'])

    def start_daemon(self):
        """start daemon process which will execute self.run()
        """
        self.config_file = config_file
        self.idle_timeout = 60
        self.mongodb_url = mongodb_url
        retval = self.start(debug=False)
        print 'daemonized'
        return retval

    def run(self):
        """
        """
        try:
            while True:
                coll_config = db['config']
                coll_workload = db['workload']
                coll_bandwidth = db['bandwidth']
                ret = self.get_data()
                for cluster_ip in ret['cluster_list']:
                    cluster_id = ip2id(cluster_ip)
                    config = ret['cluster_config'][cluster_id]
                    workload = ret['cluster_workload'][cluster_id]
                    bandwidth = ret['cluster_bandwidth'][cluster_id]
                    timestamp = time.time()
                    if config:
                        config['timestamp'] = timestamp
                    if workload:
                        workload['timestamp'] = timestamp
                    if bandwidth:
                        bandwidth['timestamp'] = timestamp
                    if config:
                        config['_id'] = cluster_id
                    if workload:
                        workload['_id'] = cluster_id
                    if bandwidth:
                        bandwidth['_id'] = cluster_id
                    if config:
                        coll_config.update({'_id': cluster_id}, config, upsert=True)
                    if workload:
                        coll_workload.update({'_id': cluster_id}, workload, upsert=True)
                    if bandwidth:
                        coll_bandwidth.update({'_id': cluster_id}, bandwidth, upsert=True)

                time.sleep(self.idle_timeout)

        except Exception as e:
            raise