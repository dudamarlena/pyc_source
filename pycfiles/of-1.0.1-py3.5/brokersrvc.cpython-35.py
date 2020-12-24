# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/broker/brokersrvc.py
# Compiled at: 2016-12-01 18:02:10
# Size of source mod 2**32: 1703 bytes
"""
This module implements windows service functionality for the Optimal Framework

Created on Jan 22, 2016

@author: Nicklas Boerjesson

"""
import os, servicemanager, socket, sys, win32event, win32service, win32serviceutil
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, '../../'))
from of.common.win32svc import write_to_event_log
import of.broker.broker

class BrokerService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'Optimal BPM Broker Service'
    _svc_display_name_ = 'The Optimal BPM Broker Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        _exit_status = of.broker.broker.stop_broker('Shutting down the Broker service')
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        os.exit(_exit_status)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (
         self._svc_name_, ''))
        self.main()

    def main(self):
        try:
            of.broker.broker.start_broker()
        except Exception as e:
            write_to_event_log('Application', 1, 'Error starting broker', str(e))


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(BrokerService)