# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid_passwdstack/passwdstack/PasswdStackServer.py
# Compiled at: 2012-08-20 15:20:19
"""
Server to modify the password of OpenStack dashboard
"""
__author__ = 'Javier Diaz'
from types import *
import re, logging, logging.handlers, random, os, sys, socket, ssl
from multiprocessing import Process
from subprocess import *
import time
from futuregrid_passwdstack.passwdstack.PasswdStackServerConf import PasswdStackServerConf
from futuregrid_passwdstack.utils.FGTypes import FGCredential
from futuregrid_passwdstack.utils import FGAuth

class PasswdStackServer(object):

    def __init__(self):
        super(PasswdStackServer, self).__init__()
        self.user = ''
        self.numparams = 4
        self._genConf = PasswdStackServerConf()
        self._genConf.load_passwdstackServerConfig()
        self.port = self._genConf.getPort()
        self.proc_max = self._genConf.getProcMax()
        self.refresh_status = self._genConf.getRefreshStatus()
        self.log_filename = self._genConf.getLog()
        self.logLevel = self._genConf.getLogLevel()
        self.logger = self.setup_logger()
        self._ca_certs = self._genConf.getCaCerts()
        self._certfile = self._genConf.getCertFile()
        self._keyfile = self._genConf.getKeyFile()
        print '\nReading Configuration file from ' + self._genConf.getConfigFile() + '\n'

    def setup_logger(self):
        logger = logging.getLogger('PasswdStackServer')
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
                proc_list.append(Process(target=self.passwdreset, args=(connstream, fromaddr[0])))
                proc_list[(len(proc_list) - 1)].start()
            except ssl.SSLError:
                self.logger.error('Unsuccessful connection attempt from: ' + repr(fromaddr))
                self.logger.info('Password Stack Request DONE')
            except socket.error:
                self.logger.error('Error with the socket connection')
                self.logger.info('Password Stack Request DONE')
            except:
                self.logger.error('Uncontrolled Error: ' + str(sys.exc_info()))
                try:
                    connstream.shutdown(socket.SHUT_RDWR)
                    connstream.close()
                except:
                    pass
                else:
                    self.logger.info('Password Stack Request DONE')

    def auth(self, userCred):
        return FGAuth.auth(self.user, userCred)

    def passwdreset(self, channel, fromaddr):
        start_all = time.time()
        self.logger = logging.getLogger('PasswdStackServer.' + str(os.getpid()))
        self.logger.info('Starting to process the request')
        data = channel.read(2048)
        params = data.split('|')
        self.user = params[0].strip()
        passwd = params[1].strip()
        passwdtype = params[2].strip()
        dashboardpasswd = params[3]
        if len(params) != self.numparams:
            msg = 'ERROR: incorrect message'
            self.errormsg(channel, msg)
            return
        retry = 0
        maxretry = 3
        endloop = False
        while not endloop:
            userCred = FGCredential(passwdtype, passwd)
            if self.auth(userCred):
                channel.write('OK')
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

        self.logger.info('Reseting the password of the user: ' + self.user)
        leave = True
        cmd = 'keystone user-list'
        p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        std = p.communicate()
        if p.returncode != 0:
            status = 'ERROR: getting user information. ' + std[1]
            self.logger.error(status)
        else:
            status = 'ERROR: User not found.'
            for i in std[0].split('\n'):
                if not re.search('^\\+', i) and i.strip() != '':
                    i = ('').join(i.split()).strip()
                    parts = i.split('|')
                    if parts[0] == '':
                        add = 1
                    else:
                        add = 0
                    if re.search('^' + self.user + '$', parts[(3 + add)].strip()):
                        useridOS = parts[(0 + add)]
                        leave = False
                        status = 'OK'
                        break

            if not leave:
                cmd = 'keystone user-password-update --pass ' + dashboardpasswd + ' ' + useridOS
                p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
                std = p.communicate()
                if p.returncode != 0:
                    status = 'ERROR: updating user password. ' + std[1]
                    self.logger.error(status)
                else:
                    status = 'OK'
            if re.search('^ERROR', status):
                self.errormsg(channel, status)
            else:
                channel.write(str(status))
                channel.shutdown(socket.SHUT_RDWR)
                channel.close()
            end_all = time.time()
            self.logger.info('TIME walltime image generate:' + str(end_all - start_all))
            self.logger.info('Password Stack DONE')

    def errormsg(self, channel, msg):
        self.logger.error(msg)
        try:
            channel.write(msg)
            channel.shutdown(socket.SHUT_RDWR)
            channel.close()
        except:
            self.logger.debug('In errormsg: ' + str(sys.exc_info()))

        self.logger.info('Password Stack DONE')


def main():
    passwdstackserver = PasswdStackServer()
    passwdstackserver.start()


if __name__ == '__main__':
    main()