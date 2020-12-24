# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/plone/recipe/cluster/nt_service.py
# Compiled at: 2008-08-11 05:37:05
"""Windows Services installer/controller for Zope/ZEO/ZRS instance homes"""
import sys, os, time, threading, signal, pywintypes, winerror, win32con, win32api, win32event, win32file, win32pipe, win32process, win32security, win32service, win32serviceutil, servicemanager
BACKOFF_MAX = 300
BACKOFF_CLEAR_TIME = 30
BACKOFF_INITIAL_INTERVAL = 5
CHILDCAPTURE_BLOCK_SIZE = 80
CHILDCAPTURE_MAX_BLOCKS = 50

class Service(win32serviceutil.ServiceFramework):
    """Base class for a Windows Server to manage an external process.

    Subclasses can be used to managed an instance home-based Zope or
    ZEO process.  The win32 Python service module registers a specific
    file and class for a service.  To manage an instance, a subclass
    should be created in the instance home.
    """
    __module__ = __name__
    _svc_name_ = 'Zope-Instance'
    _svc_display_name_ = 'Zope instance at C:\\Zope-Instance'
    process_runner = 'C:\\Program Files\\Zope-2.7.0-a1\\bin\\python.exe'
    process_args = '{path_to}\\run.py -C {path_to}\\zope.conf'
    evtlog_name = 'Zope'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        try:
            servicemanager.SetEventSourceName(self.evtlog_name)
        except AttributeError:
            pass

        sa = win32security.SECURITY_ATTRIBUTES()
        sa.bInheritHandle = True
        self.hWaitStop = win32event.CreateEvent(sa, 0, 0, None)
        self.redirect_thread = None
        return

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.onStop()
        win32event.SetEvent(self.hWaitStop)

    SvcShutdown = SvcStop

    def onStop(self):
        pass

    def createProcess(self, cmd):
        self.start_time = time.time()
        return self.createProcessCaptureIO(cmd)

    def logmsg(self, event):
        try:
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, event, (
             self._svc_name_, ' (%s)' % self._svc_display_name_))
        except win32api.error, details:
            try:
                print 'FAILED to write INFO event', event, ':', details
            except IOError:
                pass

    def _dolog(self, func, msg):
        try:
            fullmsg = '%s (%s): %s' % (self._svc_name_, self._svc_display_name_, msg)
            func(fullmsg)
        except win32api.error, details:
            try:
                print 'FAILED to write event log entry:', details
                print msg
            except IOError:
                pass

    def info(self, s):
        self._dolog(servicemanager.LogInfoMsg, s)

    def warning(self, s):
        self._dolog(servicemanager.LogWarningMsg, s)

    def error(self, s):
        self._dolog(servicemanager.LogErrorMsg, s)

    def SvcDoRun(self):
        os.environ['ZMANAGED'] = '1'
        self.backoff_interval = BACKOFF_INITIAL_INTERVAL
        self.backoff_cumulative = 0
        self.logmsg(servicemanager.PYS_SERVICE_STARTED)
        while 1:
            cmd = '"%s" %s' % (self.process_runner, self.process_args)
            info = self.createProcess(cmd)
            self.hZope = info[0]
            if self.backoff_interval > BACKOFF_INITIAL_INTERVAL:
                self.info('created process')
            if not (self.run() and self.checkRestart()):
                break

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        winver = sys.getwindowsversion()
        for (sig, timeout) in ((signal.SIGINT, 30), (signal.SIGTERM, 10)):
            event_name = 'Zope-%d-%d' % (info[2], sig)
            if winver[0] >= 5 and winver[3] == 2:
                event_name = 'Global\\' + event_name
            try:
                he = win32event.OpenEvent(win32event.EVENT_MODIFY_STATE, 0, event_name)
            except win32event.error, details:
                if details[0] == winerror.ERROR_FILE_NOT_FOUND:
                    break
                self.warning('Failed to open child shutdown event %s' % (event_name,))
                continue

            win32event.SetEvent(he)
            for i in range(timeout):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                rc = win32event.WaitForSingleObject(self.hZope, 3000)
                if rc == win32event.WAIT_OBJECT_0:
                    break

            if rc == win32event.WAIT_OBJECT_0:
                break

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if win32process.GetExitCodeProcess(self.hZope) == win32con.STILL_ACTIVE:
            win32api.TerminateProcess(self.hZope, 3)
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.redirect_thread is not None:
            for i in range(5):
                self.redirect_thread.join(1)
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                if not self.redirect_thread.isAlive():
                    break
            else:
                self.warning('Redirect thread did not stop!')
        self.logmsg(servicemanager.PYS_SERVICE_STOPPED)
        return

    def run(self):
        """Monitor the daemon process.

        Returns True if the service should continue running and
        False if the service process should exit.  On True return,
        the process exited unexpectedly and the caller should restart
        it.
        """
        keep_running = True
        rc = win32event.WaitForMultipleObjects([self.hWaitStop, self.hZope], 0, win32event.INFINITE)
        if rc == win32event.WAIT_OBJECT_0:
            keep_running = False
        elif rc == win32event.WAIT_OBJECT_0 + 1:
            status = win32process.GetExitCodeProcess(self.hZope)
            if status != 0:
                self.redirect_thread.join(5)
                if self.redirect_thread.isAlive():
                    self.warning('Redirect thread did not stop!')
                self.warning('process terminated with exit code %d.\n%s' % (status, ('').join(self.captured_blocks)))
            keep_running = status != 0
        else:
            assert 0, rc
        return keep_running

    def checkRestart(self):
        if self.backoff_cumulative > BACKOFF_MAX:
            self.error('restarting too frequently; quit')
            return False
        self.warning('sleep %s to avoid rapid restarts' % self.backoff_interval)
        if time.time() - self.start_time > BACKOFF_CLEAR_TIME:
            self.backoff_interval = BACKOFF_INITIAL_INTERVAL
            self.backoff_cumulative = 0
        if win32event.WAIT_OBJECT_0 == win32event.WaitForSingleObject(self.hWaitStop, self.backoff_interval * 1000):
            return False
        self.backoff_cumulative += self.backoff_interval
        self.backoff_interval *= 2
        return True

    def createProcessCaptureIO(self, cmd):
        (hInputRead, hInputWriteTemp) = self.newPipe()
        (hOutReadTemp, hOutWrite) = self.newPipe()
        pid = win32api.GetCurrentProcess()
        hErrWrite = win32api.DuplicateHandle(pid, hOutWrite, pid, 0, 1, win32con.DUPLICATE_SAME_ACCESS)
        hOutRead = self.dup(hOutReadTemp)
        hInputWrite = self.dup(hInputWriteTemp)
        si = win32process.STARTUPINFO()
        si.hStdInput = hInputRead
        si.hStdOutput = hOutWrite
        si.hStdError = hErrWrite
        si.dwFlags = win32process.STARTF_USESTDHANDLES | win32process.STARTF_USESHOWWINDOW
        si.wShowWindow = win32con.SW_HIDE
        create_flags = win32process.CREATE_NEW_CONSOLE
        info = win32process.CreateProcess(None, cmd, None, None, True, create_flags, None, None, si)
        hOutWrite.Close()
        hErrWrite.Close()
        hInputRead.Close()
        hInputWrite.Close()
        t = threading.Thread(target=self.redirectCaptureThread, args=(hOutRead,))
        t.start()
        self.redirect_thread = t
        return info

    def redirectCaptureThread(self, handle):
        self.captured_blocks = []
        while 1:
            try:
                (ec, data) = win32file.ReadFile(handle, CHILDCAPTURE_BLOCK_SIZE)
            except pywintypes.error, err:
                if err[0] != winerror.ERROR_BROKEN_PIPE:
                    self.warning('Error reading output from process: %s' % err)
                break

            self.captured_blocks.append(data)
            del self.captured_blocks[CHILDCAPTURE_MAX_BLOCKS:]

        handle.Close()

    def newPipe(self):
        sa = win32security.SECURITY_ATTRIBUTES()
        sa.bInheritHandle = True
        return win32pipe.CreatePipe(sa, 0)

    def dup(self, pipe):
        pid = win32api.GetCurrentProcess()
        dup = win32api.DuplicateHandle(pid, pipe, pid, 0, 0, win32con.DUPLICATE_SAME_ACCESS)
        pipe.Close()
        return dup


if __name__ == '__main__':
    print "This is a framework module - you don't run it directly."
    print 'See your $SOFTWARE_HOME\x08in directory for the service script.'
    sys.exit(1)