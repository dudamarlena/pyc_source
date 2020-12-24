# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/management/IMRegisterServerIaaS.py
# Compiled at: 2012-09-06 11:03:15
"""
Description: IaaS image registration server.  Customizes images and return them to the user side to register them in the 
corresponding IaaS framework
"""
__author__ = 'Javier Diaz, Andrew Younge'
from types import *
import re, logging, logging.handlers, random
from random import randrange
import os, sys, socket, ssl
from multiprocessing import Process
from subprocess import *
from xml.dom.minidom import Document, parseString, parse
import xmlrpclib, time
from futuregrid.image.management.IMServerConf import IMServerConf
from futuregrid.image.repository.client.IRServiceProxy import IRServiceProxy
from futuregrid.utils.FGTypes import FGCredential
from futuregrid.utils import FGAuth

class IMRegisterServerIaaS(object):

    def __init__(self):
        super(IMRegisterServerIaaS, self).__init__()
        self.path = ''
        self.numparams = 9
        self.name = ''
        self.givenname = ''
        self.operatingsystem = ''
        self.version = ''
        self.arch = ''
        self.kernel = ''
        self.user = ''
        self.iaas = ''
        self._registerConf = IMServerConf()
        self._registerConf.load_registerServerIaasConfig()
        self.port = self._registerConf.getIaasPort()
        self.http_server = self._registerConf.getHttpServerIaas()
        self.proc_max = self._registerConf.getProcMaxIaas()
        self.refresh_status = self._registerConf.getRefreshStatusIaas()
        self._nopasswdusers = self._registerConf.getNoPasswdUsersIaas()
        self.tempdir = self._registerConf.getTempDirIaas()
        self.log_filename = self._registerConf.getLogIaas()
        self.logLevel = self._registerConf.getLogLevelIaas()
        self._ca_certs = self._registerConf.getCaCertsIaas()
        self._certfile = self._registerConf.getCertFileIaas()
        self._keyfile = self._registerConf.getKeyFileIaas()
        print '\nReading Configuration file from ' + self._registerConf.getConfigFile() + '\n'
        self.logger = self.setup_logger('')
        verbose = False
        printLogStdout = False
        self._reposervice = IRServiceProxy(verbose, printLogStdout)

    def setup_logger(self, extra):
        logger = logging.getLogger('RegisterIaaS' + extra)
        logger.setLevel(self.logLevel)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(self.log_filename)
        handler.setLevel(self.logLevel)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
        return logger

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
                self.logger.info('IaaS register server Request DONE')
            except socket.error:
                self.logger.error('Error with the socket connection')
                self.logger.info('IaaS register server Request DONE')
            except:
                self.logger.error('Uncontrolled Error: ' + str(sys.exc_info()))
                if type(connstream) is ssl.SSLSocket:
                    connstream.shutdown(socket.SHUT_RDWR)
                    connstream.close()
                self.logger.info('IaaS register server Request DONE')

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

    def checkKernel(self):
        status = False
        if self.iaas == 'euca':
            status = self.kernel in self._euca_auth_kernels
        elif self.iaas == 'nimbus':
            status = self.kernel in self._nimbus_auth_kernels
        elif self.iaas == 'openstack':
            status = self.kernel in self._openstack_auth_kernels
        elif self.iaas == 'opennebula':
            status = self.kernel in self._opennebula_auth_kernels
        return status

    def checkIaasAvail(self):
        status = False
        if self.iaas == 'euca':
            if not self.default_euca_kernel == '':
                status = True
        elif self.iaas == 'nimbus':
            if not self.default_nimbus_kernel == '':
                status = True
        elif self.iaas == 'openstack':
            if not self.default_openstack_kernel == '':
                status = True
        elif self.iaas == 'opennebula':
            if not self.default_opennebula_kernel == '':
                status = True
        return status

    def loadIaasConfig(self, iaasSite):
        self._registerConf.loadIaasSiteConfig(iaasSite)
        self.default_euca_kernel = self._registerConf.getDefaultEucaKernel()
        self.default_nimbus_kernel = self._registerConf.getDefaultNimbusKernel()
        self.default_openstack_kernel = self._registerConf.getDefaultOpenstackKernel()
        self.default_opennebula_kernel = self._registerConf.getDefaultOpennebulaKernel()
        self._euca_auth_kernels = self._registerConf.getEucaAuthKernels()
        self._nimbus_auth_kernels = self._registerConf.getNimbusAuthKernels()
        self._openstack_auth_kernels = self._registerConf.getOpenstackAuthKernels()
        self._opennebula_auth_kernels = self._registerConf.getOpennebulaAuthKernels()

    def process_client(self, connstream, fromaddr):
        start_all = time.time()
        self.logger = self.setup_logger('.' + str(os.getpid()))
        self.logger.info('Accepted new connection')
        data = connstream.read(2048)
        self.logger.debug('msg received: ' + data)
        params = data.split(',')
        imgID = params[0].strip()
        imgSource = params[1].strip()
        machinename = params[2].strip()
        self.iaas = params[3].strip()
        self.kernel = params[4].strip()
        self.user = params[5].strip()
        passwd = params[6].strip()
        passwdtype = params[7].strip()
        ldap = False
        try:
            ldap = eval(params[8].strip())
        except:
            self.logger.warning('Ldap configure set to False in except')
            ldap = False

        if len(params) != self.numparams:
            msg = 'ERROR: incorrect message'
            self.errormsg(connstream, msg)
            return
        else:
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

            if imgID == 'infosites':
                infosites = self._registerConf.listIaasSites()
                self.logger.debug('Information Cloud Sites: ' + str(infosites))
                connstream.write(str(infosites))
                connstream.shutdown(socket.SHUT_RDWR)
                connstream.close()
                self.logger.info('Image Register Request (info sites) DONE')
                return
            output = self.loadIaasConfig(machinename)
            if output == 'ERROR':
                msg = 'ERROR: The specified site ' + machinename + '. Please use the option --listsites to list available sites and its services. \n'
                self.errormsg(connstream, msg)
                return
            if imgID == 'kernels':
                kernelslist = {}
                if self.iaas == 'euca':
                    kernelslist['Default'] = self.default_euca_kernel
                    kernelslist['Authorized'] = self._euca_auth_kernels
                elif self.iaas == 'nimbus':
                    kernelslist['Default'] = self.default_nimbus_kernel
                    kernelslist['Authorized'] = self._nimbus_auth_kernels
                elif self.iaas == 'openstack':
                    kernelslist['Default'] = self.default_openstack_kernel
                    kernelslist['Authorized'] = self._openstack_auth_kernels
                elif self.iaas == 'opennebula':
                    kernelslist['Default'] = self.default_opennebula_kernel
                    kernelslist['Authorized'] = self._opennebula_auth_kernels
                self.logger.debug(self.iaas + ' default kernels list: ' + str(kernelslist['Default']))
                self.logger.debug(self.iaas + ' kernels list: ' + str(kernelslist['Authorized']))
                connstream.write(str(kernelslist))
                connstream.shutdown(socket.SHUT_RDWR)
                connstream.close()
                self.logger.info('Image Register Request (kernel list ' + self.iaas + ') DONE')
                return
            if not self.checkIaasAvail():
                msg = 'ERROR: The specified infrastructure ' + self.iaas + ' is not available on ' + machinename + '. Please use the option --listservices to list available sites and its services. \n'
                self.errormsg(connstream, msg)
                return
            if self.kernel != 'None':
                if not self.checkKernel():
                    msg = 'ERROR: The specified kernel (' + self.kernel + ') is not available. Authorized kernels for ' + self.iaas + ' are: ' + str(eval('self._' + self.iaas + '_auth_kernels'))
                    self.errormsg(connstream, msg)
                    return
                self.logger.debug('The kernel ' + self.kernel + ' is valid')
            auxdir = str(randrange(999999999999999999999999))
            localtempdir = self.tempdir + '/' + auxdir + '_0'
            while os.path.isdir(localtempdir):
                auxdir = str(randrange(999999999999999999999999))
                localtempdir = self.tempdir + '/' + auxdir + '_0'

            cmd = 'mkdir -p ' + localtempdir
            self.runCmd(cmd)
            self.runCmd('chmod 777 ' + localtempdir)
            start = time.time()
            if imgSource == 'repo':
                if not self._reposervice.connection():
                    msg = 'ERROR: Connection with the Image Repository failed'
                    self.errormsg(connstream, msg)
                    return
                self.logger.info('Retrieving image from repository')
                image = self._reposervice.get(self.user, passwd, self.user, 'img', imgID, localtempdir)
                if image == None:
                    msg = 'ERROR: Cannot get access to the image with imgId ' + str(imgID)
                    self.errormsg(connstream, msg)
                    self._reposervice.disconnect()
                    self.runCmd('rm -rf ' + localtempdir)
                    return
                self._reposervice.disconnect()
            else:
                connstream.write(localtempdir)
                status = connstream.read(1024)
                status = status.split(',')
                if len(status) == 2:
                    image = localtempdir + '/' + status[1].strip()
                    if status[0].strip() != 'OK':
                        msg = 'ERROR: Receiving image from client: ' + str(status)
                        self.errormsg(connstream, msg)
                        return
                else:
                    msg = 'ERROR: Message received from client is incorrect: ' + str(status)
                    self.errormsg(connstream, msg)
                    return
            end = time.time()
            self.logger.info('TIME retrieve image from repo or client:' + str(end - start))
            if not os.path.isfile(image):
                msg = 'ERROR: file ' + image + ' not found'
                self.errormsg(connstream, msg)
                return
            start = time.time()
            if not self.handle_image(image, localtempdir, connstream):
                return
            end = time.time()
            self.logger.info('TIME untar image: ' + str(end - start))
            start = time.time()
            stat = 0
            if self.iaas == 'euca':
                stat = self.euca_method(localtempdir, ldap)
            elif self.iaas == 'nimbus':
                stat = self.nimbus_method(localtempdir, ldap)
            elif self.iaas == 'opennebula':
                stat = self.opennebula_method(localtempdir, ldap)
            elif self.iaas == 'openstack':
                stat = self.openstack_method(localtempdir, ldap)
            end = time.time()
            self.logger.info('TIME customize image for specific IaaS framework:' + str(end - start))
            start = time.time()
            max_retry = 5
            retry_done = 0
            umounted = False
            while not umounted:
                status = self.runCmd('sudo umount ' + localtempdir + '/temp')
                if status == 0:
                    umounted = True
                elif retry_done == max_retry:
                    umounted = True
                    self.logger.error('Problems to umount the image')
                else:
                    retry_done += 1
                    time.sleep(2)

            end = time.time()
            self.logger.info('TIME umount image:' + str(end - start))
            status = self.runCmd('mv -f ' + localtempdir + '/' + self.name + '.img ' + localtempdir + '/' + self.operatingsystem + self.version + self.name + '.img')
            kerneltouse = eval('self._' + self.iaas + '_auth_kernels')
            eki = kerneltouse[self.kernel][0]
            eri = kerneltouse[self.kernel][1]
            connstream.write(localtempdir + '/' + self.operatingsystem + self.version + self.name + '.img,' + eki + ',' + eri + ',' + self.operatingsystem)
            start = time.time()
            self.logger.info('Wait until client get the image')
            connstream.read()
            end = time.time()
            self.logger.info('TIME wait until client get image:' + str(end - start))
            cmd = 'rm -rf ' + localtempdir
            status = self.runCmd(cmd)
            try:
                connstream.shutdown(socket.SHUT_RDWR)
                connstream.close()
            except:
                self.logger.error('ERROR: ' + str(sys.exc_info()))

            end_all = time.time()
            self.logger.info('TIME walltime image register IaaS:' + str(end_all - start_all))
            self.logger.info('Image Register Request DONE')
            return

    def configure_ldap(self, localtempdir):
        start = time.time()
        if self.operatingsystem == 'centos':
            self.runCmd('sudo chroot ' + localtempdir + '/temp/ yum -y install fuse-sshfs')
            self.logger.info('Installing LDAP packages')
            if self.version == '5':
                self.runCmd('sudo chroot ' + localtempdir + '/temp/ yum -y install openldap-clients nss_ldap')
                self.runCmd('sudo wget ' + self.http_server + '/ldap/nsswitch.conf -O ' + localtempdir + '/temp/etc/nsswitch.conf')
            elif self.version == '6':
                self.runCmd('sudo chroot ' + localtempdir + '/temp/ yum -y install openldap-clients nss-pam-ldapd sssd')
                self.runCmd('sudo wget ' + self.http_server + '/ldap/nsswitch.conf_centos6 -O ' + localtempdir + '/temp/etc/nsswitch.conf')
                self.runCmd('sudo wget ' + self.http_server + '/ldap/sssd.conf_centos6 -O ' + localtempdir + '/temp/etc/sssd/sssd.conf')
                self.runCmd('sudo chmod 600 ' + localtempdir + '/temp/etc/sssd/sssd.conf')
                self.runCmd('sudo chroot ' + localtempdir + '/temp/ chkconfig sssd on')
            self.logger.info('Configuring LDAP access')
            self.runCmd('sudo mkdir -p ' + localtempdir + '/temp/etc/openldap/cacerts ' + localtempdir + '/temp/N/u')
            self.runCmd('sudo wget ' + self.http_server + '/ldap/cacerts/12d3b66a.0 -O ' + localtempdir + '/temp/etc/openldap/cacerts/12d3b66a.0')
            self.runCmd('sudo wget ' + self.http_server + '/ldap/cacerts/cacert.pem -O ' + localtempdir + '/temp/etc/openldap/cacerts/cacert.pem')
            self.runCmd('sudo wget ' + self.http_server + '/ldap/ldap.conf -O ' + localtempdir + '/temp/etc/ldap.conf')
            self.runCmd('sudo wget ' + self.http_server + '/ldap/openldap/ldap.conf -O ' + localtempdir + '/temp/etc/openldap/ldap.conf')
            os.system("sudo sed -i 's/enforcing/disabled/g' " + localtempdir + '/temp/etc/selinux/config')
        elif self.operatingsystem == 'ubuntu':
            f = open(localtempdir + '/_policy-rc.d', 'w')
            f.write('#!/bin/sh\nexit 101\n')
            f.close()
            self.runCmd('sudo mv -f ' + localtempdir + '/_policy-rc.d ' + localtempdir + '/temp/usr/sbin/policy-rc.d')
            self.runCmd('sudo chmod +x ' + localtempdir + '/temp/usr/sbin/policy-rc.d')
            self.runCmd('sudo chroot ' + localtempdir + '/temp/ apt-get -y install sshfs')
            self.logger.info('Configuring LDAP access')
            self.runCmd('sudo wget ' + self.http_server + '/ldap/nsswitch.conf -O ' + localtempdir + '/temp/etc/nsswitch.conf')
            self.runCmd('sudo mkdir -p ' + localtempdir + '/temp/etc/ldap/cacerts ' + localtempdir + '/temp/N/u')
            self.runCmd('sudo wget ' + self.http_server + '/ldap/cacerts/12d3b66a.0 -O ' + localtempdir + '/temp/etc/ldap/cacerts/12d3b66a.0')
            self.runCmd('sudo wget ' + self.http_server + '/ldap/cacerts/cacert.pem -O ' + localtempdir + '/temp/etc/ldap/cacerts/cacert.pem')
            self.runCmd('sudo wget ' + self.http_server + '/ldap/ldap.conf -O ' + localtempdir + '/temp/etc/ldap.conf')
            self.runCmd('sudo wget ' + self.http_server + '/ldap/openldap/ldap.conf -O ' + localtempdir + '/temp/etc/ldap/ldap.conf')
            os.system("sudo sed -i 's/openldap/ldap/g' " + localtempdir + '/temp/etc/ldap/ldap.conf')
            os.system("sudo sed -i 's/openldap/ldap/g' " + localtempdir + '/temp/etc/ldap.conf')
            self.logger.info('Installing LDAP packages')
            f = open(localtempdir + '/_ldap.install', 'w')
            f.write('#!/bin/bash\n' + 'export DEBIAN_FRONTEND=noninteractive' + '\n' + 'apt-get ' + '-y install ldap-utils libnss-ldapd nss-updatedb libnss-db')
            f.close()
            self.runCmd('sudo mv -f ' + localtempdir + '/_ldap.install ' + localtempdir + '/temp/tmp/ldap.install')
            os.system('sudo chmod +x ' + localtempdir + '/temp/tmp/ldap.install')
            self.runCmd('sudo chroot ' + localtempdir + '/temp /tmp/ldap.install')
            self.runCmd('sudo mv -f ' + localtempdir + '/temp/usr/sbin/policy-rc.d ' + localtempdir + '/_policy-rc.d')
            self.runCmd('rm -f ' + localtempdir + '/_policy-rc.d')
        end = time.time()
        self.logger.info('TIME configure LDAP (this is included in the TIME customize image for specific IaaS framework):' + str(end - start))

    def euca_method(self, localtempdir, ldap):
        stat = 0
        self.logger.debug('kernel: ' + self.kernel)
        if self.kernel == 'None':
            self.kernel = self.default_euca_kernel
        self.logger.info('Retrieving kernel ' + self.kernel)
        stat = self.runCmd('wget ' + self.http_server + 'kernel/' + self.kernel + '.modules.tar.gz -O ' + localtempdir + '/' + self.kernel + '.modules.tar.gz')
        if stat == 0:
            self.runCmd('sudo tar xfz ' + localtempdir + '/' + self.kernel + '.modules.tar.gz --directory ' + localtempdir + '/temp/lib/modules/')
            self.logger.info('Injected kernel ' + self.kernel)
            fstab = '\n# Default fstab\n /dev/sda1       /             ext3     defaults,errors=remount-ro 0 0\n /dev/sda2      /tmp          ext3    defaults 0 0\n /dev/sda3    swap          swap     defaults              0 0\n proc            /proc         proc     defaults                   0 0\n devpts          /dev/pts      devpts   gid=5,mode=620             0 0\n '
            f = open(localtempdir + '/fstab', 'w')
            f.write(fstab)
            f.close()
            self.runCmd('sudo mv -f ' + localtempdir + '/fstab ' + localtempdir + '/temp/etc/fstab')
            self.runCmd('sudo chown root:root ' + localtempdir + '/temp/etc/fstab')
            self.logger.info('fstab Injected')
            if self.operatingsystem == 'centos':
                os.system("sudo sed -i 's/enforcing/disabled/g' " + localtempdir + '/temp/etc/selinux/config')
            if ldap:
                self.configure_ldap(localtempdir)
        return stat

    def nimbus_method(self, localtempdir, ldap):
        stat = 0
        self.logger.debug('kernel: ' + self.kernel)
        if self.kernel == 'None':
            self.kernel = self.default_nimbus_kernel
        self.logger.info('Retrieving kernel ' + self.kernel)
        stat = self.runCmd('wget ' + self.http_server + 'kernel/' + self.kernel + '.modules.tar.gz -O ' + localtempdir + '/' + self.kernel + '.modules.tar.gz')
        if stat == 0:
            self.runCmd('sudo tar xfz ' + localtempdir + '/' + self.kernel + '.modules.tar.gz --directory ' + localtempdir + '/temp/lib/modules/')
            self.logger.info('Injected kernel ' + self.kernel)
            fstab = '\n# Default fstab\n /dev/sda1       /             ext3     defaults,errors=remount-ro 0 0\n proc            /proc         proc     defaults                   0 0\n devpts          /dev/pts      devpts   gid=5,mode=620             0 0\n '
            f = open(localtempdir + '/fstab', 'w')
            f.write(fstab)
            f.close()
            self.runCmd('sudo mv -f ' + localtempdir + '/fstab ' + localtempdir + '/temp/etc/fstab')
            self.runCmd('sudo chown root:root ' + localtempdir + '/temp/etc/fstab')
            self.logger.info('fstab Injected')
            if self.operatingsystem == 'centos':
                os.system("sudo sed -i 's/enforcing/disabled/g' " + localtempdir + '/temp/etc/selinux/config')
            os.system('sudo mkdir -p ' + localtempdir + '/temp/root/.ssh')
            if ldap:
                self.configure_ldap(localtempdir)
        return stat

    def openstack_method(self, localtempdir, ldap):
        self.logger.debug('kernel: ' + self.kernel)
        if self.kernel == 'None':
            self.kernel = self.default_openstack_kernel
        self.logger.info('Retrieving kernel ' + self.kernel)
        self.runCmd('wget ' + self.http_server + 'kernel/' + self.kernel + '.modules.tar.gz -O ' + localtempdir + '/' + self.kernel + '.modules.tar.gz')
        self.runCmd('sudo tar xfz ' + localtempdir + '/' + self.kernel + '.modules.tar.gz --directory ' + localtempdir + '/temp/lib/modules/')
        self.logger.info('Injected kernel ' + self.kernel)
        fstab = '\n# Default fstab\n /dev/sda1       /             ext3     defaults,errors=remount-ro 0 0\n proc            /proc         proc     defaults                   0 0\n devpts          /dev/pts      devpts   gid=5,mode=620             0 0\n '
        f = open(localtempdir + '/fstab', 'w')
        f.write(fstab)
        f.close()
        self.runCmd('sudo mv -f ' + localtempdir + '/fstab ' + localtempdir + '/temp/etc/fstab')
        self.runCmd('sudo chown root:root ' + localtempdir + '/temp/etc/fstab')
        self.logger.info('fstab Injected')
        if self.operatingsystem == 'ubuntu':
            self.runCmd('sudo chroot ' + localtempdir + '/temp/ apt-get -y install curl cloud-init')
            cloud_cfg = '\ncloud_type: auto\nuser: root\ndisable_root: 0\npreserve_hostname: False\n'
            f = open(localtempdir + '/cloud.cfg', 'w')
            f.write(cloud_cfg)
            f.close()
            self.runCmd('sudo mv -f ' + localtempdir + '/cloud.cfg ' + localtempdir + '/temp/etc/cloud/cloud.cfg')
            self.runCmd('sudo chown root:root ' + localtempdir + '/temp/etc/cloud/cloud.cfg')
        elif self.operatingsystem == 'centos':
            rc_local = '         \nroute del -net 169.254.0.0 netmask 255.255.0.0 dev eth0\n# load pci hotplug for dynamic disk attach in KVM (for EBS)\ndepmod -a\nmodprobe acpiphp\n\n# simple attempt to get the user ssh key using the meta-data service\nmkdir -p /root/.ssh\necho >> /root/.ssh/authorized_keys\ncurl -m 10 -s http://169.254.169.254/latest/meta-data/public-keys/0/openssh-key | grep \'ssh-rsa\' >> /root/.ssh/authorized_keys\necho "AUTHORIZED_KEYS:"\necho "************************"\ncat /root/.ssh/authorized_keys\necho "************************"\n'
            f_org = open(localtempdir + '/temp/etc/rc.local', 'r')
            f = open(localtempdir + '/rc.local', 'w')
            write_remain = False
            for line in f_org:
                if re.search('^#', line) or write_remain:
                    f.write(line)
                else:
                    f.write(rc_local)
                    write_remain = True

            f.close()
            f_org.close()
            self.runCmd('sudo mv -f ' + localtempdir + '/rc.local ' + localtempdir + '/temp/etc/rc.local')
            self.runCmd('sudo chroot ' + localtempdir + '/temp/ cp -f /etc/rc.local /etc/rc3.d/../')
            self.runCmd('sudo chown root:root ' + localtempdir + '/temp/etc/rc.local')
            self.runCmd('sudo chmod 755 ' + localtempdir + '/temp/etc/rc.local')
            cmd = 'echo "NOZEROCONF=yes" | sudo tee -a ' + localtempdir + '/temp/etc/sysconfig/network > /dev/null'
            self.logger.debug(cmd)
            os.system(cmd)
            self.runCmd('sudo chroot ' + localtempdir + '/temp/ yum -y install curl')
        if ldap:
            self.configure_ldap(localtempdir)

    def opennebula_method(self, localtempdir, ldap):
        self.logger.debug('kernel: ' + self.kernel)
        self.runCmd('sudo wget ' + self.http_server + '/opennebula/' + self.operatingsystem + '/vmcontext.sh -O ' + localtempdir + '/temp/etc/init.d/vmcontext.sh')
        self.runCmd('sudo chmod +x ' + localtempdir + '/temp/etc/init.d/vmcontext.sh')
        self.runCmd('sudo chown root:root ' + localtempdir + '/temp/etc/rc.local')
        device = 'sda'
        rc_local = ''
        if self.operatingsystem == 'ubuntu':
            self.runCmd('sudo sudo chroot ' + localtempdir + '/temp ln -s /etc/init.d/vmcontext.sh /etc/rc2.d/S01vmcontext.sh')
            device = 'sda'
            rc_local = 'mount -t iso9660 /dev/sr0 /mnt \n'
            self.runCmd('sudo rm -f ' + localtempdir + '/temp/etc/udev/rules.d/70-persistent-net.rules')
            if self.kernel == 'None':
                self.kernel = self.default_opennebula_kernel
        elif self.operatingsystem == 'centos':
            self.runCmd('sudo chroot ' + localtempdir + '/temp chkconfig --add vmcontext.sh')
            if self.version == '5':
                device = 'hda'
                rc_local = 'mount -t iso9660 /dev/hdc /mnt \n'
            elif self.version == '6':
                device = 'sda'
                rc_local = 'mount -t iso9660 /dev/sr0 /mnt \n'
                self.runCmd('sudo rm -f ' + localtempdir + '/temp/etc/udev/rules.d/70-persistent-net.rules')
            os.system("sudo sed -i 's/enforcing/disabled/g' " + localtempdir + '/temp/etc/selinux/config')
            if self.kernel == 'None':
                self.kernel = self.default_opennebula_kernel
        self.logger.info('Retrieving kernel ' + self.kernel)
        self.runCmd('wget ' + self.http_server + 'kernel/' + self.kernel + '.modules.tar.gz -O ' + localtempdir + '/' + self.kernel + '.modules.tar.gz')
        self.runCmd('sudo tar xfz ' + localtempdir + '/' + self.kernel + '.modules.tar.gz --directory ' + localtempdir + '/temp/lib/modules/')
        self.logger.info('Injected kernel ' + self.kernel)
        rc_local += 'if [ -f /mnt/context.sh ]; then \n'
        rc_local += '      . /mnt/init.sh \n'
        rc_local += 'fi \n'
        rc_local += 'umount /mnt \n\n'
        f_org = open(localtempdir + '/temp/etc/rc.local', 'r')
        f = open(localtempdir + '/rc.local', 'w')
        write_remain = False
        for line in f_org:
            if re.search('^#', line) or write_remain:
                f.write(line)
            else:
                f.write(rc_local)
                write_remain = True

        f.close()
        f_org.close()
        self.runCmd('sudo mv -f ' + localtempdir + '/rc.local ' + localtempdir + '/temp/etc/rc.local')
        self.runCmd('sudo chown root:root ' + localtempdir + '/temp/etc/rc.local')
        self.runCmd('sudo chmod 755 ' + localtempdir + '/temp/etc/rc.local')
        os.system('sudo chroot ' + localtempdir + '/temp/ cp -f /etc/rc.local /etc/rc3.d/../')
        fstab = '# Default fstab \n '
        fstab += '/dev/' + device + '       /             ext3     defaults,errors=remount-ro 0 0 \n'
        fstab += 'proc            /proc         proc     defaults                   0 0 \n'
        fstab += 'devpts          /dev/pts      devpts   gid=5,mode=620             0 0 \n'
        f = open(localtempdir + '/fstab', 'w')
        f.write(fstab)
        f.close()
        self.runCmd('sudo mv -f ' + localtempdir + '/fstab ' + localtempdir + '/temp/etc/fstab')
        self.runCmd('sudo chown root:root ' + localtempdir + '/temp/etc/fstab')
        self.logger.info('fstab Injected')

    def handle_image(self, image, localtempdir, connstream):
        success = True
        realnameimg = ''
        self.logger.info('untar file with image and manifest')
        cmd = 'tar xvfz ' + image + ' -C ' + localtempdir
        self.logger.debug(cmd)
        p = Popen(cmd.split(' '), stdout=PIPE, stderr=PIPE)
        std = p.communicate()
        stat = 0
        if len(std[0]) > 0:
            realnameimg = std[0].split('\n')[0].strip().split('.')[0]
        if p.returncode != 0:
            self.logger.error('Command: ' + cmd + ' failed, status: ' + str(p.returncode) + ' --- ' + std[1])
            stat = 1
        cmd = 'rm -f ' + image
        status = self.runCmd(cmd)
        if stat != 0:
            msg = 'ERROR: the files were not extracted'
            self.errormsg(connstream, msg)
            return False
        self.manifestname = realnameimg + '.manifest.xml'
        manifestfile = open(localtempdir + '/' + self.manifestname, 'r')
        manifest = parse(manifestfile)
        self.name = ''
        self.givenname = ''
        self.operatingsystem = ''
        self.version = ''
        self.arch = ''
        self.name = manifest.getElementsByTagName('name')[0].firstChild.nodeValue.strip()
        self.givenname = manifest.getElementsByTagName('givenname')
        self.operatingsystem = manifest.getElementsByTagName('os')[0].firstChild.nodeValue.strip()
        self.version = manifest.getElementsByTagName('version')[0].firstChild.nodeValue.strip()
        self.arch = manifest.getElementsByTagName('arch')[0].firstChild.nodeValue.strip()
        self.logger.debug(self.name + ' ' + self.operatingsystem + ' ' + self.version + ' ' + self.arch)
        cmd = 'mkdir -p ' + localtempdir + '/temp'
        status = self.runCmd(cmd)
        if status != 0:
            msg = 'ERROR: creating temp directory inside ' + localtempdir
            self.errormsg(connstream, msg)
            return False
        cmd = 'sudo mount -o loop ' + localtempdir + '/' + self.name + '.img ' + localtempdir + '/temp'
        status = self.runCmd(cmd)
        if status != 0:
            msg = 'ERROR: mounting image'
            self.errormsg(connstream, msg)
            return False
        return True

    def errormsg(self, connstream, msg):
        self.logger.error(msg)
        try:
            connstream.write(msg)
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            self.logger.debug('In errormsg: ' + str(sys.exc_info()))

        self.logger.info('Image Register Request DONE')

    def runCmd(self, cmd):
        cmdLog = logging.getLogger('RegisterIaaS.' + str(os.getpid()) + '.exec')
        cmdLog.debug(cmd)
        p = Popen(cmd.split(' '), stdout=PIPE, stderr=PIPE)
        std = p.communicate()
        status = 0
        if len(std[0]) > 0:
            cmdLog.debug('stdout: ' + std[0])
            cmdLog.debug('stderr: ' + std[1])
        if p.returncode != 0:
            cmdLog.error('Command: ' + cmd + ' failed, status: ' + str(p.returncode) + ' --- ' + std[1])
            status = 1
        return status


def main():
    server = IMRegisterServerIaaS()
    server.start()


if __name__ == '__main__':
    main()