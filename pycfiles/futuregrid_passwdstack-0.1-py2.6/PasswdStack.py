# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid_passwdstack/passwdstack/PasswdStack.py
# Compiled at: 2012-08-20 15:17:26
"""
Command line front end for passwdstack
"""
__author__ = 'Javier Diaz'
import argparse
from types import *
import re, logging, logging.handlers, glob, random, os, sys, socket, ssl
from subprocess import *
import textwrap, re, time
from getpass import getpass
import hashlib
from futuregrid_passwdstack.passwdstack.PasswdStackClientConf import PasswdStackClientConf
from futuregrid_passwdstack.utils import fgLog

class PasswdStack(object):

    def __init__(self, user, passwd, verbose):
        super(PasswdStack, self).__init__()
        self.user = user
        self.passwd = passwd
        self._verbose = verbose
        self._genConf = PasswdStackClientConf()
        self._genConf.load_passwdstackConfig()
        self.serveraddr = self._genConf.getServeraddr()
        self.port = self._genConf.getPort()
        self._ca_certs = self._genConf.getCaCerts()
        self._certfile = self._genConf.getCertFile()
        self._keyfile = self._genConf.getKeyFile()
        self._log = fgLog.fgLog(self._genConf.getLogFile(), self._genConf.getLogLevel(), 'PasswdStackClient', False)

    def check_auth(self, socket_conn, checkauthstat):
        endloop = False
        passed = False
        while not endloop:
            ret = socket_conn.read(1024)
            if ret == 'OK':
                if self._verbose:
                    print 'Authentication OK. Your image request is being processed'
                self._log.debug('Authentication OK')
                endloop = True
                passed = True
            elif ret == 'TryAuthAgain':
                msg = 'ERROR: Permission denied, please try again. User is ' + self.user
                self._log.error(msg)
                if self._verbose:
                    print msg
                m = hashlib.md5()
                m.update(getpass())
                passwd = m.hexdigest()
                socket_conn.write(passwd)
                self.passwd = passwd
            elif ret == 'NoActive':
                msg = 'ERROR: The status of the user ' + self.user + ' is not active'
                checkauthstat.append(str(msg))
                self._log.error(msg)
                endloop = True
                passed = False
            elif ret == 'NoUser':
                msg = 'ERROR: User ' + self.user + ' does not exist'
                checkauthstat.append(str(msg))
                self._log.error(msg)
                endloop = True
                passed = False
            else:
                self._log.error(str(ret))
                checkauthstat.append(str(ret))
                endloop = True
                passed = False

        return passed

    def passwdstackReset(self, dashboardpasswd):
        start_all = time.time()
        output = None
        checkauthstat = []
        options = str(self.user) + '|' + str(self.passwd) + '|ldappassmd5|' + str(dashboardpasswd)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            genServer = ssl.wrap_socket(s, ca_certs=self._ca_certs, certfile=self._certfile, keyfile=self._keyfile, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1)
            self._log.debug('Connecting server: ' + self.serveraddr + ':' + str(self.port))
            if self._verbose:
                print 'Connecting server: ' + self.serveraddr + ':' + str(self.port)
            genServer.connect((self.serveraddr, self.port))
        except ssl.SSLError:
            self._log.error('CANNOT establish SSL connection. EXIT')
            if self._verbose:
                print 'ERROR: CANNOT establish SSL connection. EXIT'

        genServer.write(options)
        if self._verbose:
            print 'Your request is in the queue to be processed after authentication'
        if self.check_auth(genServer, checkauthstat):
            ret = genServer.read(2048)
            if re.search('^ERROR', ret):
                output = 'The password could not be modified. Exit error:' + ret
                self._log.error(output)
            else:
                output = 'The password was reset: ' + str(ret)
                self._log.debug(output)
        else:
            self._log.error(str(checkauthstat[0]))
            if self._verbose:
                print checkauthstat[0]
            return
        end_all = time.time()
        self._log.info('TIME walltime reset client passwd:' + str(end_all - start_all))
        return output


def main():
    parser = argparse.ArgumentParser(prog='fg-passwdstack', formatter_class=argparse.RawDescriptionHelpFormatter, description='FutureGrid Passwd Stack Help')
    parser.add_argument('-u', '--user', dest='user', required=True, help='FutureGrid User name')
    args = parser.parse_args()
    print 'Passwd Stack client...'
    verbose = True
    print 'Please insert the password for the user ' + args.user + ''
    m = hashlib.md5()
    m.update(getpass('Enter Portal Password: '))
    passwd = m.hexdigest()
    print ''
    print 'Please insert the password you want to have in the OpenStack dashboard'
    dashboard_pass1 = getpass('Enter new Dashboard password: ')
    dashboard_pass2 = getpass('Retype new Dashboard password: ')
    if dashboard_pass1 != dashboard_pass2:
        print 'ERROR: OpenStack Dashboard: the password differ'
        sys.exit(-1)
    if dashboard_pass1 == '' or dashboard_pass1 == None:
        print 'ERROR: OpenStack Dashboard: the password is empty'
        sys.exit(-1)
    score = CheckPassword(dashboard_pass1)
    if score <= 1:
        print 'ERROR: OpenStack Dashboard: the password is too weak. Please use a longer password; include numbers; ' + 'upper case and lower case characters'
        sys.exit(-1)
    strength = ['Blank', 'Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong']
    print 'The strength of the password is: ' + strength[score]
    imgen = PasswdStack(args.user, passwd, verbose)
    status = imgen.passwdstackReset(dashboard_pass1)
    print status
    return


def CheckPassword(password):
    score = 1
    if len(password) < 1:
        score = 0
    if len(password) < 4:
        score = 1
    if len(password) >= 8:
        score = score + 1
    if len(password) >= 10:
        score = score + 1
    if re.search('\\d+', password):
        score = score + 1
    if re.search('[a-z]', password) and re.search('[A-Z]', password):
        score = score + 1
    if re.search('.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]', password):
        score = score + 1
    return score


if __name__ == '__main__':
    main()