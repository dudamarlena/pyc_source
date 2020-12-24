# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid_move/rain/move/Fabric.py
# Compiled at: 2012-07-23 13:51:22
"""
The Fabric module

"""
__author__ = 'Fugang Wang'
__version__ = '0.1'
import abc, json, re, logging, logging.handlers
from futuregrid_move.rain.move.Resource import Resource, Node, Cluster, Service
from futuregrid_move.rain.move.EucaService import EucaService
from futuregrid_move.rain.move.OpenStackService import OpenStackService
from futuregrid_move.rain.move.NimbusService import NimbusService
from futuregrid_move.rain.move.HPCService import HPCService
from teefaa.teefaa import Teefaa

class Inventory(object):
    """Abstract base class that defines inventory for a fabric.
    read(), and write() methods have to be implemented"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read(self):
        """
        load the inventory info and returns a dict object in the format of:
        {'nodes':[[node1id, node1name, node1ip], ...],
        'clusters':{clusteridentifier:[[node1id, node1name, node1ip], ...], ...},
        'services':{serviceidentifier:{'nodes':[node1id, node2id, ...], 'type':servicetype}, ...}
        }
        """
        pass

    @abc.abstractmethod
    def write(self, data):
        """
        write the updated dict object as defined in the read() per data persistence method.
        """
        pass


class InventoryFile(Inventory):
    """file based implementation for the inventory class"""

    def __init__(self, fname):
        self._cfgfile = fname
        self._res = dict()

    def read(self):
        """reading from file"""
        file_inv = open(self._cfgfile)
        content = file_inv.read()
        file_inv.close()
        nodes = []
        clusters = dict()
        services = dict()
        current = None
        lines = re.split('\n', content)
        for line in lines:
            if line:
                linesregex = re.compile('\\[(.+)\\]')
                m = linesregex.match(line)
                if m is not None:
                    header = m.group(1)
                    headerclusterregex = re.compile('CLUSTER:(.+)')
                    m = headerclusterregex.match(header)
                    if m is not None:
                        clustername = m.group(1).lower()
                        clusters[clustername] = []
                        current = clusters[clustername]
                    else:
                        headerserviceregex = re.compile('SERVICE:(.+):(.+)')
                        m = headerserviceregex.match(header)
                        servicetype = m.group(1).lower()
                        servicename = m.group(2).lower()
                        services[servicename] = dict()
                        services[servicename]['type'] = servicetype
                        services[servicename]['nodes'] = []
                        current = services[servicename]['nodes']
                else:
                    nodeallregex = re.compile('(.+),(.*),(.*)')
                    m = nodeallregex.match(line)
                    if m is not None:
                        resId = m.group(1)
                        name = m.group(2)
                        ip = m.group(3)
                        nodes.append([resId, name, ip, clustername])
                        current.append([resId, name, ip, clustername])
                    else:
                        nodeidregex = re.compile('(.+)')
                        m = nodeidregex.match(line)
                        if m is not None:
                            resId = m.group(1)
                            current.append(resId)
                        else:
                            print 'ERROR'

        ret = {'nodes': nodes, 'clusters': clusters, 'services': services}
        return ret

    def write(self, data):
        """construct strings from he updated data and write it to file"""
        clusters = data['clusters']
        services = data['services']
        file_inv = open(self._cfgfile, 'w')
        str2print = ''
        for acluster in sorted(clusters.keys()):
            clustername = acluster
            cluster = clusters[clustername]
            str2print += '[CLUSTER:' + clustername.upper() + ']\n'
            clusternodes = cluster.list()
            for anodeid in sorted(clusternodes.keys()):
                node = clusternodes[anodeid]
                str2print += node.identifier + ',' + node.name + ',' + node.ip + '\n'

            str2print += '\n'

        for aservice in sorted(services.keys()):
            servicename = aservice
            service = services[servicename]
            servicetype = service.type
            str2print += '[SERVICE:' + servicetype.upper() + ':' + servicename.upper() + ']\n'
            servicenodes = service.list()
            for anodeid in sorted(servicenodes.keys()):
                node = servicenodes[anodeid]
                str2print += node.identifier + '\n'

            str2print += '\n'

        file_inv.write(str2print)
        file_inv.close()


class InventoryDB(Inventory):
    """database based implementation class for inventory"""

    def __init__(self, config):
        pass

    def read(self):
        pass

    def write(self):
        pass


class Fabric(object):
    """Fabric class that defines a set of nodes, clusters, and services"""
    svctype = {'hpc': 'HPC', 'eucalyptus': 'Euca', 'nimbus': 'Nimbus', 'openstack': 'OpenStack'}

    def __init__(self, moveConf, logger, verbose=True, nodes=(), clusters=(), services=()):
        self._moveConf = moveConf
        self.logger = logger
        self.verbose = verbose
        self._inventory = None
        self._nodes = {}
        self._clusters = {}
        self._services = {}
        self.teefaaobj = Teefaa()
        self.update(nodes, clusters, services)
        return

    def load(self, inventory):
        """load data from inventory to bootstrap the fabric"""
        self._inventory = inventory
        data = self._inventory.read()
        if self.verbose:
            print data
        else:
            self.logger.debug(str(data))
        _nodes = []
        _clusters = []
        _services = []
        nodesdata = data['nodes']
        clustersdata = data['clusters']
        servicesdata = data['services']
        for node in nodesdata:
            _nodes.append(Node(node[0], node[1], node[2], node[3]))

        self.updateNodes(_nodes)
        for clustername in clustersdata.keys():
            acluster = Cluster(clustername)
            clusterdata = clustersdata[clustername]
            for nodedata in clusterdata:
                acluster.add(self.getNode(nodedata[0]))

            _clusters.append(acluster)

        for servicename in servicesdata.keys():
            atype = servicesdata[servicename]['type']
            nodeids = servicesdata[servicename]['nodes']
            nodes = {}
            for resId in nodeids:
                anode = self.getNode(resId)
                anode.allocated = servicename
                nodes[resId] = anode

            classname = Fabric.svctype[atype] + 'Service'
            aservice = eval(classname)(servicename, nodes)
            if aservice.load_config(self._moveConf):
                aservice.setLogger(self.logger)
                aservice.setVerbose(self.verbose)
                aservice.setTeefaa(self.teefaaobj)
            else:
                msg = 'Loading configuration of the Service ' + str(aservice.identifier) + '. The service will not be included. ' + ' Please add service configuration in the fg-server.conf file under a section called Move-<service>-<site> (i.e. Move-eucalyptus-sierra)'
                self.logger.error(msg)
                print 'ERROR: ' + msg
            _services.append(aservice)

        self.update(_nodes, _clusters, _services)

    def store(self):
        """data persistence after new update"""
        data = {'clusters': self.getCluster(), 'services': self.getService()}
        self._inventory.write(data)

    def getNode(self, identifier=None):
        """get a node based on the identifier, or return all nodes if id not provided"""
        if identifier is not None:
            if self._nodes.has_key(identifier):
                ret = self._nodes[identifier]
            else:
                ret = None
        else:
            ret = self._nodes
        return ret

    def getCluster(self, identifier=None):
        """get a cluster based on the identifier, or return all clusters if id not provided"""
        if identifier is not None:
            if self._clusters.has_key(identifier):
                ret = self._clusters[identifier]
            else:
                ret = None
        else:
            ret = self._clusters
        return ret

    def getService(self, identifier=None):
        """get a service based on the identifier, or return all services if id not provided"""
        if identifier is not None:
            if self._services.has_key(identifier):
                ret = self._services[identifier]
            else:
                ret = None
        else:
            ret = self._services
        return ret

    def addNode(self, node):
        """Add a Node to the node dict"""
        self._nodes[node.identifier] = node

    def addCluster(self, cluster):
        """Add a Cluster to the cluster dict"""
        self._clusters[cluster.identifier] = cluster

    def addService(self, service):
        """Add a Service to the service dict"""
        success = True
        msg = 'OK'
        if service.load_config(self._moveConf):
            service.setLogger(self.logger)
            service.setVerbose(self.verbose)
            service.setTeefaa(self.teefaaobj)
            self._services[service.identifier] = service
        else:
            msg = 'Loading configuration of the Service ' + str(service.identifier) + '. The service will not be included. ' + ' Please add service configuration in the fg-server.conf file under a section called Move-<service>-<site> (i.e. Move-eucalyptus-sierra)'
            self.logger.error(msg)
            success = False
        return (
         success, msg)

    def update(self, nodes=(), clusters=(), services=()):
        """update the nodes, clusters, and services data"""
        self.updateNodes(nodes)
        self.updateClusters(clusters)
        self.updateServices(services)
        if self.verbose:
            print 'updating inventory....'
            print self._inventory
            print 'just printed the inventory of the fabric'
        else:
            self.logger.debug('updating inventory....')
        if self._inventory is not None:
            self.store()
        return

    def updateNodes(self, nodes=()):
        """update the nodes list"""
        self._nodes = dict()
        for node in nodes:
            key = node.identifier
            self._nodes[key] = node

    def updateClusters(self, clusters=()):
        """update the clusters data"""
        self._clusters = dict()
        for cluster in clusters:
            key = cluster.identifier
            self._clusters[key] = cluster

    def updateServices(self, services=()):
        """update the services data"""
        self._services = dict()
        for service in services:
            key = service.identifier
            self._services[key] = service

    def info(self):
        """info of the fabric - identifiers of all nodes, clusters, and services"""
        nodes = 'Nodes:\n' + (',').join(sorted(self._nodes.keys()))
        clusters = 'Clusters:\n' + (',').join(sorted(self._clusters.keys()))
        services = 'Services:\n' + (',').join(sorted(self._services.keys()))
        return nodes + '\n' + clusters + '\n' + services + '\n'

    def __repr__(self):
        return self.info()