# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/easycluster/winservice.py
# Compiled at: 2013-03-08 16:51:28
import sys, os, traceback, win32serviceutil, win32service
KEY_PATH = os.path.join(os.environ.get('SYSTEMROOT', 'c:\\windows'), 'system32', 'easycluster_service.key')

class EasyClusterService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'EasyCluster'
    _svc_display_name_ = 'EasyCluster remote execution service'
    server = None

    def SvcDoRun(self):
        """Start and run the service."""
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            import easycluster.server, servicemanager
            servicemanager.LogInfoMsg('%s - Starting (%r)' % (self._svc_name_, sys.executable))
            easycluster.server.server_main(['-S', '-k', KEY_PATH])
        except Exception:
            import servicemanager
            servicemanager.LogErrorMsg(traceback.format_exc())

    def SvcStop(self):
        """Stop the service."""
        import easycluster.server, servicemanager
        servicemanager.LogInfoMsg('%s - Shutting down' % self._svc_name_)
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        easycluster.server.stop_server()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(EasyClusterService)