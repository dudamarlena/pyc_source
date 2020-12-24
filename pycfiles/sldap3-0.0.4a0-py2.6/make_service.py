# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sldap3\make_service.py
# Compiled at: 2015-04-22 18:13:37
"""
"""
import logging
from time import sleep
import sys
from sldap3 import EXEC_THREAD, EXEC_PROCESS
logging.basicConfig(filename='c:\\Temp\\sldap3.log', level=logging.DEBUG, format='[sldap3-service] %(levelname)-7.7s %(message)s')
try:
    import win32serviceutil, win32service, win32event, servicemanager
except ImportError:
    logging.error('pywin32 package missing')
    sys.exit(1)

sys.stderr = open('C:\\Temp\\pyasn1.log', 'a')
try:
    import pyasn1
except ImportError:
    logging.error('pyasn1 package missing')
    sys.exit(2)

try:
    import ldap3
except ImportError:
    logging.error('ldap3 package missing')
    sys.exit(3)

try:
    from asyncio import BaseEventLoop
except ImportError:
    try:
        import trollius as asyncio
        from trollius import From, Return
    except:
        logging.error('trollius package missing')
        sys.exit(4)

try:
    import sldap3
except ImportError:
    logging.error('sldap3 package missing')
    sys.exit(5)

class Sldap3Service(win32serviceutil.ServiceFramework):
    _svc_name_ = 'sldap3'
    _svc_display_name_ = 'sldap3 - LDAP Server'
    _svc_description_ = 'A strictly RFC 4511 conforming LDAP V3 pure Python server'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.instances = list()
        self.stop_requested = False
        return

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('stopping sldap3 service...')
        self.stop_requested = True

    def SvcDoRun(self):
        logging.info('running sldap3 service...')
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (
         self._svc_name_, ''))
        self.run()
        logging.info('ending sldap3 service...')

    def run(self):
        logging.info('executing sldap3 service...')
        logging.info('instantiating sldap3 daemon')
        self.instances = []
        user_backend = sldap3.JsonUserBackend('/root/sldap3/test/localhost-users.json')
        user_backend.add_user('giovanni', 'admin', 'password')
        user_backend.add_user('beatrice', 'user', 'password')
        user_backend.store()
        dsa1 = sldap3.Instance(sldap3.Dsa('DSA1', '0.0.0.0', cert_file='/root/sldap3/test/server-cert.pem', key_file='/root/sldap3/test/server-key.pem', user_backend=user_backend), name='MixedInstance', executor=EXEC_THREAD)
        dsa2 = sldap3.Instance(sldap3.Dsa('DSA2', '0.0.0.0', port=1389, user_backend=user_backend), name='UnsecureInstance', executor=EXEC_THREAD)
        self.instances.append(dsa1)
        self.instances.append(dsa2)
        for instance in self.instances:
            instance.start()

        logging.info('sldap3 daemon instantiation complete')
        while not self.stop_requested:
            sleep(3)

        for instance in self.instances:
            instance.stop()

        logging.info('sldap3 service stopped')


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(Sldap3Service)