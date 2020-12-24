# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/mapscookiegettercli/mapscookiegettercli/library/cookiegetter.py
# Compiled at: 2019-06-16 09:01:32
# Size of source mod 2**32: 8493 bytes
"""
Main code for cookiegetter

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging, sys, pickle
from pathlib import Path
from time import sleep
from requests import Session
from selenium.common.exceptions import NoSuchWindowException
from mapscookiegettercli.mapscookiegettercliexceptions import UnsupportedOS, UnsupportedDefaultBrowser
from mapscookiegettercli.browsers import Chrome, Firefox, IE, Edge
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '04-03-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos', 'https://github.com/Protonex']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'cookiegetter'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())
MAPS_LOGIN = 'https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2Fmaps%2F%4040.7484986%2C-73.9857129%2C15z%3Fhl%3Den&service=local&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
LOGGED_IN_HEURISTIC = 'Find local businesses, view maps and get driving directions in Google Maps.'

class CookieGetter:
    __doc__ = 'Object able to retrieve the cookies from an interactive login session to a google maps service'

    def __init__(self):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix=(self.__class__.__name__))
        self._logger = logging.getLogger(logger_name)
        self.os = self._identify_os()
        self._logger.info('Identified OS as %s', self.os)
        self.default_browser = self._identify_default_browser(self.os)
        self._logger.info('Identified default browser as %s', self.default_browser)

    @staticmethod
    def _identify_os():
        platforms = {'linux':'linux', 
         'linux1':'linux', 
         'linux2':'linux', 
         'darwin':'mac', 
         'win32':'windows'}
        platform = sys.platform
        if platform not in platforms:
            raise UnsupportedOS(platform)
        return platforms.get(platform)

    def _identify_default_browser(self, identified_os):
        browser = getattr(self, '_identify_browser_{os}'.format(os=identified_os))()
        if browser == 'unknown':
            raise UnsupportedDefaultBrowser
        return browser

    @staticmethod
    def _identify_browser_mac():
        from plistlib import load, FMT_BINARY
        supported_browsers = ('firefox', 'chrome')
        default_browser_plist_path = '~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist'
        path = Path(default_browser_plist_path).expanduser()
        with open(path, 'rb') as (plist):
            settings = load(plist, fmt=FMT_BINARY)
        browser_setting = next((setting.get('LSHandlerRoleAll') for setting in settings.get('LSHandlers') if setting.get('LSHandlerContentType') == 'public.html'), 'Unknown')
        browser = next((browser for browser in supported_browsers if browser in browser_setting.lower()), 'unknown')
        return browser

    @staticmethod
    def _identify_browser_windows():
        from winreg import HKEY_CURRENT_USER, HKEY_CLASSES_ROOT, OpenKey, QueryValueEx
        supported_browsers = ('firefox', 'chrome', 'edge', 'ie')
        default_browser_registry_path = 'Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\https\\UserChoice'
        with OpenKey(HKEY_CURRENT_USER, default_browser_registry_path) as (key):
            program_id = QueryValueEx(key, 'ProgId')[0]
        browser = next((browser for browser in supported_browsers if browser in program_id.lower()), None)
        if browser:
            return browser
        with OpenKey(HKEY_CLASSES_ROOT, '{program_id}\\Application'.format(program_id=program_id)) as (key):
            application_name = QueryValueEx(key, 'ApplicationName')[0]
        browser = next((browser for browser in supported_browsers if browser in application_name.lower()), 'unknown')
        return browser

    @staticmethod
    def _identify_browser_linux():
        from subprocess import Popen, PIPE
        supported_browsers = ('firefox', 'chrome')
        command = ['xdg-settings', 'get', 'default-web-browser']
        try:
            get_browser_command = Popen(command, stdout=PIPE, stderr=PIPE)
        except FileNotFoundError:
            print('Could not execute xdg-settings, probably unsupported version of linux.')
            return 'unknown'
        else:
            output, _ = get_browser_command.communicate()
            browser = next((browser for browser in supported_browsers if browser in output.decode('utf-8')), 'unknown')
            return browser

    def _get_driver(self):
        browsers = {'chrome':Chrome,  'firefox':Firefox, 
         'ie':IE, 
         'edge':Edge}
        return browsers.get(self.default_browser)()

    def run(self, cookie_file_name='location_sharing.cookies'):
        """Executes the process and saves the cookies

        Args:
            cookie_file_name (str): The path and name of the exported cookie file

        Returns:

        """
        driver = self._get_driver()
        self._logger.info('Starting interactive login process.')
        try:
            driver.get(MAPS_LOGIN)
            while LOGGED_IN_HEURISTIC not in driver.page_source:
                sleep(0.5)

            session = self._get_session(driver)
            self._save_cookies(session, cookie_file_name)
            self._logger.info('Terminating browser session.')
            driver.close()
            driver.quit()
        except NoSuchWindowException:
            self._logger.warning('Window disappeared, seems like it was closed manually')

    def _get_session(self, driver):
        self._logger.info('Log in successful, getting session cookies.')
        session = Session()
        self._logger.info('Transferring cookies to a requests session.')
        for cookie in driver.get_cookies():
            for invalid in ('httpOnly', 'expiry'):
                try:
                    del cookie[invalid]
                except KeyError:
                    pass

            (session.cookies.set)(**cookie)

        return session

    def _save_cookies(self, session, file_name):
        self._logger.info('Saving the requests session to pickled file "%s".', file_name)
        with open(file_name, 'wb') as (ofile):
            pickle.dump(session.cookies, ofile)