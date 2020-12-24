# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/grad03/fengl/AIMES_project/aimes.bundle/src/aimes/bundle/resource_bundle.py
# Compiled at: 2015-09-07 11:52:03
__doc__ = 'Resource & Resource Bundle\n\nResource:\n    This module defines different types of resources such as the compute\n    resource and the network resource. Conceptually, a resource object is\n    the most fine-grained entity which can be independently characterized.\n\n    On an HPC cluster for example, a user submit his/her job to a particular\n    queue. The queue could be viewed as the end-point of compute resource,\n    despite that it contains multiple compute nodes. Since usually nodes\n    within a queue are homogeneous in terms of core-count, processor type,\n    and memory size, we can characterize a queue with the configuration of\n    any of its compute nodes and the total number of nodes.\n\n    On a Grid such as OSG, a job is launched to a single node. Each node\n    could be seen as an independent compute resource unit.\n\n    Resource has, by and large, two types of info, namely static and\n    dynamic. Typical static info are configurations, which ideally should\n    not constant change. Dynamic info include workload. The creator of these\n    resource class are in charge of guarantee the number and statistics of\n    each resource are up-to-date. However, this could be done in a "Lazy"\n    way - only update data once being accessed.\n\nResource Bundle:\n\nFurthermore, in OSG, a user is given quite a\nfew options to specify a group of nodes all satisfying certain conditions to\nallocate from. We can view such groups of nodes as a compute resource\nbundle.\n'
import os
from UserDict import UserDict
import radical.utils as ru, saga
DEFAULT_MONGODB_URL = 'mongodb://54.221.194.147:24242/AIMES_bundle_fengl/'
DEFAULT_OSG_CONFIG_MONGODB_URL = 'mongodb://54.221.194.147:24242/AIMES_bundle_osg_config/'

class HpcQueue(UserDict):
    """This class represents a batch queue of HPC clusters.

    This class is a dict like wrapper class which encapsulates per-queue
    information.
    """

    def __init__(self, qname, cname):
        UserDict.__init__(self)
        self['name'] = qname
        self['cluster'] = cname
        self['uid'] = ('{}.{}').format(qname, cname)
        self['last_update_timestamp'] = 0


class HpcCluster(UserDict):
    """This class represents a batch queue based HPC cluster.

    This class is a dict like wrapper class which encapsulates cluster-wide
    information.
    """

    def __init__(self, name, db_session):
        UserDict.__init__(self)
        self['name'] = name
        self._db_session = db_session
        self['uid'] = ('{}').format(name)
        self['queues'] = {}
        self['num_nodes'] = 0
        self['num_cores'] = 0
        self._query_db()

    def update_status(self):
        """Query db to set all data to up-to-date values
        """
        self._query_db()

    def _query_db(self):
        """Do the actual work
        """
        timestamp, config, workload = self._db_session.get_hpc_cluster_info(self['name'])


class OsgSite(object):

    def __init__(self, name):
        self['name'] = name


class NetworkConnection(object):

    def __init__(self, name):
        self['name'] = name


class OSGResource(object):

    def __init__(self, name, config, workload=None, bandwidths=None):
        self.name = name
        self.num_nodes = config.aggregate([{'$match': {'site': name}}, {'$group': {'_id': '$hostname', 'count': {'$sum': 1}}}])['result'][0]['count']
        self.queues = dict()
        for _group in config.aggregate([{'$match': {'site': name}}, {'$group': {'_id': {'num_cores': '$num_cores', 'mips': '$mips', 'mem_size': '$mem_size'}, 'node_list': {'$addToSet': '$_id'}}}])['result']:
            _config = _group['_id']
            queue_name = ('num_cores_{}-mips_{}-mem_size_{}').format(_config['num_cores'], _config['mips'], _config['mem_size'])
            self.queues[queue_name] = OSGQueue(self.name, queue_name, _group['node_list'])

    def get_bandwidth(self, tgt, mode):
        return 0.0


class Resource(object):

    def __init__(self, name, config, workload, bandwidths):
        self.name = name
        self.num_nodes = config['num_nodes']
        self.bandwidths = bandwidths
        self.queues = dict()
        for queue_name in config['queue_info']:
            self.queues[queue_name] = Queue(self.name, queue_name, config['queue_info'][queue_name], workload[queue_name])

    def get_bandwidth(self, tgt, mode):
        if tgt in self.bandwidths:
            return self.bandwidths[tgt][mode]
        return 0.0

    def get_bandwidth_now(self, tgt='localhost', mode='out'):
        REMOTE_HOST = tgt
        REMOTE_DIR = 'tmp'
        REMOTE_FILE_ENDPOINT = 'sftp://' + REMOTE_HOST + '/' + REMOTE_DIR
        dirname = '%s/iperf/' % REMOTE_FILE_ENDPOINT
        REMOTE_JOB_ENDPOINT = 'ssh://' + REMOTE_HOST
        if mode is 'out':
            ctx = saga.Context('ssh')
            ctx.user_id = 'fengl'
            session = saga.Session()
            session.add_context(ctx)
            workdir = saga.filesystem.Directory(dirname, saga.filesystem.CREATE_PARENTS, session=session)
            mbwrapper = saga.filesystem.File('file://localhost/%s/impl/iperf-client.sh' % os.getcwd())
            mbwrapper.copy(workdir.get_url())
            mbexe = saga.filesystem.File('file://localhost/%s/third_party/iperf-3.0.11-source.tar.gz' % os.getcwd())
            mbexe.copy(workdir.get_url())
            js = saga.job.Service(REMOTE_JOB_ENDPOINT, session=session)
            jd = saga.job.Description()
            jd.environment = {'MYOUTPUT': 'result.dat'}
            jd.working_directory = workdir.get_url().path
            jd.executable = './iperf-client.sh'
            iperf_local_port = 55201
            jd.arguments = ['login1.stampede.tacc.utexas.edu', iperf_local_port, '$MYOUTPUT']
            jd.output = 'mysagajob.stdout'
            jd.error = 'mysagajob.stderr'
            myjob = js.create_job(jd)
            myjob.run()
            myjob.wait()
            outfilesource = ('{}/result.dat').format(dirname)
            outfiletarget = ('file://localhost/{}/').format(os.getcwd())
            out = saga.filesystem.File(outfilesource, session=session)
            out.copy(outfiletarget)
            f1 = open('result.dat')
            timestamp1 = int(f1.readline().strip())
            for line in f1.readlines():
                if line.find('sender') != -1:
                    line_tokens = line.split()
                    out_bandwidth = float(line_tokens[(line_tokens.index('Mbits/sec') - 1)])
                elif line.find('receiver') != -1:
                    line_tokens = line.split()
                    in_bandwidth = float(line_tokens[(line_tokens.index('Mbits/sec') - 1)])

            mongo, db, dbname, cname, pname = ru.mongodb_connect(self.mongodb_url)
            coll_bandwidth_new = db['bandwidth_new']
            coll_bandwidth.update({'_id': cluster_id}, bandwidth, upsert=True)


def parse_iperf_result(output_file):
    f = open(output_file)


class OSGQueue(object):
    """
    This class represents a set of information on a batch queue of a
    specific resource.
    """

    def __init__(self, resource_name, name, node_list, workload=None):
        self.name = name
        self.resource_name = resource_name
        self.num_nodes = len(node_list)
        self.hostname_list = node_list

    def as_dict(self):
        object_dict = {'name': self.name, 
           'resource_name': self.resource_name, 
           'num_nodes': self.num_nodes, 
           'hostname_list': self.hostname_list}
        return object_dict

    def __str__(self):
        return str(self.as_dict())


class Queue(object):
    """This class represents a set of information on a batch queue of a
    specific resource.
    """

    def __init__(self, resource_name, name, config, workload):
        self.name = name
        self.resource_name = resource_name
        self.max_walltime = config['max_walltime']
        self.num_procs_limit = config['num_procs_limit']
        self.alive_nodes = workload['alive_nodes']
        self.alive_procs = workload['alive_procs']
        self.busy_nodes = workload['busy_nodes']
        self.busy_procs = workload['busy_procs']
        self.free_nodes = workload['free_nodes']
        self.free_procs = workload['free_procs']
        self.num_queueing_jobs = workload['num_queueing_jobs']
        self.num_running_jobs = workload['num_running_jobs']

    def as_dict(self):
        object_dict = {'name': self.name, 
           'resource_name': self.resource_name, 
           'max_walltime': self.max_walltime, 
           'num_procs_limit': self.num_procs_limit, 
           'alive_nodes': self.alive_nodes, 
           'alive_procs': self.alive_procs, 
           'busy_nodes': self.busy_nodes, 
           'busy_procs': self.busy_procs, 
           'free_nodes': self.free_nodes, 
           'free_procs': self.free_procs, 
           'num_queueing_jobs': self.num_queueing_jobs, 
           'num_running_jobs': self.num_running_jobs}
        return object_dict

    def __str__(self):
        return str(self.as_dict())


class ResourceBundle(object):

    def __init__(self, mongodb_url=DEFAULT_MONGODB_URL):
        self.mongodb_url = DEFAULT_MONGODB_URL
        self.query_db()

    @staticmethod
    def create(bundle_description, bundle_manager_id):
        bundle = ResourceBundle()
        return bundle

    def query_db(self):
        mongo, db, dbname, cname, pname = ru.mongodb_connect(self.mongodb_url)
        self._priv = dict()
        self._priv['cluster_list'] = list()
        self._priv['cluster_config'] = dict()
        self._priv['cluster_workload'] = dict()
        self._priv['cluster_bandwidth'] = dict()
        for doc in list(db['config'].find()):
            self._priv['cluster_list'].append(doc['_id'])
            self._priv['cluster_config'][doc['_id']] = doc

        for doc in list(db['workload'].find()):
            self._priv['cluster_workload'][doc['_id']] = doc

        for doc in list(db['bandwidth'].find()):
            self._priv['cluster_bandwidth'][doc['_id']] = doc

        self.resources = dict()
        for resource_name in self._priv['cluster_list']:
            config = self._priv['cluster_config'].get(resource_name, dict())
            workload = self._priv['cluster_workload'].get(resource_name, dict())
            bandwidths = self._priv['cluster_bandwidth'].get(resource_name, dict())
            self.resources[resource_name] = Resource(resource_name, config, workload, bandwidths)

        self.queues = list()
        for resource in self.resources:
            self.queues += self.resources[resource].queues.values()

        self.load_osg_resource()

    def load_osg_resource(self, db_url=DEFAULT_OSG_CONFIG_MONGODB_URL):
        mongo, db, dbname, cname, pname = ru.mongodb_connect(db_url)
        self.osg_site_list = []
        for doc in db['config'].aggregate({'$group': {'_id': '$site'}})['result']:
            self._priv['cluster_list'].append(doc['_id'])
            self.osg_site_list.append(doc['_id'])
            self.resources[doc['_id']] = OSGResource(doc['_id'], db.config)

    def list_resources(self):
        for resource in self.resources:
            print resource