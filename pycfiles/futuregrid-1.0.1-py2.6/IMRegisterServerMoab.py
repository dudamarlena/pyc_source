# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/management/IMRegisterServerMoab.py
# Compiled at: 2012-09-06 11:03:15
"""
xCAT image register server that DO REGISTER AN IMAGE IN MOAB.
"""
__author__ = 'Javier Diaz, Andrew Younge'
from subprocess import *
import logging, logging.handlers, os, re, socket, ssl, sys, time
from futuregrid.image.management.IMServerConf import IMServerConf

class IMRegisterServerMoab(object):

    def __init__(self):
        super(IMRegisterServerMoab, self).__init__()
        self.numparams = 5
        self.prefix = ''
        self.name = ''
        self.operatingsystem = ''
        self.arch = ''
        self.machine = ''
        self._registerConf = IMServerConf()
        self._registerConf.load_registerServerMoabConfig()
        self.port = self._registerConf.getMoabPort()
        self.moabInstallPath = self._registerConf.getMoabInstallPath()
        self.log_filename = self._registerConf.getLogMoab()
        self.logLevel = self._registerConf.getLogLevelMoab()
        self._ca_certs = self._registerConf.getCaCertsMoab()
        self._certfile = self._registerConf.getCertFileMoab()
        self._keyfile = self._registerConf.getKeyFileMoab()
        print '\nReading Configuration file from ' + self._registerConf.getConfigFile() + '\n'
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('RegisterMoab')
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
        while True:
            (newsocket, fromaddr) = sock.accept()
            connstream = 0
            try:
                try:
                    connstream = ssl.wrap_socket(newsocket, server_side=True, ca_certs=self._ca_certs, cert_reqs=ssl.CERT_REQUIRED, certfile=self._certfile, keyfile=self._keyfile, ssl_version=ssl.PROTOCOL_TLSv1)
                    self.process_client(connstream)
                except ssl.SSLError:
                    self.logger.error('Unsuccessful connection attempt from: ' + repr(fromaddr))

            finally:
                if connstream is ssl.SSLSocket:
                    connstream.shutdown(socket.SHUT_RDWR)
                    connstream.close()

    def process_client(self, connstream):
        self.logger.info('Accepted new connection')
        data = connstream.read(2048)
        params = data.split(',')
        self.prefix = params[0]
        self.name = params[1]
        self.operatingsystem = params[2]
        self.arch = params[3]
        self.machine = params[4]
        if len(params) != self.numparams:
            msg = 'ERROR: incorrect message'
            self.errormsg(connstream, msg)
            return
        if self.prefix == 'list':
            moabimageslist = ''
            f = open(self.moabInstallPath + '/tools/msm/images.txt')
            for i in f:
                if not re.search('^#', i):
                    moabimageslist += i.split()[0] + ','

            moabimageslist = moabimageslist.rstrip(',')
            self.logger.debug('Moab image list: ' + moabimageslist)
            connstream.write(moabimageslist)
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
            self.logger.info('Image Register Moab (list) DONE')
        elif self.prefix == 'infosites':
            self.logger.debug('Information Moab Site: ' + str(self.machine))
            connstream.write('True')
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
            self.logger.info('Image Register Moab (info sites) DONE')
        elif self.prefix == 'remove':
            self.logger.debug('Remove image from Moab')
            cmd = "sudo sed -i '/^" + self.name + "/d' /opt/moab/tools/msm/images.txt"
            self.logger.info(cmd)
            status = os.system(cmd)
            if status != 0:
                msg = 'ERROR: removing image from image.txt file'
                self.logger.debug(msg)
                self.errormsg(connstream, msg)
                return
            connstream.write('OK')
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
            cmd = 'sudo ' + self.moabInstallPath + '/bin/mschedctl -R'
            self.runCmd(cmd)
            self.logger.info('Image Register Moab DONE')
        else:
            moabstring = ''
            if self.machine == 'minicluster':
                moabstring = 'echo "' + self.prefix + self.operatingsystem + '' + self.name + ' ' + self.arch + ' ' + self.prefix + self.operatingsystem + '' + self.name + ' compute netboot" | sudo tee -a ' + self.moabInstallPath + '/tools/msm/images.txt > /dev/null'
            elif self.machine == 'india':
                moabstring = 'echo "' + self.prefix + self.operatingsystem + '' + self.name + ' ' + self.arch + ' boottarget ' + self.prefix + self.operatingsystem + '' + self.name + ' netboot" | sudo tee -a ' + self.moabInstallPath + '/tools/msm/images.txt > /dev/null'
            self.logger.debug(moabstring)
            status = os.system(moabstring)
            if status != 0:
                msg = 'ERROR: including image name in image.txt file'
                self.logger.debug(msg)
                self.errormsg(connstream, msg)
                return
            connstream.write('OK')
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
            cmd = 'sudo ' + self.moabInstallPath + '/bin/mschedctl -R'
            status = self.runCmd(cmd)
            self.logger.info('Image Register Moab DONE')

    def errormsg(self, connstream, msg):
        self.logger.error(msg)
        try:
            connstream.write(msg)
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            self.logger.debug('In errormsg: ' + str(sys.exc_info()))

        self.logger.info('Image Register Moab DONE')

    def runCmd(self, cmd):
        cmdLog = logging.getLogger('RegisterMoab.exec')
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
    print '\n The user that executes this must have sudo with NOPASSWD for "tee -a" and "mschedctl -R" commands'
    server = IMRegisterServerMoab()
    server.start()


if __name__ == '__main__':
    main()