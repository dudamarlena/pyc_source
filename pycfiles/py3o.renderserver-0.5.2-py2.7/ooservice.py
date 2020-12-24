# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ooservice/ooservice.py
# Compiled at: 2013-11-20 05:57:33
import time
from ConfigParser import SafeConfigParser
import optparse, logging, sys, os
from os.path import *
import win32serviceutil, win32service, win32event, win32process, win32api
from win32com.client import constants
import _winreg
from subprocess import Popen
organization = 'py3o'
product_name = 'py3o-sofficeserver'

class NullOutput(object):
    """a file-like object that behaves like a black hole.
    Does not consume memory and gives nothing back. Ever.
    """

    def noop(self, *args, **kw):
        pass

    write = writelines = close = seek = flush = truncate = noop

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration

    def isatty(self):
        return False

    def tell(self):
        return 0

    def read(self, *args, **kw):
        return ''

    readline = read

    def readlines(self, *args, **kw):
        return list()


def get_config():
    """find the config file path in the registry
    """
    config = dict()
    try:
        reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\%s\\%s' % (organization, product_name))
        config['soffice_path'] = _winreg.QueryValueEx(reg_key, 'soffice_path')[0]
        config['soffice_host'] = _winreg.QueryValueEx(reg_key, 'soffice_host')[0]
        config['soffice_port'] = int(_winreg.QueryValueEx(reg_key, 'soffice_port')[0])
    except WindowsError as e:
        logging.exception(str(e))

    return config


def set_config(options):
    """set the config file path in the registry
    """
    reg_key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\%s\\%s' % (organization, product_name))
    reg_val = _winreg.SetValueEx(reg_key, 'soffice_path', None, _winreg.REG_SZ, options.soffice_path)
    reg_val = _winreg.SetValueEx(reg_key, 'soffice_host', None, _winreg.REG_SZ, options.soffice_host)
    reg_val = _winreg.SetValueEx(reg_key, 'soffice_port', None, _winreg.REG_SZ, options.soffice_port)
    return


class Py3oSofficeService(win32serviceutil.ServiceFramework):
    """The Py3oSofficeService class contains all the functionality required
    for running a Open Office instance as a Windows Service.
    """
    _svc_name_ = '%s' % product_name
    _svc_display_name_ = _svc_name_
    _svc_deps = list()

    def __init__(self, args):
        """set some usefull variables
        """
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = NullOutput()
        sys.stderr = NullOutput()
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        return

    def SvcDoRun(self):
        """Called when the Windows Service runs."""
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.serv_process = self.runoo()
        pcs = win32process.EnumProcesses()
        if self.serv_process.pid in pcs:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        else:
            self.ReportServiceStatus(win32service.SERVICE_ERROR_CRITICAL)
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcStop(self):
        """Called when Windows receives a service stop request."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        try:
            win32api.TerminateProcess(int(self.serv_process._handle), -1)
        except:
            pass

        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def runoo(self):
        """Bootsrap an Uno application environment by starting a soffice server
        and then connecting to it.
        """
        call_flags = 0
        call_flags |= win32process.CREATE_NO_WINDOW
        config = get_config()
        soffice_bin = config['soffice_path']
        host = config['soffice_host']
        tcp_port = config['soffice_port']
        cmdArray = (
         '%s' % soffice_bin,
         '-nologo',
         '-norecover',
         '-norestore',
         '-invisible',
         '-headless',
         '-nocrashreport',
         '-nofirststartwizard',
         '-nodefault',
         '-accept=socket,host=%s,port=%s;urp;' % (host, tcp_port))
        p = Popen(cmdArray, creationflags=call_flags)
        time.sleep(1.0)
        return p


def setup():
    """basic win32 service setup: install or remove or update or start or stop the service
    """
    win32serviceutil.HandleCommandLine(Py3oSofficeService)


def config():
    """write the configuration parameters of the OpenOffice service in the windows registry
    """
    optparser = optparse.OptionParser()
    optparser.add_option('-s', '--sofficepath', dest='soffice_path', help='specify the open office file path FILE', metavar='FILE', default=None)
    optparser.add_option('-a', '--sofficehost', dest='soffice_host', help='specify the open office hostname/ip address ADDR', metavar='ADDR', default='127.0.0.1')
    optparser.add_option('-p', '--sofficeport', dest='soffice_port', help='specify the open office port PORT', metavar='PORT', default='8997')
    options, args = optparser.parse_args()
    set_config(options)
    sys.exit(0)
    return