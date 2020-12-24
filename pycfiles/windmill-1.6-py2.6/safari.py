# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/browser/safari.py
# Compiled at: 2011-01-13 01:48:44
import commands, tempfile, logging, signal, killableprocess, subprocess, sys, os
if not sys.version.startswith('2.4'):
    import urlparse
else:
    from windmill.tools import urlparse_25 as urlparse
from StringIO import StringIO
import windmill
logger = logging.getLogger(__name__)
html_redirection = '\n<html>\n  <head>\n    <script type="text/javascript">\t\n    var i = function(){\n    \twindow.location = "{replace}";\n    }\n    </script>\n </head>\n  <body onload="i();">\t\n  </body>\n<html>'

def getoutput(l):
    tmp = tempfile.mktemp()
    x = open(tmp, 'w')
    subprocess.call(l, stdout=x, stderr=x)
    x.close()
    x = open(tmp, 'r')
    r = x.read()
    x.close()
    os.remove(tmp)
    return r


def dprint(s):
    if len(s) is not 0:
        print s.rstrip('\n')
    if 'Library/Preferences/SystemConfiguration/preferences.plist.old' in s:
        print '** To remove this error `chmod -R 777` the directory that shows the permission error'


def find_default_interface_name():
    if windmill.settings['NETWORK_INTERFACE_NAME'] is not None:
        return windmill.settings['NETWORK_INTERFACE_NAME']
    else:
        target_host = urlparse.urlparse(windmill.settings['TEST_URL']).hostname
        x = ['/sbin/route', 'get', target_host]
        interface_id = [ l for l in getoutput(x).splitlines() if 'interface' in l ][0].split(':')[(-1)].strip()
        all_inet = getoutput([windmill.settings['NETWORKSETUP_BINARY'], '-listallhardwareports']).splitlines()
        try:
            i = all_inet.index([ l for l in all_inet if 'Device: ' + interface_id in l ][0])
            interface_name = all_inet[(i - 1)].split(':')[(-1)].strip()
        except IndexError:
            print 'ERROR: Cannot figure out interface name, please set NETWORK_INTERFACE_NAME in local settings file'
            from windmill.bin import admin_lib
            admin_lib.teardown(admin_lib.shell_objects_dict)
            sys.exit()

        return interface_name


class Safari(object):

    def __init__(self):
        self.safari_binary = windmill.settings['SAFARI_BINARY']
        self.test_url = windmill.settings['TEST_URL']

    def create_redirect(self):
        self.redirection_page = tempfile.mktemp(suffix='.html')
        f = open(self.redirection_page, 'w')
        test_url = windmill.get_test_url(windmill.settings['TEST_URL'])
        f.write(html_redirection.replace('{replace}', test_url))
        f.flush()
        f.close()

    def set_proxy_mac(self):
        """Set local Proxy"""
        self.netsetup_binary = windmill.settings['NETWORKSETUP_BINARY']
        interface_name = find_default_interface_name()
        uri = urlparse.urlparse(self.test_url)
        set_proxy_command = [self.netsetup_binary, '-setwebproxy',
         interface_name, '127.0.0.1',
         str(windmill.settings['SERVER_HTTP_PORT'])]
        dprint(getoutput(set_proxy_command))
        enable_proxy_command = [
         self.netsetup_binary, '-setwebproxystate',
         interface_name, 'on']
        dprint(getoutput(enable_proxy_command))
        if windmill.has_ssl:
            set_ssl_proxy_command = [
             self.netsetup_binary, '-setsecurewebproxy',
             interface_name, '127.0.0.1',
             str(windmill.settings['SERVER_HTTP_PORT'])]
        dprint(getoutput(set_proxy_command))
        enable_ssl_proxy_command = [self.netsetup_binary, '-setsecurewebproxystate',
         interface_name, 'on']
        dprint(getoutput(enable_proxy_command))
        self.create_redirect()
        self.interface_name = interface_name

    def unset_proxy_mac(self):
        getoutput([self.netsetup_binary, '-setwebproxystate', self.interface_name, 'off'])
        getoutput([self.netsetup_binary, '-setsecurewebproxystate', self.interface_name, 'off'])

    def set_proxy_windows(self):
        self.create_redirect()
        import ie
        self.ie_obj = ie.InternetExplorer()
        self.ie_obj.set_proxy()

    def unset_proxy_windows(self):
        self.ie_obj.unset_proxy()

    def start(self):
        """Start Safari"""
        if sys.platform == 'darwin':
            self.set_proxy_mac()
        elif sys.platform in ('cygwin', 'win32'):
            self.set_proxy_windows()
        if hasattr(sys.stdout, 'fileno'):
            kwargs = {'stdout': sys.stdout, 'stderr': sys.stderr, 'stdin': sys.stdin}
        else:
            kwargs = {'stdout': sys.__stdout__, 'stderr': sys.__stderr__, 'stdin': sys.stdin}
        self.p_handle = killableprocess.runCommand([self.safari_binary, self.redirection_page], **kwargs)
        logger.info([self.safari_binary, self.redirection_page])

    def kill(self, kill_signal=None):
        """Stop Safari"""
        if sys.platform == 'darwin':
            self.unset_proxy_mac()
        elif sys.platform in ('cygwin', 'win32'):
            self.unset_proxy_windows()
        try:
            self.p_handle.kill(group=True)
        except:
            logger.error('Cannot kill Safari')

    def stop(self):
        self.kill(signal.SIGTERM)

    def is_alive(self):
        if self.p_handle.poll() is None:
            return False
        else:
            return True