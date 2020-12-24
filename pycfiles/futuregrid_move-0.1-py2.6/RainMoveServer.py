# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid_move/rain/move/RainMoveServer.py
# Compiled at: 2012-07-28 18:35:38
__author__ = 'Javier Diaz'
import argparse, logging, logging.handlers, os, re, socket, ssl, sys, time
from threading import Thread, Lock
from futuregrid_move.rain.move.Resource import Resource, Node, Cluster, Service
from futuregrid_move.rain.move.HPCService import HPCService
from futuregrid_move.rain.move.EucaService import EucaService
from futuregrid_move.rain.move.OpenStackService import OpenStackService
from futuregrid_move.rain.move.OpenNebulaService import OpenNebulaService
from futuregrid_move.rain.move.NimbusService import NimbusService
from futuregrid_move.rain.move.Fabric import Fabric, Inventory, InventoryFile, InventoryDB
from futuregrid_move.rain.move.RainMoveServerConf import RainMoveServerConf
from futuregrid_move.utils import FGAuth
from futuregrid_move.utils.FGTypes import FGCredential

class RainMoveServer(object):

    def __init__(self, inventoryfile):
        super(RainMoveServer, self).__init__()
        self.numparams = 7
        self.user = ''
        self.element = ''
        self.operation = ''
        self.arguments = None
        self.forcemove = False
        self.lock = Lock()
        self._rainConf = RainMoveServerConf()
        self._rainConf.load_moveServerConfig()
        self.port = self._rainConf.getMovePort()
        self.authorizedusers = self._rainConf.getMoveAuthorizedUsers()
        self.log_filename = self._rainConf.getMoveLog()
        self.logLevel = self._rainConf.getMoveLogLevel()
        self.proc_max = self._rainConf.getMoveProcMax()
        self.refresh_status = self._rainConf.getMoveRefreshStatus()
        self._ca_certs = self._rainConf.getMoveServerCaCerts()
        self._certfile = self._rainConf.getMoveServerCertFile()
        self._keyfile = self._rainConf.getMoveServerKeyFile()
        print '\nReading Configuration file from ' + self._rainConf.getConfigFile() + '\n'
        self.logger = self.setup_logger()
        self.fgfabric = Fabric(self._rainConf, self.logger, False)
        if inventoryfile != None:
            fginventory = InventoryFile(inventoryfile)
            self.fgfabric.load(fginventory)
        return

    def load(self, inventoryfile):
        fginventory = InventoryFile(inventoryfile)
        self.fgfabric.load(fginventory)

    def setup_logger(self):
        logger = logging.getLogger('RainMoveServer')
        logger.setLevel(self.logLevel)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(self.log_filename)
        handler.setLevel(self.logLevel)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
        return logger

    def auth(self, userCred):
        return FGAuth.auth(self.user, userCred)

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.port))
        sock.listen(1)
        self.logger.info('Starting Server on port ' + str(self.port))
        while True:
            (newsocket, fromaddr) = sock.accept()
            connstream = None
            try:
                try:
                    connstream = ssl.wrap_socket(newsocket, server_side=True, ca_certs=self._ca_certs, cert_reqs=ssl.CERT_REQUIRED, certfile=self._certfile, keyfile=self._keyfile, ssl_version=ssl.PROTOCOL_TLSv1)
                    self.process_client(connstream)
                except ssl.SSLError:
                    self.logger.error('Unsuccessful connection attempt from: ' + repr(fromaddr))
                except socket.error:
                    self.logger.error('Error with the socket connection')

            finally:
                if type(connstream) is ssl.SSLSocket:
                    try:
                        connstream.shutdown(socket.SHUT_RDWR)
                        connstream.close()
                    except:
                        pass

        return

    def process_client(self, connstream):
        self.logger.info('Accepted new connection')
        data = connstream.read(2048)
        self.logger.debug('received data: ' + data)
        params = data.split('|')
        if len(params) != self.numparams:
            msg = 'ERROR: incorrect message'
            self.errormsg(connstream, msg)
            return
        else:
            self.user = params[0]
            passwd = params[1]
            passwdtype = params[2]
            self.resource = params[3]
            self.operation = params[4]
            try:
                value = eval(params[5])
                if value:
                    self.arguments = value
                else:
                    self.arguments = [
                     None]
            except:
                self.arguments = [
                 params[5]]

            try:
                self.forcemove = eval(params[6].strip())
            except:
                self.forcemove = False

            retry = 0
            maxretry = 3
            endloop = False
            while not endloop:
                userCred = FGCredential(passwdtype, passwd)
                if self.user in self.authorizedusers:
                    if self.auth(userCred):
                        connstream.write('OK')
                        endloop = True
                    else:
                        retry += 1
                        if retry < maxretry:
                            connstream.write('TryAuthAgain')
                            passwd = connstream.read(2048)
                        else:
                            msg = 'ERROR: authentication failed'
                            endloop = True
                            self.errormsg(connstream, msg)
                            return
                else:
                    msg = 'ERROR: authentication failed. User is not allowed to use this service.'
                    endloop = True
                    self.errormsg(connstream, msg)
                    return

            if self.resource == 'service' and (self.operation == 'add' or self.operation == 'remove' or self.operation == 'move'):
                nodelist = self.arguments[:len(self.arguments) - 1]
                if self.operation == 'move':
                    nodelist = self.arguments[:len(self.arguments) - 2]
                full = False
                proc_list = []
                joinstatus = []
                for node in nodelist:
                    if len(proc_list) == self.proc_max:
                        full = True
                        while full:
                            for i in range(len(proc_list) - 1, -1, -1):
                                if not proc_list[i].is_alive():
                                    proc_list.pop(i)
                                    full = False

                            if full:
                                time.sleep(self.refresh_status)

                    if self.operation == 'move':
                        new_arguments = [
                         node, self.arguments[(len(self.arguments) - 2)], self.arguments[(len(self.arguments) - 1)]]
                    else:
                        new_arguments = [
                         node, self.arguments[(len(self.arguments) - 1)]]
                    proc_list.append(Thread(target=eval('self.wrap_' + self.operation), args=(joinstatus, new_arguments)))
                    proc_list[(len(proc_list) - 1)].start()

                for i in proc_list:
                    i.join()

                status = ''
                for i in joinstatus:
                    status += i + '\n'
                    if re.search('^ERROR', i):
                        self.logger.error(i)

                self.okmsg(connstream, status)
                self.printCurrentStatus()
            else:
                status = eval('self.' + self.operation + '(' + str(self.arguments) + ')')
                if re.search('^ERROR', status):
                    self.errormsg(connstream, status)
                else:
                    self.okmsg(connstream, status)
            self.logger.info('Rain Move Server DONE')
            return

    def create(self, arguments):
        """create empty clusters or services"""
        status = 'OK'
        if self.resource == 'cluster':
            if self.fgfabric.getCluster(self.arguments[0]) == None:
                self.fgfabric.addCluster(Cluster(self.arguments[0]))
                self.fgfabric.store()
                status = 'The cluster has been successfully created.'
            else:
                status = 'ERROR: the Cluster already exists'
        elif self.resource == 'service':
            if self.fgfabric.getService(self.arguments[0]) == None:
                if self.arguments[1].lower() == 'hpc':
                    (success, msg) = self.fgfabric.addService(HPCService(self.arguments[0]))
                elif self.arguments[1].lower() == 'eucalyptus':
                    (success, msg) = self.fgfabric.addService(EucaService(self.arguments[0]))
                elif self.arguments[1].lower() == 'openstack':
                    (success, msg) = self.fgfabric.addService(OpenStackService(self.arguments[0]))
                elif self.arguments[1].lower() == 'nimbus':
                    (success, msg) = self.fgfabric.addService(NimbusService(self.arguments[0]))
                elif self.arguments[1].lower() == 'opennebula':
                    (success, msg) = self.fgfabric.addService(OpenNebulaService(self.arguments[0]))
                if success:
                    self.fgfabric.store()
                    status = 'The service has been successfully created.'
                else:
                    status = 'ERROR: ' + msg
            else:
                status = 'ERROR: the Service already exists'
        return status

    def wrap_add(self, joinstatus, arguments):
        joinstatus.append(self.add(arguments))

    def add(self, arguments):
        """add new node; existing node to a cluster; existing node to a service, etc.
        """
        status = 'OK'
        if self.resource == 'node':
            newnode = Node(arguments[0], arguments[1], arguments[2], arguments[3])
            if self.fgfabric.getNode(arguments[0]) == None:
                cluster = self.fgfabric.getCluster(arguments[3])
                if cluster != None:
                    self.fgfabric.addNode(newnode)
                    if not cluster.add(newnode):
                        status = 'ERROR: adding the cluster'
                    self.fgfabric.store()
                else:
                    status = 'ERROR: the Node cannot be added because the Cluster does not exists'
            else:
                status = 'ERROR: the Node already exists'
        elif self.resource == 'service':
            existingnode = self.fgfabric.getNode(arguments[0])
            if existingnode != None:
                service = self.fgfabric.getService(arguments[1])
                if service != None:
                    (success, restatus) = service.add(existingnode)
                    if not success:
                        status = 'ERROR: adding the node ' + arguments[0] + ' to the service ' + arguments[1] + '. ' + str(restatus)
                    else:
                        status = 'The node ' + arguments[0] + ' have been successfully integrated into the Cloud. ' + str(restatus)
                    self.lock.acquire()
                    try:
                        try:
                            self.fgfabric.store()
                        except:
                            status = 'ERROR: adding the node ' + arguments[0] + '. Storing information in the persistent data in the Fabric. ' + str(sys.exc_info())

                    finally:
                        self.lock.release()

                else:
                    status = 'ERROR: the Node ' + arguments[0] + ' cannot be added because the Service does not exists'
            else:
                status = 'ERROR: the Node ' + arguments[0] + ' does not exists'
        return status

    def wrap_remove(self, joinstatus, arguments):
        joinstatus.append(self.remove(arguments))

    def remove(self, arguments):
        status = 'OK'
        if self.resource == 'node':
            status = 'ERROR: Not supported yet'
        elif self.resource == 'cluster':
            status = 'ERROR: Not supported yet'
        elif self.resource == 'service':
            service = self.fgfabric.getService(arguments[1])
            if service != None:
                (success, restatus) = service.remove(arguments[0], self.forcemove)
                if not success:
                    status = 'ERROR: removing the node ' + arguments[0] + ' from the service ' + arguments[1] + '. ' + str(restatus)
                else:
                    status = 'The node ' + arguments[0] + ' have been successfully deleted from the Cloud. ' + str(restatus)
                self.lock.acquire()
                try:
                    try:
                        self.fgfabric.store()
                    except:
                        status = 'ERROR: removing the node ' + arguments[0] + '. Storing information in the persistent data in the Fabric. ' + str(sys.exc_info())

                finally:
                    self.lock.release()

            else:
                status = 'ERROR: the Node ' + arguments[0] + ' cannot be deleted because the Service does not exists'
        return status

    def wrap_move(self, joinstatus, arguments):
        joinstatus.append(self.move(arguments))

    def move(self, arguments):
        status = 'ERROR: Wrong resource.'
        if self.resource == 'service':
            status = self.remove(arguments)
            if not re.search('^ERROR', status):
                arguments[1] = arguments[2]
                status = self.add(arguments)
        return status

    def info(self, arguments):
        if arguments[0] in self.fgfabric.getNode().keys():
            return str(self.fgfabric.getNode()[arguments[0]])
        else:
            return 'ERROR: The node does not exists.'

    def lists(self, arguments):
        status = 'ERROR: Wrong resource.'
        if self.resource == 'cluster':
            if not arguments[0]:
                cluster = self.fgfabric.getCluster()
                status = 'The list of clusters is: ' + str(cluster.keys())
            else:
                cluster = self.fgfabric.getCluster(arguments[0])
                if cluster != None:
                    status = 'Details of cluster ' + str(arguments[0]) + ' cluster: ' + str(cluster.list().keys())
        elif self.resource == 'service':
            if not arguments[0]:
                service = self.fgfabric.getService()
                status = 'The list of services is: ' + str(service.keys())
            else:
                service = self.fgfabric.getService(arguments[0])
                if service != None:
                    status = 'Details of service ' + str(arguments[0]) + ' service: ' + str(service.list().keys())
        return status

    def listfreenodes(self, arguments):
        status = 'ERROR: getting the list of free nodes'
        dictfree = {}
        if not arguments[0]:
            listcluster = self.fgfabric.getCluster()
            for i in listcluster:
                dictfree[i] = []
                cluster = self.fgfabric.getCluster(i)
                listnodes = cluster.list()
                for j in listnodes:
                    if listnodes[j].allocated == 'FREE':
                        dictfree[i].append(listnodes[j].identifier)

            status = str(dictfree)
        else:
            cluster = self.fgfabric.getCluster(arguments[0])
            dictfree[arguments[0]] = []
            listnodes = cluster.list()
            for j in listnodes:
                if listnodes[j].allocated == 'FREE':
                    dictfree[i].append(listnodes[j].identifier)

            status = str(dictfree)
        return status

    def printCurrentStatus(self):
        services_details = {}
        services = self.fgfabric.getService()
        for i in services.keys():
            serv = self.fgfabric.getService(i)
            services_details[i] = serv.list().keys()

        services_details['freenodes'] = self.listfreenodes([None])
        self.logger.debug('CURRENT_STATUS=' + str(services_details))
        return

    def okmsg(self, connstream, msg):
        connstream.write(msg)
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()

    def errormsg(self, connstream, msg):
        self.logger.error(msg)
        try:
            connstream.write(msg)
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            self.logger.debug('In errormsg: ' + str(sys.exc_info()))

        self.logger.info('Rain Move Server DONE')


def main():
    parser = argparse.ArgumentParser(prog='RainMoveServer', formatter_class=argparse.RawDescriptionHelpFormatter, description='FutureGrid Rain Move Server Help ')
    parser.add_argument('-l', '--load', dest='inventoryFile', metavar='inventoryFile', required=True, help='File that contains the machines/services inventory')
    args = parser.parse_args()
    server = RainMoveServer(args.inventoryFile)
    server.start()


if __name__ == '__main__':
    main()