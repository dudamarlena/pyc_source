# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/renderserver/service.py
# Compiled at: 2018-07-04 04:43:43
from ConfigParser import SafeConfigParser
import optparse, logging, sys, os
from os.path import *
import win32serviceutil, win32service, win32event, win32process, win32api
from win32com.client import constants
import _winreg, pkg_resources
from pkg_resources import iter_entry_points
from pkg_resources import working_set, Environment
organization = 'py3o'
product_name = 'py3o-renderserver'

def get_config():
    """find the config file path in the registry
    """

    class Config(object):
        pass

    config = Config()
    try:
        reg_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\%s\\%s' % (organization, product_name))
        config.soffice_host = _winreg.QueryValueEx(reg_key, 'soffice_host')[0]
        config.soffice_port = _winreg.QueryValueEx(reg_key, 'soffice_port')[0]
        config.listen_port = _winreg.QueryValueEx(reg_key, 'listen_port')[0]
        config.listen_interface = _winreg.QueryValueEx(reg_key, 'listen_interface')[0]
        config.javalib = _winreg.QueryValueEx(reg_key, 'javalib')[0]
        config.driver = _winreg.QueryValueEx(reg_key, 'driver')[0]
        config.maxmem = _winreg.QueryValueEx(reg_key, 'maxmem')[0]
    except WindowsError as e:
        logging.exception(str(e))

    return config


def scan_directory(directory):
    distributions, errors = working_set.find_plugins(Environment([directory]))
    map(working_set.add, distributions)
    if len(errors) > 0:
        raise ValueError("Couldn't load %s" % errors)


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


def set_config(options):
    """set the config file path in the registry
    """
    reg_key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\%s\\%s' % (organization, product_name))
    reg_val = _winreg.SetValueEx(reg_key, 'soffice_host', None, _winreg.REG_SZ, options.soffice_host)
    reg_val = _winreg.SetValueEx(reg_key, 'soffice_port', None, _winreg.REG_SZ, options.soffice_port)
    reg_val = _winreg.SetValueEx(reg_key, 'listen_port', None, _winreg.REG_SZ, options.listen_port)
    reg_val = _winreg.SetValueEx(reg_key, 'listen_interface', None, _winreg.REG_SZ, options.listen_interface)
    reg_val = _winreg.SetValueEx(reg_key, 'javalib', None, _winreg.REG_SZ, options.javalib)
    reg_val = _winreg.SetValueEx(reg_key, 'driver', None, _winreg.REG_SZ, options.driver)
    reg_val = _winreg.SetValueEx(reg_key, 'maxmem', None, _winreg.REG_SZ, options.maxmem)
    return


class Py3oWindowsService(win32serviceutil.ServiceFramework):
    """The Py3oWindowsService class contains all the functionality required
    for running a py3o renderserver as a Windows Service. The only
    user edits required for this class are located in the following class
    variables:

    _svc_name_:         The name of the service (used in the Windows registry).
                        DEFAULT: The capitalized name of the current directory.
    _svc_display_name_: The name that will appear in the Windows Service Manager.
                        DEFAULT: The capitalized name of the current directory.

    For information on installing the application, please refer to the
    documentation at the end of this module or navigate to the directory
    where this module is located and type "service.py" from the command
    prompt.
    """
    _svc_name_ = '%s' % product_name
    _svc_display_name_ = _svc_name_
    _svc_deps = list()

    def __init__(self, args):
        """set some usefull variables
        """
        sys.stdout = NullOutput()
        sys.stderr = NullOutput()
        win32serviceutil.ServiceFramework.__init__(self, args)

    def SvcDoRun(self):
        """Called when the Windows Service runs."""
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            config = get_config()
            from py3o.renderserver.server import start_server
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            start_server(config)
        except Exception as e:
            self.ReportServiceStatus(win32service.SERVICE_ERROR_CRITICAL)
            import servicemanager
            servicemanager.LogErrorMsg('The service could not start for the folloing reason: %s' % str(e))
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcStop(self):
        """Called when Windows receives a service stop request."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        from twisted.internet import reactor
        reactor.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)


def config():
    """write the configuration parameters of the py3o-renderserver service in the windows registry
    """
    optparser = optparse.OptionParser()
    optparser.add_option('-a', '--sofficehost', dest='soffice_host', help='specify the open office hostname/ip address ADDR', metavar='ADDR', default='127.0.0.1')
    optparser.add_option('-p', '--sofficeport', dest='soffice_port', help='specify the open office port PORT', metavar='PORT', default='8997')
    optparser.add_option('-l', '--listenport', dest='listen_port', help='specify the PORT on which our service will listen', metavar='PORT', default=8994)
    optparser.add_option('-i', '--listeninterface', dest='listen_interface', help='specify the INTERFACE on which our service will listen (default: all interfaces)', metavar='INTERFACE', default=None)
    optparser.add_option('-d', '--driver', dest='driver', help='choose a driver between juno & pyuno', default='juno')
    optparser.add_option('-j', '--java', dest='javalib', help='choose a jvm.dll/jvm.so to use if you are using the juno driver', default=None)
    optparser.add_option('-m', '--maxmem', dest='maxmem', help='how much memory to give to the JVM if you are using juno driver, default is 150Mb', default='150')
    options, args = optparser.parse_args()
    set_config(options)
    return


def setup():
    """basic win32 service setup: install or remove or update or start or stop the service
    """
    win32serviceutil.HandleCommandLine(Py3oWindowsService)