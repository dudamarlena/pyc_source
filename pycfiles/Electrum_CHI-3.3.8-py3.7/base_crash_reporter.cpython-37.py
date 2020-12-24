# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/base_crash_reporter.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 5458 bytes
import asyncio, json, locale, traceback, subprocess, sys, os
from .version import ELECTRUM_VERSION
from . import constants
from .i18n import _
from .util import make_aiohttp_session
from .logging import describe_os_version, Logger

class BaseCrashReporter(Logger):
    report_server = 'https://crashhub.electrum.org'
    config_key = 'show_crash_reporter'
    issue_template = '<h2>Traceback</h2>\n<pre>\n{traceback}\n</pre>\n\n<h2>Additional information</h2>\n<ul>\n  <li>Electrum version: {app_version}</li>\n  <li>Python version: {python_version}</li>\n  <li>Operating system: {os}</li>\n  <li>Wallet type: {wallet_type}</li>\n  <li>Locale: {locale}</li>\n</ul>\n    '
    CRASH_MESSAGE = _('Something went wrong while executing Electrum-CHI.')
    CRASH_TITLE = _('Sorry!')
    REQUEST_HELP_MESSAGE = _('To help us diagnose and fix the problem, you can send us a bug report that contains useful debug information:')
    DESCRIBE_ERROR_MESSAGE = _('Please briefly describe what led to the error (optional):')
    ASK_CONFIRM_SEND = _('Do you want to send this report?')

    def __init__(self, exctype, value, tb):
        Logger.__init__(self)
        self.exc_args = (exctype, value, tb)

    def send_report(self, asyncio_loop, proxy, endpoint='/crash', *, timeout=None):
        if constants.net.GENESIS[-4:] not in ('4943', 'e26f'):
            if '.electrum.org' in BaseCrashReporter.report_server:
                raise Exception(_('Missing report URL.'))
        report = self.get_traceback_info()
        report.update(self.get_additional_info())
        report = json.dumps(report)
        coro = self.do_post(proxy, (BaseCrashReporter.report_server + endpoint), data=report)
        response = asyncio.run_coroutine_threadsafe(coro, asyncio_loop).result(timeout)
        return response

    async def do_post(self, proxy, url, data):
        async with make_aiohttp_session(proxy) as session:
            async with session.post(url, data=data) as resp:
                return await resp.text()

    def get_traceback_info(self):
        exc_string = str(self.exc_args[1])
        stack = traceback.extract_tb(self.exc_args[2])
        readable_trace = ''.join(traceback.format_list(stack))
        id = {'file':stack[(-1)].filename, 
         'name':stack[(-1)].name, 
         'type':self.exc_args[0].__name__}
        return {'exc_string':exc_string, 
         'stack':readable_trace, 
         'id':id}

    def get_additional_info(self):
        args = {'app_version':ELECTRUM_VERSION, 
         'python_version':sys.version, 
         'os':describe_os_version(), 
         'wallet_type':'unknown', 
         'locale':locale.getdefaultlocale()[0] or '?', 
         'description':self.get_user_description()}
        try:
            args['wallet_type'] = self.get_wallet_type()
        except:
            pass

        try:
            args['app_version'] = self.get_git_version()
        except:
            pass

        return args

    @staticmethod
    def get_git_version():
        dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        version = subprocess.check_output([
         'git', 'describe', '--always', '--dirty'],
          cwd=dir)
        return str(version, 'utf8').strip()

    def get_report_string(self):
        info = self.get_additional_info()
        info['traceback'] = ''.join((traceback.format_exception)(*self.exc_args))
        return (self.issue_template.format)(**info)

    def get_user_description(self):
        raise NotImplementedError

    def get_wallet_type(self):
        raise NotImplementedError


def trigger_crash():

    class TestingException(Exception):
        pass

    def crash_test():
        raise TestingException('triggered crash for testing purposes')

    import threading
    t = threading.Thread(target=crash_test)
    t.start()