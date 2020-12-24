# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/browser/ie.py
# Compiled at: 2011-02-09 04:10:54
import windmill, exceptions, os, sys, shutil, time, signal, killableprocess, logging
if sys.platform == 'win32':
    import _winreg as wreg
if sys.platform == 'cygwin':
    import cygwinreg as wreg
logger = logging.getLogger(__name__)

class InternetExplorer(object):
    registry_modifications = {'MigrateProxy': {'type': wreg.REG_DWORD, 'new_value': 1}, 'ProxyEnable': {'type': wreg.REG_DWORD, 'new_value': 1}, 'ProxyHttp1.1': {'type': wreg.REG_DWORD, 'new_value': 1}, 'ProxyServer': {'type': wreg.REG_SZ}}

    def __init__(self):
        self.proxy_port = windmill.settings['SERVER_HTTP_PORT']
        self.test_url = windmill.get_test_url(windmill.settings['TEST_URL'])
        self.registry_modifications['ProxyServer']['new_value'] = 'http=127.0.0.1:%s' % self.proxy_port
        if windmill.has_ssl:
            self.registry_modifications['ProxyServer']['new_value'] += ';https=127.0.0.1:%s' % self.proxy_port
        self.reg = wreg.OpenKey(wreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings', 0, wreg.KEY_ALL_ACCESS)
        for (key, value) in self.registry_modifications.items():
            try:
                result = wreg.QueryValueEx(self.reg, key)
                self.registry_modifications[key]['previous_value'] = result[0]
            except exceptions.WindowsError:
                self.registry_modifications[key]['previous_value'] = None

        self.ie_binary = windmill.settings['IE_BINARY']
        self.cmd = [self.ie_binary, '-private', self.test_url]
        return

    def set_proxy(self):
        for (key, value) in self.registry_modifications.items():
            wreg.SetValueEx(self.reg, key, 0, value['type'], value['new_value'])

    def unset_proxy(self):
        for (key, value) in self.registry_modifications.items():
            if value['previous_value'] is not None:
                wreg.SetValueEx(self.reg, key, 0, value['type'], value['previous_value'])
            else:
                wreg.DeleteValue(self.reg, key)

        return

    def start(self):
        """Start IE"""
        self.set_proxy()
        if hasattr(sys.stdout, 'fileno'):
            kwargs = {'stdout': sys.stdout, 'stderr': sys.stderr, 'stdin': sys.stdin}
        else:
            kwargs = {'stdout': sys.__stdout__, 'stderr': sys.__stderr__, 'stdin': sys.stdin}
        self.p_handle = killableprocess.Popen(self.cmd, **kwargs)

    def stop(self):
        """Stop IE"""
        self.unset_proxy()
        try:
            self.p_handle.kill(group=True)
        except:
            logger.error('Cannot kill Internet Explorer')

    def is_alive(self):
        if self.p_handle.poll() is None:
            return False
        else:
            try:
                self.p_handle.kill(group=True)
                return True
            except exceptions.OSError:
                return False

            return