# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/provisioners/gceProvisioner.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 22122 bytes
from builtins import range
import os, time, threading, json, requests, uuid, logging
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.drivers.gce import GCEFailedNode
from toil.provisioners.abstractProvisioner import AbstractProvisioner, Shape
from toil.provisioners import NoSuchClusterException
from toil.jobStores.googleJobStore import GoogleJobStore
from toil.provisioners.node import Node
logger = logging.getLogger(__name__)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

class GCEProvisioner(AbstractProvisioner):
    __doc__ = '\n    Implements a Google Compute Engine Provisioner using libcloud.\n    '
    NODE_BOTO_PATH = '/root/.boto'
    SOURCE_IMAGE = b'projects/coreos-cloud/global/images/family/coreos-stable'

    def __init__(self, clusterName, zone, nodeStorage, sseKey):
        super(GCEProvisioner, self).__init__(clusterName, zone, nodeStorage)
        self.cloud = 'gce'
        self._sseKey = sseKey
        if clusterName:
            self._readCredentials()
        else:
            self._readClusterSettings()

    def _readClusterSettings(self):
        """
        Read the cluster settings from the instance, which should be the leader.
        See https://cloud.google.com/compute/docs/storing-retrieving-metadata for details about
        reading the metadata.
        """
        metadata_server = 'http://metadata/computeMetadata/v1/instance/'
        metadata_flavor = {'Metadata-Flavor': 'Google'}
        zone = requests.get((metadata_server + 'zone'), headers=metadata_flavor).text
        self._zone = zone.split('/')[(-1)]
        project_metadata_server = 'http://metadata/computeMetadata/v1/project/'
        self._projectId = requests.get((project_metadata_server + 'project-id'), headers=metadata_flavor).text
        self._googleJson = ''
        self._clientEmail = ''
        self._tags = requests.get((metadata_server + 'description'), headers=metadata_flavor).text
        tags = json.loads(self._tags)
        self.clusterName = tags['clusterName']
        self._gceDriver = self._getDriver()
        self._instanceGroup = self._gceDriver.ex_get_instancegroup((self.clusterName), zone=(self._zone))
        leader = self.getLeader()
        self._leaderPrivateIP = leader.privateIP
        self._masterPublicKey = self._setSSH()
        self._credentialsPath = GoogleJobStore.nodeServiceAccountJson
        self._keyName = 'core'
        self._botoPath = self.NODE_BOTO_PATH

    def _readCredentials(self):
        """
        Get the credentials from the file specified by GOOGLE_APPLICATION_CREDENTIALS.
        """
        self._googleJson = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not self._googleJson:
            raise RuntimeError('GOOGLE_APPLICATION_CREDENTIALS not set.')
        try:
            with open(self._googleJson) as (jsonFile):
                self.googleConnectionParams = json.loads(jsonFile.read())
        except:
            raise RuntimeError('GCEProvisioner: Could not parse the Google service account json file %s' % self._googleJson)

        self._projectId = self.googleConnectionParams['project_id']
        self._clientEmail = self.googleConnectionParams['client_email']
        self._credentialsPath = self._googleJson
        self._masterPublicKey = None
        self._gceDriver = self._getDriver()

    def launchCluster(self, leaderNodeType, leaderStorage, owner, **kwargs):
        """
        In addition to the parameters inherited from the abstractProvisioner,
        the Google launchCluster takes the following parameters:
        keyName: The key used to communicate with instances
        botoPath: Boto credentials for reading an AWS jobStore (optional).
        vpcSubnet: A subnet (optional).
        """
        if 'keyName' not in kwargs:
            raise RuntimeError('A keyPairName is required for the GCE provisioner.')
        else:
            self._keyName = kwargs['keyName']
            if 'botoPath' in kwargs:
                self._botoPath = kwargs['botoPath']
            self._vpcSubnet = kwargs['vpcSubnet'] if 'vpcSubnet' in kwargs else None
            self._instanceGroup = self._gceDriver.ex_create_instancegroup(self.clusterName, self._zone)
            logger.debug('Launching leader')
            tags = {'Owner':self._keyName, 
             'clusterName':self.clusterName}
            if 'userTags' in kwargs:
                tags.update(kwargs['userTags'])
            self._tags = json.dumps(tags)
            userData = self._getCloudConfigUserData('leader')
            metadata = {'items': [{'key':'user-data',  'value':userData}]}
            imageType = 'coreos-stable'
            sa_scopes = [{'scopes': ['compute', 'storage-full']}]
            disk = {}
            disk['initializeParams'] = {'sourceImage':self.SOURCE_IMAGE, 
             'diskSizeGb':leaderStorage}
            disk.update({'boot':True,  'autoDelete':True})
            name = 'l' + str(uuid.uuid4())
            leader = self._gceDriver.create_node(name, leaderNodeType, imageType, location=(self._zone),
              ex_service_accounts=sa_scopes,
              ex_metadata=metadata,
              ex_subnetwork=(self._vpcSubnet),
              ex_disks_gce_struct=[
             disk],
              description=(self._tags),
              ex_preemptible=False)
            self._instanceGroup.add_instances([leader])
            self._leaderPrivateIP = leader.private_ips[0]
            leaderNode = Node(publicIP=(leader.public_ips[0]), privateIP=(leader.private_ips[0]), name=(leader.name),
              launchTime=(leader.created_at),
              nodeType=(leader.size),
              preemptable=False,
              tags=(self._tags))
            leaderNode.waitForNode('toil_leader', keyName=(self._keyName))
            leaderNode.copySshKeys(self._keyName)
            leaderNode.injectFile(self._credentialsPath, GoogleJobStore.nodeServiceAccountJson, 'toil_leader')
            if self._botoPath:
                leaderNode.injectFile(self._botoPath, self.NODE_BOTO_PATH, 'toil_leader')
        logger.debug('Launched leader')

    def getNodeShape(self, nodeType, preemptable=False):
        sizes = self._gceDriver.list_sizes(location=(self._zone))
        sizes = [x for x in sizes if x.name == nodeType]
        assert len(sizes) == 1
        instanceType = sizes[0]
        disk = 0
        if disk == 0:
            disk = self._nodeStorage * 1073741824
        memory = (instanceType.ram / 1000 - 0.1) * 1073741824
        return Shape(wallTime=3600, memory=memory,
          cores=(instanceType.extra['guestCpus']),
          disk=disk,
          preemptable=preemptable)

    @staticmethod
    def retryPredicate(e):
        """ Not used by GCE """
        return False

    def destroyCluster(self):
        """
        Try a few times to terminate all of the instances in the group.
        """
        logger.debug('Destroying cluster %s' % self.clusterName)
        instancesToTerminate = self._getNodesInCluster()
        attempts = 0
        while instancesToTerminate and attempts < 3:
            self._terminateInstances(instances=instancesToTerminate)
            instancesToTerminate = self._getNodesInCluster()
            attempts += 1

        instanceGroup = self._gceDriver.ex_get_instancegroup((self.clusterName), zone=(self._zone))
        instanceGroup.destroy()

    def terminateNodes(self, nodes):
        nodeNames = [n.name for n in nodes]
        instances = self._getNodesInCluster()
        instancesToKill = [i for i in instances if i.name in nodeNames]
        self._terminateInstances(instancesToKill)

    def addNodes(self, nodeType, numNodes, preemptable, spotBid=None):
        if not self._leaderPrivateIP:
            raise AssertionError
        else:
            keyPath = None
            botoExists = False
            if self._botoPath is not None:
                if os.path.exists(self._botoPath):
                    keyPath = self.NODE_BOTO_PATH
                    botoExists = True
                else:
                    if self._sseKey:
                        keyPath = self._sseKey
                preemptable or logger.debug('Launching %s non-preemptable nodes', numNodes)
            else:
                logger.debug('Launching %s preemptable nodes', numNodes)
            userData = self._getCloudConfigUserData('worker', self._masterPublicKey, keyPath, preemptable)
            metadata = {'items': [{'key':'user-data',  'value':userData}]}
            imageType = 'coreos-stable'
            sa_scopes = [{'scopes': ['compute', 'storage-full']}]
            disk = {}
            disk['initializeParams'] = {'sourceImage':self.SOURCE_IMAGE, 
             'diskSizeGb':self._nodeStorage}
            disk.update({'boot':True,  'autoDelete':True})
            retries = 0
            workersCreated = 0
            while numNodes - workersCreated > 0 and retries < 3:
                instancesLaunched = self.ex_create_multiple_nodes('',
                  nodeType, imageType, (numNodes - workersCreated), location=(self._zone),
                  ex_service_accounts=sa_scopes,
                  ex_metadata=metadata,
                  ex_disks_gce_struct=[
                 disk],
                  description=(self._tags),
                  ex_preemptible=preemptable)
                failedWorkers = []
                for instance in instancesLaunched:
                    if isinstance(instance, GCEFailedNode):
                        logger.error('Worker failed to launch with code %s. Error message: %s' % (
                         instance.code, instance.error))
                    else:
                        node = Node(publicIP=(instance.public_ips[0]), privateIP=(instance.private_ips[0]), name=(instance.name),
                          launchTime=(instance.created_at),
                          nodeType=(instance.size),
                          preemptable=False,
                          tags=(self._tags))
                        try:
                            self._injectWorkerFiles(node, botoExists)
                            logger.debug('Created worker %s' % node.publicIP)
                            self._instanceGroup.add_instances([instance])
                            workersCreated += 1
                        except Exception as e:
                            logger.error('Failed to configure worker %s. Error message: %s' % (node.name, e))
                            failedWorkers.append(instance)

                if failedWorkers:
                    logger.error('Terminating %d failed workers' % len(failedWorkers))
                    self._terminateInstances(failedWorkers)
                retries += 1

            logger.debug('Launched %d new instance(s)', numNodes)
            if numNodes != workersCreated:
                logger.error('Failed to launch %d worker(s)', numNodes - workersCreated)
        return workersCreated

    def getProvisionedWorkers(self, nodeType, preemptable):
        assert self._leaderPrivateIP
        entireCluster = self._getNodesInCluster(nodeType=nodeType)
        logger.debug('All nodes in cluster: %s', entireCluster)
        workerInstances = []
        for instance in entireCluster:
            scheduling = instance.extra.get('scheduling')
            if scheduling:
                if scheduling.get('preemptible', False) != preemptable:
                    continue
                isWorker = True
                for ip in instance.private_ips:
                    if ip == self._leaderPrivateIP:
                        isWorker = False
                        break

                if isWorker and instance.state == 'running':
                    workerInstances.append(instance)

        logger.debug('All workers found in cluster: %s', workerInstances)
        return [Node(publicIP=(i.public_ips[0]), privateIP=(i.private_ips[0]), name=(i.name), launchTime=(i.created_at), nodeType=(i.size), preemptable=preemptable, tags=None) for i in workerInstances]

    def getLeader(self):
        instances = self._getNodesInCluster()
        instances.sort(key=(lambda x: x.created_at))
        try:
            leader = instances[0]
        except IndexError:
            raise NoSuchClusterException(self.clusterName)

        return Node(publicIP=(leader.public_ips[0]), privateIP=(leader.private_ips[0]), name=(leader.name),
          launchTime=(leader.created_at),
          nodeType=(leader.size),
          preemptable=False,
          tags=None)

    def _injectWorkerFiles(self, node, botoExists):
        """
        Set up the credentials on the worker.
        """
        node.waitForNode('toil_worker', keyName=(self._keyName))
        node.copySshKeys(self._keyName)
        node.injectFile(self._credentialsPath, GoogleJobStore.nodeServiceAccountJson, 'toil_worker')
        if self._sseKey:
            node.injectFile(self._sseKey, self._sseKey, 'toil_worker')
        if botoExists:
            node.injectFile(self._botoPath, self.NODE_BOTO_PATH, 'toil_worker')

    def _getNodesInCluster(self, nodeType=None):
        instanceGroup = self._gceDriver.ex_get_instancegroup((self.clusterName), zone=(self._zone))
        instances = instanceGroup.list_instances()
        if nodeType:
            instances = [instance for instance in instances if instance.size == nodeType]
        return instances

    def _getDriver(self):
        """  Connect to GCE """
        driverCls = get_driver(Provider.GCE)
        return driverCls((self._clientEmail), (self._googleJson),
          project=(self._projectId),
          datacenter=(self._zone))

    def _terminateInstances(self, instances):

        def worker(driver, instance):
            logger.debug('Terminating instance: %s', instance.name)
            driver.destroy_node(instance)

        threads = []
        for instance in instances:
            t = threading.Thread(target=worker, args=(self._gceDriver, instance))
            threads.append(t)
            t.start()

        logger.debug('... Waiting for instance(s) to shut down...')
        for t in threads:
            t.join()

    DEFAULT_TASK_COMPLETION_TIMEOUT = 180

    def ex_create_multiple_nodes(self, base_name, size, image, number, location=None, ex_network='default', ex_subnetwork=None, ex_tags=None, ex_metadata=None, ignore_errors=True, use_existing_disk=True, poll_interval=2, external_ip='ephemeral', ex_disk_type='pd-standard', ex_disk_auto_delete=True, ex_service_accounts=None, timeout=DEFAULT_TASK_COMPLETION_TIMEOUT, description=None, ex_can_ip_forward=None, ex_disks_gce_struct=None, ex_nic_gce_struct=None, ex_on_host_maintenance=None, ex_automatic_restart=None, ex_image_family=None, ex_preemptible=None):
        """
         Monkey patch to gce.py in libcloud to allow disk and images to be specified.
         Also changed name to a uuid below.
         The prefix 'wp' identifies preemptable nodes and 'wn' non-preemptable nodes.
        """
        driver = self._getDriver()
        if image:
            if ex_image_family:
                raise ValueError("Cannot specify both 'image' and 'ex_image_family'")
        location = location or driver.zone
        if not hasattr(location, 'name'):
            location = driver.ex_get_zone(location)
        if not hasattr(size, 'name'):
            size = driver.ex_get_size(size, location)
        if not hasattr(ex_network, 'name'):
            ex_network = driver.ex_get_network(ex_network)
        if ex_subnetwork:
            if not hasattr(ex_subnetwork, 'name'):
                ex_subnetwork = driver.ex_get_subnetwork(ex_subnetwork, region=(driver._get_region_from_zone(location)))
        if ex_image_family:
            image = driver.ex_get_image_from_family(ex_image_family)
        if image:
            if not hasattr(image, 'name'):
                image = driver.ex_get_image(image)
        if not hasattr(ex_disk_type, 'name'):
            ex_disk_type = driver.ex_get_disktype(ex_disk_type, zone=location)
        node_attrs = {'size':size,  'image':image, 
         'location':location, 
         'network':ex_network, 
         'subnetwork':ex_subnetwork, 
         'tags':ex_tags, 
         'metadata':ex_metadata, 
         'ignore_errors':ignore_errors, 
         'use_existing_disk':use_existing_disk, 
         'external_ip':external_ip, 
         'ex_disk_type':ex_disk_type, 
         'ex_disk_auto_delete':ex_disk_auto_delete, 
         'ex_service_accounts':ex_service_accounts, 
         'description':description, 
         'ex_can_ip_forward':ex_can_ip_forward, 
         'ex_disks_gce_struct':ex_disks_gce_struct, 
         'ex_nic_gce_struct':ex_nic_gce_struct, 
         'ex_on_host_maintenance':ex_on_host_maintenance, 
         'ex_automatic_restart':ex_automatic_restart, 
         'ex_preemptible':ex_preemptible}
        status_list = []
        for i in range(number):
            name = 'wp' if ex_preemptible else 'wn'
            name += str(uuid.uuid4())
            status = {'name':name,  'node_response':None,  'node':None}
            status_list.append(status)

        start_time = time.time()
        complete = False
        while not complete:
            if time.time() - start_time >= timeout:
                raise Exception('Timeout (%s sec) while waiting for multiple instances')
            complete = True
            time.sleep(poll_interval)
            for status in status_list:
                if not status['node']:
                    if not status['node_response']:
                        driver._multi_create_node(status, node_attrs)
                    else:
                        driver._multi_check_node(status, node_attrs)
                    if not status['node']:
                        complete = False

        node_list = []
        for status in status_list:
            node_list.append(status['node'])

        return node_list