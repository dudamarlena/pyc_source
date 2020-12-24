# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twillrecord/utils.py
# Compiled at: 2007-03-22 10:11:26
"""FunkLoad common utils.

$Id: utils.py 24649 2005-08-29 14:20:19Z bdelbosc $
"""
import os, sys, time, logging
from time import sleep
from socket import error as SocketError
from xmlrpclib import ServerProxy
MIN_SLEEPTIME = 0.005

def thread_sleep(seconds=0):
    """Sleep seconds.

    Insure that seconds is at least MIN_SLEEPTIME to let
    threads working properly."""
    sleep(max(abs(seconds), MIN_SLEEPTIME))


g_recording = False
g_running = False

def recording():
    """A semaphore to tell the running threads when to begin recording."""
    global g_recording
    return g_recording


def set_recording_flag(value):
    """Enable recording."""
    global g_recording
    g_recording = value


def running():
    """A semaphore to tell the running threads that it should continue running
    ftest."""
    global g_running
    return g_running


def set_running_flag(value):
    """Set running mode on."""
    global g_running
    g_running = value


def create_daemon():
    """Detach a process from the controlling terminal and run it in the
    background as a daemon.
    """
    try:
        pid = os.fork()
    except OSError, msg:
        raise Exception, '%s [%d]' % (msg.strerror, msg.errno)

    if pid == 0:
        os.setsid()
        try:
            pid = os.fork()
        except OSError, msg:
            raise Exception, '%s [%d]' % (msg.strerror, msg.errno)
        else:
            if pid == 0:
                os.umask(0)
            else:
                os._exit(0)
    else:
        sleep(0.5)
        os._exit(0)
    import resource
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if maxfd == resource.RLIM_INFINITY:
        maxfd = 1024
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:
            pass

    os.open('/dev/null', os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)
    return 0


MMN_SEP = ':'

def mmn_is_bench(meta_method_name):
    """Is it a meta method name ?."""
    return meta_method_name.count(MMN_SEP) and True or False


def mmn_encode(method_name, cycle, cvus, thread_id):
    """Encode a extra information into a method_name."""
    return MMN_SEP.join((method_name, str(cycle), str(cvus), str(thread_id)))


def mmn_decode(meta_method_name):
    """Decode a meta method name."""
    if mmn_is_bench(meta_method_name):
        (method_name, cycle, cvus, thread_id) = meta_method_name.split(MMN_SEP)
        return (method_name, int(cycle), int(cvus), int(thread_id))
    else:
        return (
         meta_method_name, 1, 0, 1)


def get_default_logger(log_to, log_path=None, level=logging.DEBUG, name='FunkLoad'):
    """Get a logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    if log_to.count('console'):
        hdlr = logging.StreamHandler()
        logger.addHandler(hdlr)
    if log_to.count('file') and log_path:
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr = logging.FileHandler(log_path)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
    if log_to.count('xml') and log_path:
        if os.access(log_path, os.F_OK):
            os.rename(log_path, log_path + '.bak-' + str(int(time.time())))
        hdlr = logging.FileHandler(log_path)
        logger.addHandler(hdlr)
    logger.setLevel(level)
    return logger


def close_logger(name):
    """Close the logger."""
    logger = logging.getLogger(name)
    for hdlr in logger.handlers:
        logger.removeHandler(hdlr)


def trace(message):
    """Simple print to stdout

    Not thread safe."""
    sys.stdout.write(message)
    sys.stdout.flush()


def xmlrpc_get_credential(host, port, group=None):
    """Get credential thru xmlrpc credential_server."""
    url = 'http://%s:%s' % (host, port)
    server = ServerProxy(url)
    try:
        return server.getCredential(group)
    except SocketError:
        raise SocketError('No Credential server reachable at %s, use fl-credential-ctl to start the credential server.' % url)


def xmlrpc_list_groups(host, port):
    """Get list of groups thru xmlrpc credential_server."""
    url = 'http://%s:%s' % (host, port)
    server = ServerProxy(url)
    try:
        return server.listGroups()
    except SocketError:
        raise SocketError('No Credential server reachable at %s, use fl-credential-ctl to start the credential server.' % url)


def xmlrpc_list_credentials(host, port, group=None):
    """Get list of users thru xmlrpc credential_server."""
    url = 'http://%s:%s' % (host, port)
    server = ServerProxy(url)
    try:
        return server.listCredentials(group)
    except SocketError:
        raise SocketError('No Credential server reachable at %s, use fl-credential-ctl to start the credential server.' % url)


def get_version():
    """Retrun the FunkLoad package version."""
    from pkg_resources import get_distribution
    return get_distribution('twillrecord').version


_COLOR = {'green': '\x1b[32;01m', 'red': '\x1b[31;01m', 'reset': '\x1b[0m'}

def red_str(text):
    """Return red text."""
    global _COLOR
    return _COLOR['red'] + text + _COLOR['reset']


def green_str(text):
    """Return green text."""
    return _COLOR['green'] + text + _COLOR['reset']


def is_html(text):
    """Simple check that return True if the text is an html page."""
    if '<html' in text[:300].lower():
        return True
    return False


class BaseFilter(object):
    """Base filter."""
    __module__ = __name__

    def __ror__(self, other):
        return other

    def __call__(self, other):
        return other | self


class truncate(BaseFilter):
    """Middle truncate string up to length."""
    __module__ = __name__

    def __init__(self, length=40, extra='...'):
        self.length = length
        self.extra = extra

    def __ror__(self, other):
        if len(other) > self.length:
            mid_size = (self.length - 3) / 2
            other = other[:mid_size] + self.extra + other[-mid_size:]
        return other


def is_valid_html(html=None, file_path=None, accept_warning=False):
    """Ask tidy if the html is valid.

    Return a tuple (status, errors)
    """
    if not file_path:
        (fd, file_path) = mkstemp(prefix='fl-tidy', suffix='.html')
        os.write(fd, html)
        os.close(fd)
    tidy_cmd = 'tidy -errors %s' % file_path
    (ret, output) = getstatusoutput(tidy_cmd)
    status = False
    if ret == 0:
        status = True
    elif ret == 256:
        if accept_warning:
            status = True
    elif ret > 512:
        if 'command not found' in output:
            raise RuntimeError('tidy command not found, please install tidy.')
        raise RuntimeError('Executing [%s] return: %s ouput: %s' % (tidy_cmd, ret, output))
    return (status, output)