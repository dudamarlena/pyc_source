# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/browser/chrome.py
# Compiled at: 2011-04-09 01:50:00
import commands, tempfile, logging, signal, subprocess, sys, os
if not sys.version.startswith('2.4'):
    import urlparse
else:
    from windmill.tools import urlparse_25 as urlparse
import windmill
logger = logging.getLogger(__name__)
import safari

class Chrome(safari.Safari):

    def __init__(self):
        self.chrome_binary = windmill.settings['CHROME_BINARY']
        self.test_url = windmill.settings['TEST_URL']

    def unset_proxy_mac(self):
        commands.getoutput((' ').join([self.netsetup_binary, '-setwebproxystate', '"' + self.interface_name + '"', 'off']))

    def get_chrome_command(self):
        tmp_profile = tempfile.mkdtemp(suffix='.mozrunner')
        chrome_options = [
         '--user-data-dir=' + tmp_profile, '--temp-profile', '--disable-popup-blocking', '--no-first-run', '--proxy-server=' + '127.0.0.1:' + str(windmill.settings['SERVER_HTTP_PORT']), '--homepage', self.test_url + '/windmill-serv/start.html']
        return [self.chrome_binary] + chrome_options

    def start(self):
        """Start Chrome"""
        if hasattr(sys.stdout, 'fileno'):
            kwargs = {'stdout': sys.stdout, 'stderr': sys.stderr, 'stdin': sys.stdin}
        else:
            kwargs = {'stdout': sys.__stdout__, 'stderr': sys.__stderr__, 'stdin': sys.stdin}
        command = self.get_chrome_command()
        self.p_handle = subprocess.Popen(command, **kwargs)
        logger.info(command)

    def kill(self, kill_signal=None):
        """Stop Chrome"""
        if sys.version < '2.6':
            raise Exception("Kill doesn't work for Chrome on Python version pre-2.6")
        try:
            self.p_handle.kill()
        except:
            logger.exception('Cannot kill Chrome')