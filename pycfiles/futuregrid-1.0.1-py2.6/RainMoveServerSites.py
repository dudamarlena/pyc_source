# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/rain/move/RainMoveServerSites.py
# Compiled at: 2012-05-09 14:29:13
"""
Description: Server to do the real operations in the machines. Install software in machine and add/remove from infrastructure.
"""
__author__ = 'Javier Diaz'
from types import *
import re, logging, logging.handlers, random
from random import randrange
import os, sys, socket, ssl
from multiprocessing import Process
from subprocess import *
import time
from futuregrid.image.repository.client.IRServiceProxy import IRServiceProxy
from futuregrid.utils.FGTypes import FGCredential
from futuregrid.utils import FGAuth
from futuregrid.rain.RainServerConf import RainServerConf

class RainMoveServerSites(object):

    def __init__(self):
        super(RainMoveServerSites, self).__init__()
        self.numparams = 4
        self._rainSitesConf = RainServerConf()
        self._rainSitesConf.load_rainMoveServerConfig()
        self.port = self._rainSitesConf.getPortRainMoveSites()
        self.log_filename = self._rainSitesConf.getLogRainMoveSites()
        self.logLevel = self._rainSitesConf.getLogLevelRainMoveSites()
        self._ca_certs = self._rainSitesConf.getCaCertsRainMoveSites()
        self._certfile = self._rainSitesConf.getCertFileRainMoveSites()
        self._keyfile = self._rainSitesConf.getKeyFileRainMoveSites()
        print '\nReading Configuration file from ' + self._rainSitesConf.getConfigFile() + '\n'
        self.logger = self.setup_logger('')
        verbose = False
        printLogStdout = False
        self._reposervice = IRServiceProxy(verbose, printLogStdout)

    def setup_logger(self, extra):
        logger = logging.getLogger('RainMoveServerSites' + extra)
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

    def checkUserStatus(self, userId, passwd, userIdB):
        """
        return "Active", "NoActive", "NoUser"; also False in case the connection with the repo fails
        """
        if not self._reposervice.connection():
            msg = 'ERROR: Connection with the Image Repository failed'
            self.logger.error(msg)
            return False
        else:
            self.logger.debug('Checking User Status')
            status = self._reposervice.getUserStatus(userId, passwd, userIdB)
            self._reposervice.disconnect()
            return status

    def checknopasswd(self, fromaddr):
        status = False
        if self.user in self._nopasswdusers:
            if fromaddr in self._nopasswdusers[self.user]:
                status = True
        return status

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.port))
        sock.listen(1)
        self.logger.info('Starting Server on port ' + str(self.port))
        proc_list = []
        total_count = 0
        while True:
            if len(proc_list) == self.proc_max:
                full = True
                while full:
                    for i in range(len(proc_list) - 1, -1, -1):
                        if not proc_list[i].is_alive():
                            proc_list.pop(i)
                            full = False

                    if full:
                        time.sleep(self.refresh_status)

            total_count += 1
            (newsocket, fromaddr) = sock.accept()
            connstream = 0
            try:
                connstream = ssl.wrap_socket(newsocket, server_side=True, ca_certs=self._ca_certs, cert_reqs=ssl.CERT_REQUIRED, certfile=self._certfile, keyfile=self._keyfile, ssl_version=ssl.PROTOCOL_TLSv1)
                proc_list.append(Process(target=self.process_client, args=(connstream, fromaddr[0])))
                proc_list[(len(proc_list) - 1)].start()
            except ssl.SSLError:
                self.logger.error('Unsuccessful connection attempt from: ' + repr(fromaddr))
                self.logger.info('Rain Server Sites Request DONE')
            except socket.error:
                self.logger.error('Error with the socket connection')
                self.logger.info('Rain Server Sites Request DONE')
            except:
                self.logger.error('Uncontrolled Error: ' + str(sys.exc_info()))
                if type(connstream) is ssl.SSLSocket:
                    connstream.shutdown(socket.SHUT_RDWR)
                    connstream.close()
                self.logger.info('Rain Server Sites Request DONE')

    def process_client(self, connstream, fromaddr):
        start_all = time.time()
        self.logger = self.setup_logger('.' + str(os.getpid()))
        self.logger.info('Accepted new connection')
        data = connstream.read(2048)
        self.logger.debug('msg received: ' + data)
        params = data.split(',')
        infrastructure = params[0].strip()
        self.user = params[1].strip()
        passwd = params[2].strip()
        passwdtype = params[3].strip()
        if len(params) != self.numparams:
            msg = 'ERROR: incorrect message'
            self.errormsg(connstream, msg)
            return
        retry = 0
        maxretry = 3
        endloop = False
        while not endloop:
            if not self.checknopasswd(fromaddr):
                userCred = FGCredential(passwdtype, passwd)
                if self.auth(userCred):
                    userstatus = self.checkUserStatus(self.user, passwd, self.user)
                    if userstatus == 'Active':
                        connstream.write('OK')
                    else:
                        if userstatus == 'NoActive':
                            connstream.write('NoActive')
                            msg = 'ERROR: The user ' + self.user + ' is not active'
                            self.errormsg(connstream, msg)
                            return
                        else:
                            if userstatus == 'NoUser':
                                connstream.write('NoUser')
                                msg = 'ERROR: The user ' + self.user + ' does not exist'
                                self.logger.error(msg)
                                self.logger.info('IaaS register server Request DONE')
                                return
                            connstream.write('Could not connect with image repository server')
                            msg = 'ERROR: Could not connect with image repository server to verify the user status'
                            self.logger.error(msg)
                            self.logger.info('IaaS register server Request DONE')
                            return
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
                connstream.write('OK')
                endloop = True