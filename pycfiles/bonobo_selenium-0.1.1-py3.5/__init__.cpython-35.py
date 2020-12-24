# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_selenium/__init__.py
# Compiled at: 2017-11-07 01:55:58
# Size of source mod 2**32: 1078 bytes
import selenium.webdriver
from bonobo_selenium._version import __version__
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'

def create_profile(use_tor=False):
    _profile = selenium.webdriver.FirefoxProfile()
    _profile.set_preference('toolkit.startup.max_resumed_crashes', '-1')
    if use_tor:
        _profile.set_preference('network.proxy.type', 1)
        _profile.set_preference('network.proxy.socks', '127.0.0.1')
        _profile.set_preference('network.proxy.socks_port', 9050)
    _profile.set_preference('general.useragent.override', USER_AGENT)
    return _profile


def create_browser(profile):
    _browser = selenium.webdriver.Firefox(profile)
    return _browser


def create_chrome_browser():
    browser = selenium.webdriver.Chrome()
    return browser


__all__ = [
 'USER_AGENT',
 '__version__',
 'create_browser',
 'create_profile']