# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/easycluster/windows_service.py
# Compiled at: 2019-04-18 17:28:18
import sys, os, traceback, win32serviceutil, win32service, pywintypes, easycluster as _core
sysroot = os.environ.get('SYSTEMROOT', 'c:\\windows')
sysdir = os.path.join(sysroot, 'sysnative')
if not os.path.isdir(sysdir):
    sysdir = os.path.join(sysroot, 'system32')
KEY_PATH = os.path.join(sysdir, 'easycluster_service.key')
del sysdir
del sysroot

class EasyClusterService(win32serviceutil.ServiceFramework):
    if _core.PYTHON3:
        _svc_name_ = 'EasyCluster-Py3'
        _svc_display_name_ = 'EasyCluster remote execution service (Python 3)'
    else:
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


def _service_action(*args):
    return win32serviceutil.HandleCommandLine(EasyClusterService, argv=[''] + list(args))


def install_service():
    return _service_action('--startup', 'auto', 'install')


def uninstall_service():
    return _service_action('remove')


def start_service():
    return _service_action('start')


def stop_service():
    return _service_action('stop')


def query_service_installed():
    hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
    try:
        try:
            hs = win32serviceutil.SmartOpenService(hscm, EasyClusterService._svc_name_, win32service.SERVICE_ALL_ACCESS)
            win32service.CloseServiceHandle(hs)
            return True
        except pywintypes.error:
            return False

    finally:
        win32service.CloseServiceHandle(hscm)

    return


daemonize = None
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(EasyClusterService)