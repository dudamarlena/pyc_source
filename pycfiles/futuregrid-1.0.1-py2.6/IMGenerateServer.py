# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/management/IMGenerateServer.py
# Compiled at: 2012-09-06 11:03:15
"""
Server that manage the image generation by provisioning VM and interacting with IMGenerateScript
"""
__author__ = 'Javier Diaz'
from types import *
import re, logging, logging.handlers, random, os, sys, socket, ssl
from multiprocessing import Process
from subprocess import *
from xml.dom.minidom import Document, parseString
import xmlrpclib, time
from futuregrid.image.management.IMServerConf import IMServerConf
from futuregrid.image.repository.client.IRServiceProxy import IRServiceProxy
from futuregrid.utils.FGTypes import FGCredential
from futuregrid.utils import FGAuth

class IMGenerateServer(object):

    def __init__(self):
        super(IMGenerateServer, self).__init__()
        self.rootId = 'root'
        self.numparams = 13
        self.user = ''
        self.os = ''
        self.version = ''
        self.arch = ''
        self.software = ''
        self.givenname = ''
        self.desc = ''
        self.getimg = False
        self.baseimage = False
        self.nocache = False
        self.size = 1.5
        self._genConf = IMServerConf()
        self._genConf.load_generateServerConfig()
        self.port = self._genConf.getGenPort()
        self.proc_max = self._genConf.getProcMax()
        self.refresh_status = self._genConf.getRefreshStatus()
        self.wait_max = self._genConf.getWaitMax()
        self._nopasswdusers = self._genConf.getNoPasswdUsersGen()
        self.vmfile_centos = self._genConf.getVmFileCentos()
        self.vmfile_rhel = self._genConf.getVmFileRhel()
        self.vmfile_ubuntu = self._genConf.getVmFileUbuntu()
        self.vmfile_debian = self._genConf.getVmFileDebian()
        self.xmlrpcserver = self._genConf.getXmlRpcServer()
        self.bridge = self._genConf.getBridge()
        self.serverdir = os.path.expanduser(os.path.dirname(__file__))
        self.addrnfs = self._genConf.getAddrNfs()
        self.tempdirserver = self._genConf.getTempDirServerGen()
        self.tempdir = self._genConf.getTempDirGen()
        self.http_server = self._genConf.getHttpServerGen()
        self.oneauth = self._genConf.getOneUser() + ':' + self._genConf.getOnePass()
        self.log_filename = self._genConf.getLogGen()
        self.logLevel = self._genConf.getLogLevelGen()
        self.logger = self.setup_logger()
        self._ca_certs = self._genConf.getCaCertsGen()
        self._certfile = self._genConf.getCertFileGen()
        self._keyfile = self._genConf.getKeyFileGen()
        print '\nReading Configuration file from ' + self._genConf.getConfigFile() + '\n'
        verbose = False
        printLogStdout = False
        self._reposervice = IRServiceProxy(verbose, printLogStdout)

    def setup_logger(self):
        logger = logging.getLogger('GenerateServer')
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
                proc_list.append(Process(target=self.generate, args=(connstream, fromaddr[0])))
                proc_list[(len(proc_list) - 1)].start()
            except ssl.SSLError:
                self.logger.error('Unsuccessful connection attempt from: ' + repr(fromaddr))
                self.logger.info('Image Generation Request DONE')
            except socket.error:
                self.logger.error('Error with the socket connection')
                self.logger.info('Image Generation Request DONE')
            except:
                self.logger.error('Uncontrolled Error: ' + str(sys.exc_info()))
                try:
                    connstream.shutdown(socket.SHUT_RDWR)
                    connstream.close()
                except:
                    pass
                else:
                    self.logger.info('Image Generation Request DONE')

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

    def generate(self, channel, fromaddr):
        start_all = time.time()
        self.logger = logging.getLogger('GenerateServer.' + str(os.getpid()))
        self.logger.info('Processing an image generation request')
        data = channel.read(2048)
        self.logger.debug('received data: ' + data)
        params = data.split('|')
        self.user = params[0].strip()
        self.os = params[1].strip()
        self.version = params[2].strip()
        self.arch = params[3].strip()
        self.software = params[4].strip()
        self.givenname = params[5].strip()
        self.desc = params[6].strip()
        self.getimg = eval(params[7].strip())
        passwd = params[8].strip()
        passwdtype = params[9].strip()
        self.baseimage = eval(params[10].strip())
        self.nocache = eval(params[11].strip())
        self.size = eval(params[12].strip())
        if len(params) != self.numparams:
            msg = 'ERROR: incorrect message'
            self.errormsg(channel, msg)
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
                            channel.write('OK')
                        else:
                            if userstatus == 'NoActive':
                                channel.write('NoActive')
                                msg = 'ERROR: The user ' + self.user + ' is not active'
                                self.errormsg(channel, msg)
                                return
                            else:
                                if userstatus == 'NoUser':
                                    channel.write('NoUser')
                                    msg = 'ERROR: The user ' + self.user + ' does not exist'
                                    self.logger.error(msg)
                                    self.logger.info('Image Generation Request DONE')
                                    return
                                channel.write('Could not connect with image repository server')
                                msg = 'ERROR: Could not connect with image repository server to verify the user status'
                                self.logger.error(msg)
                                self.logger.info('Image Generation Request DONE')
                                return
                        endloop = True
                    else:
                        retry += 1
                        if retry < maxretry:
                            channel.write('TryAuthAgain')
                            passwd = channel.read(2048)
                        else:
                            msg = 'ERROR: authentication failed'
                            endloop = True
                            self.errormsg(channel, msg)
                            return
                else:
                    channel.write('OK')
                    endloop = True

            baseimageuri = None
            if not self.nocache and not self.baseimage:
                start = time.time()
                baseimageuri = self.findBaseImage(passwd)
                end = time.time()
                self.logger.info('TIME to retrieve and uncompress a base image from the repo:' + str(end - start))
            if baseimageuri == None:
                self.genInVM(channel, passwd)
            else:
                self.genLocal(channel, passwd, baseimageuri)
            end_all = time.time()
            self.logger.info('TIME walltime image generate:' + str(end_all - start_all))
            self.logger.info('Image Generation DONE')
            return

    def genLocal(self, channel, passwd, baseimageuri):
        options = '-a ' + self.arch + ' -o ' + self.os + ' -v ' + self.version + ' -u ' + self.user + ' -t ' + self.tempdirserver + ' --size ' + str(self.size)
        if type(self.givenname) is not NoneType:
            options += ' -n ' + self.givenname
        if type(self.desc) is not NoneType:
            options += ' -e ' + self.desc
        if type(self.software) is not NoneType:
            options += ' -s ' + self.software
        if baseimageuri != None:
            options += ' -i ' + baseimageuri
        if self.baseimage:
            options += ' -b '
        options += ' -c ' + self.http_server + ' -l ' + self.tempdirserver + '/' + str(os.getpid()) + '_gen_cache.log'
        cmdexec = '/usr/bin/python ' + self.serverdir + '/IMGenerateScript.py ' + options
        self.logger.info(cmdexec)
        start = time.time()
        cmd = 'sudo ' + cmdexec
        self.logger.debug(cmd)
        p = Popen(cmd.split(' '), stdout=PIPE, stderr=PIPE)
        std = p.communicate()
        end = time.time()
        self.logger.info('TIME generate image:' + str(end - start))
        if p.returncode != 0:
            self.logger.error('Command: ' + cmd + ' failed, status: ' + str(p.returncode) + ' --- ' + std[1])
        status = std[0].strip()
        self.logger.debug('status returned generate script|' + status + '|')
        if os.path.isfile(self.tempdirserver + '/' + status + '.img') and os.path.isfile(self.tempdirserver + '/' + status + '.manifest.xml'):
            self.compressUploadSend(status, channel, passwd)
        else:
            msg = 'ERROR: ' + str(std[1])
            self.errormsg(channel, msg)
        return

    def genInVM(self, channel, passwd):
        vmfile = ''
        vmID = 0
        destroyed = False
        if self.os == 'ubuntu':
            vmfile = self.vmfile_ubuntu
        elif self.os == 'debian':
            vmfile = self.vmfile_debian
        elif self.os == 'rhel':
            vmfile = self.vmfile_rhel
        elif self.os == 'centos':
            vmfile = self.vmfile_centos[self.version]
        try:
            server = xmlrpclib.ServerProxy(self.xmlrpcserver)
        except:
            self.logger.error('Error connection with OpenNebula ' + str(sys.exc_info()))
            return
        else:
            start = time.time()
            output = self.boot_VM(server, vmfile)
            end = time.time()
            self.logger.info('TIME boot VM:' + str(end - start))
            vmaddr = output[0]
            vmID = output[1]
            if vmaddr != 'fail':
                self.logger.info('The VM deployed is in ' + vmaddr)
                self.logger.info('Mount scratch directory in the VM')
                cmd = 'ssh -q -oBatchMode=yes ' + self.rootId + '@' + vmaddr
                cmdmount = ' mount -t nfs ' + self.addrnfs + ':' + self.tempdirserver + ' ' + self.tempdir
                self.logger.info(cmd + cmdmount)
                stat = os.system(cmd + cmdmount)
                if stat == 0:
                    self.logger.info('Sending IMGenerateScript.py to the VM')
                    cmdscp = 'scp -q -oBatchMode=yes ' + self.serverdir + '/IMGenerateScript.py  ' + self.rootId + '@' + vmaddr + ':/root/'
                    self.logger.info(cmdscp)
                    stat = os.system(cmdscp)
                    if stat != 0:
                        msg = 'ERROR: sending IMGenerateScript.py to the VM. Exit status ' + str(stat)
                        self.errormsg(channel, msg)
                    else:
                        options = '-a ' + self.arch + ' -o ' + self.os + ' -v ' + self.version + ' -u ' + self.user + ' -t ' + self.tempdir + ' --size ' + str(self.size)
                        if type(self.givenname) is not NoneType:
                            options += ' -n ' + self.givenname
                        if type(self.desc) is not NoneType:
                            options += ' -e ' + self.desc
                        if type(self.software) is not NoneType:
                            options += ' -s ' + self.software
                        if self.baseimage:
                            options += ' -b '
                        options += ' -c ' + self.http_server
                        cmdexec = " -q '/usr/bin/python /root/IMGenerateScript.py " + options + " '"
                        self.logger.info(cmdexec)
                        start = time.time()
                        uid = self._rExec(self.rootId, cmdexec, vmaddr)
                        self.logger.debug('Returned from script execution' + str(uid))
                        end = time.time()
                        self.logger.info('TIME generate image:' + str(end - start))
                        self.logger.info('copying fg-image-generate.log to scrach partition ' + self.tempdirserver + '/' + str(vmID) + '_gen.log')
                        cmdscp = 'scp -q -oBatchMode=yes ' + self.rootId + '@' + vmaddr + ':/root/fg-image-generate.log ' + self.tempdirserver + '/' + str(vmID) + '_gen.log'
                        os.system(cmdscp)
                        status = uid[0].strip()
                        if 'error' in uid:
                            msg = 'ERROR: ' + str(uid[1])
                            self.errormsg(channel, msg)
                        else:
                            self.logger.info('Umount scratch directory in the VM')
                            cmd = 'ssh -q -oBatchMode=yes ' + self.rootId + '@' + vmaddr
                            cmdmount = ' umount ' + self.tempdir + ' 2>/dev/null'
                            start = time.time()
                            max_retry = 15
                            retry_done = 0
                            umounted = False
                            while not umounted:
                                self.logger.debug(cmd + cmdmount)
                                stat = os.system(cmd + cmdmount)
                                if stat == 0:
                                    umounted = True
                                elif retry_done == max_retry:
                                    self.logger.debug('exit status ' + str(stat))
                                    umounted = True
                                    self.logger.error('Problems to umount the image. Exit status ' + str(stat))
                                else:
                                    retry_done += 1
                                    time.sleep(5)

                            end = time.time()
                            self.logger.info('TIME umount image:' + str(end - start))
                            self.logger.info('Destroy VM')
                            server.one.vm.action(self.oneauth, 'finalize', vmID)
                            destroyed = True
                            self.compressUploadSend(status, channel, passwd)
            else:
                msg = 'ERROR: booting VM'
                self.errormsg(channel, msg)
            if not destroyed and vmID != -1:
                self.logger.info('Destroy VM')
            else:
                try:
                    server.one.vm.action(self.oneauth, 'finalize', vmID)
                except:
                    msg = 'ERROR: finalizing VM'
                    self.errormsg(channel, msg)

    def compressUploadSend(self, status, channel, passwd):
        self.logger.debug('Generating tgz with image and manifest files')
        self.logger.debug('tar cfz ' + self.tempdirserver + '/' + status + '.tgz -C ' + self.tempdirserver + ' ' + status + '.manifest.xml ' + status + '.img')
        start = time.time()
        out = os.system('tar cfz ' + self.tempdirserver + '/' + status + '.tgz -C ' + self.tempdirserver + ' ' + status + '.manifest.xml ' + status + '.img')
        end = time.time()
        self.logger.info('TIME tgz image:' + str(end - start))
        os.system('rm -f ' + self.tempdirserver + '' + status + '.manifest.xml ' + self.tempdirserver + '' + status + '.img')
        if out != 0:
            msg = 'ERROR: generating compressed file with the image and manifest'
            self.errormsg(channel, msg)
            return
        if self.getimg:
            channel.write(self.tempdirserver + '' + status + '.tgz')
            self.logger.info('Waiting until the client retrieve the image')
            channel.read()
            channel.shutdown(socket.SHUT_RDWR)
            channel.close()
        else:
            status_repo = ''
            error_repo = False
            try:
                if not self._reposervice.connection():
                    msg = 'ERROR: Connection with the Image Repository failed'
                    self.errormsg(channel, msg)
                else:
                    self.logger.info('Storing image ' + self.tempdirserver + '/' + status + '.tgz' + ' in the repository')
                    start = time.time()
                    if self.baseimage:
                        status_repo = self._reposervice.put(self.user, passwd, self.user, self.tempdirserver + '' + status + '.tgz', 'os=' + self.os + '_' + self.version + '&arch=' + self.arch + '&description=' + self.desc + '&tag=' + status + ',BaseImage')
                    else:
                        status_repo = self._reposervice.put(self.user, passwd, self.user, self.tempdirserver + '' + status + '.tgz', 'os=' + self.os + '_' + self.version + '&arch=' + self.arch + '&description=' + self.desc + '&tag=' + status)
                    end = time.time()
                    self.logger.info('TIME upload image to the repo:' + str(end - start))
                    success = True
                    if re.search('^ERROR', status_repo):
                        self.errormsg(channel, status_repo)
                    else:
                        channel.write(str(status_repo))
                        channel.shutdown(socket.SHUT_RDWR)
                        channel.close()
                    self._reposervice.disconnect()
            except:
                msg = 'ERROR: uploading image to the repository. ' + str(sys.exc_info())
                self.errormsg(channel, msg)

            os.system('rm -f ' + self.tempdirserver + '' + status + '.tgz')

    def findBaseImage(self, passwd):
        baseimageuri = None
        try:
            if not self._reposervice.connection():
                msg = 'ERROR: Connection with the Image Repository failed'
                self.logger.error(msg)
            else:
                self.logger.info('Find Base Image os=' + self.os + ',version=' + self.version + ',arch=' + self.arch + ' in the repository')
                imgsList = None
                imgsList = self._reposervice.query(self.user, passwd, self.user, '* where os=' + self.os + '_' + self.version + ',arch=' + self.arch + ',tag=BaseImage,imgStatus=available')
                self._reposervice.disconnect()
                baseImageId = ''
                if imgsList != None:
                    try:
                        imgs = eval(imgsList)
                        for key in imgs.keys():
                            imageproperties = imgs[key].split(', ')
                            tempbaseImageId = imageproperties[0].split('=')[1]
                            if imageproperties[3].split('=')[1].strip() == self.user:
                                baseImageId = tempbaseImageId
                                break
                            elif imageproperties[8].split('=')[1].strip() == 'public':
                                if baseImageId == '':
                                    baseImageId = tempbaseImageId

                    except:
                        self.logger.error('findbaseimage:Server replied: ' + str(imgsList))
                        self.logger.error('findbaseimage: Error interpreting the list of images from Image Repository' + str(sys.exc_info()))
                    else:
                        if baseImageId != '':
                            if not self._reposervice.connection():
                                msg = 'ERROR: Connection with the Image Repository failed'
                                self.logger.error(msg)
                            else:
                                random.seed()
                                exists = True
                                while exists:
                                    randid = str(random.getrandbits(64))
                                    path = self.tempdirserver + '/' + randid
                                    if not os.path.isdir(path):
                                        exists = False

                                os.system('mkdir ' + path)
                                baseimageuri = self._reposervice.get(self.user, passwd, self.user, 'img', baseImageId, path)
                                self._reposervice.disconnect()
                        else:
                            self.logger.debug('No Base Image found')
                else:
                    self.logger.info('No Base Image found')
        except:
            msg = 'ERROR: searching for a base image in the repository. ' + str(sys.exc_info())
            self.logger.error(msg)

        if baseimageuri != None:
            baseimageuri = self.process_baseimage(baseimageuri, randid)
            self.logger.debug('Inside the VM, the image will be in: ' + str(baseimageuri))
        return baseimageuri

    def process_baseimage(self, baseimageuri, randid):
        pathimg = None
        realnameimg = ''
        self.logger.info('untar file with image and manifest')
        cmd = 'tar xvfz ' + baseimageuri + ' -C ' + os.path.dirname(baseimageuri)
        self.logger.debug(cmd)
        p = Popen(cmd.split(' '), stdout=PIPE, stderr=PIPE)
        std = p.communicate()
        stat = 0
        if len(std[0]) > 0:
            realnameimg = std[0].split('\n')[0].strip().split('.')[0]
        if p.returncode != 0:
            self.logger.error('Command: ' + cmd + ' failed, status: ' + str(p.returncode) + ' --- ' + std[1])
            stat = 1
        cmd = 'rm -f ' + baseimageuri
        os.system(cmd)
        if stat != 0:
            msg = 'ERROR: Extracting Base Image: ' + str(sys.exc_info())
            self.logger.error(msg)
            cmd = 'rm -rf ' + os.path.basename(baseimageuri)
            os.system(cmd)
        else:
            pathimg = self.tempdirserver + '/' + randid + '/' + realnameimg + '.img'
        return pathimg

    def errormsg(self, channel, msg):
        self.logger.error(msg)
        try:
            channel.write(msg)
            channel.shutdown(socket.SHUT_RDWR)
            channel.close()
        except:
            self.logger.debug('In errormsg: ' + str(sys.exc_info()))

        self.logger.info('Image Generation DONE')

    def boot_VM(self, server, vmfile):
        """
        It will boot a VM using XMLRPC API for OpenNebula
        
        from lib/ruby/OpenNebula/VirtualMachine.rb
        index start in 0
        
        VM_STATE=%w{INIT PENDING HOLD ACTIVE STOPPED SUSPENDED DONE FAILED}
        LCM_STATE=%w{LCM_INIT PROLOG BOOT RUNNING MIGRATE SAVE_STOP SAVE_SUSPEND
        SAVE_MIGRATE PROLOG_MIGRATE PROLOG_RESUME EPILOG_STOP EPILOG
        SHUTDOWN CANCEL FAILURE CLEANUP UNKNOWN}
        """
        vmaddr = ''
        fail = False
        s = open(os.path.expanduser(vmfile), 'r').read()
        try:
            vm = server.one.vm.allocate(self.oneauth, s)
        except:
            msg = 'ERROR: Trying to allocate a VM'
            self.logger.error(msg)
            return ['fail', -1]
        else:
            if vm[0]:
                self.logger.debug('VM ID: ' + str(vm[1]))
                booted = False
                maxretry = self.wait_max / 5
                retry = 0
                while not booted and retry < maxretry:
                    try:
                        vminfo = server.one.vm.info(self.oneauth, vm[1])
                        manifest = parseString(vminfo[1])
                        vm_status = manifest.getElementsByTagName('STATE')[0].firstChild.nodeValue.strip()
                        if vm_status == '3':
                            lcm_status = manifest.getElementsByTagName('LCM_STATE')[0].firstChild.nodeValue.strip()
                            if lcm_status == '3':
                                booted = True
                        elif vm_status == '7':
                            self.logger.error('Fail to deploy VM ' + str(vm[1]))
                            booted = True
                            fail = True
                            vmaddr = 'fail'
                        elif vm_status == '6':
                            self.logger.error('The status of the VM ' + str(vm[1]) + ' is DONE')
                            booted = True
                            fail = True
                            vmaddr = 'fail'
                        else:
                            retry += 1
                            time.sleep(5)
                    except:
                        pass

                if retry >= maxretry:
                    self.logger.error('The VM ' + str(vm[1]) + ' did not change to runn status. Please verify that the status of the OpenNebula hosts or increase the wait time in the configuration file (max_wait) \n')
                    vmaddr = 'fail'
                    fail = True
                if not fail:
                    nics = manifest.getElementsByTagName('NIC')
                    for i in range(len(nics)):
                        if nics[i].childNodes[0].firstChild.nodeValue.strip() == self.bridge:
                            vmaddr = nics[i].childNodes[1].firstChild.nodeValue.strip()

                    if vmaddr.strip() != '':
                        self.logger.debug('IP of the VM ' + str(vm[1]) + ' is ' + str(vmaddr))
                        access = False
                        maxretry = 240
                        retry = 0
                        self.logger.debug('Waiting to have access to VM')
                        while not access and retry < maxretry:
                            cmd = 'ssh -q -oBatchMode=yes root@' + vmaddr + ' uname'
                            p = Popen(cmd, shell=True, stdout=PIPE)
                            status = os.waitpid(p.pid, 0)[1]
                            if status == 0:
                                access = True
                                self.logger.debug('The VM ' + str(vm[1]) + ' with ip ' + str(vmaddr) + 'is accessible')
                            else:
                                retry += 1
                                time.sleep(5)

                        if retry >= maxretry:
                            self.logger.error('Could not get access to the VM ' + str(vm[1]) + ' with ip ' + str(vmaddr) + '\nPlease verify the OpenNebula templates to make sure that the public ssh key to be injected is accessible to the oneadmin user. \nAlso verify that the VM has ssh server and is active on boot.')
                            vmaddr = 'fail'
                    else:
                        self.logger.error('Could not determine the IP of the VM ' + str(vm[1]) + ' for the bridge ' + self.bridge)
                        vmaddr = 'fail'
            else:
                vmaddr = 'fail'

        return [
         vmaddr, vm[1]]

    def _rExec(self, userId, cmdexec, vmaddr):
        random.seed()
        randid = str(random.getrandbits(32))
        cmdssh = 'ssh -oBatchMode=yes ' + userId + '@' + vmaddr
        tmpFile = '/tmp/' + str(time.time()) + str(randid)
        cmdexec = cmdexec + ' > ' + tmpFile
        cmd = cmdssh + cmdexec
        self.logger.info(str(cmd))
        stat = os.system(cmd)
        if str(stat) != '0':
            self.logger.info(str(stat))
        f = open(tmpFile, 'r')
        outputs = f.readlines()
        f.close()
        os.system('rm -f ' + tmpFile)
        return outputs


def main():
    imgenserver = IMGenerateServer()
    imgenserver.start()


if __name__ == '__main__':
    main()