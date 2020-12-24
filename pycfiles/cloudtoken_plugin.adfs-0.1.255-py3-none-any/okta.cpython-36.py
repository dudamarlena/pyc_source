# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aloughran/Code/OpenSourceProjects/cloudtoken-plugin.okta/venv/lib/python3.6/site-packages/cloudtoken_plugin/okta.py
# Compiled at: 2018-12-17 03:31:10
# Size of source mod 2**32: 5204 bytes
__doc__ = "OKTA plugin for cloudtoken.\n\nYou will need to add the key 'okta_url' with the value being the URL for your OKTA IdP, for example:\n\nokta_url: !!str 'https://{{example}}.okta.com\nAuthor: Andy Loughran (andy@lockran.com)\n"
import argparse, json, re, tkinter, tkinter.simpledialog
from os import system
from platform import system as platform
from urllib import parse
import requests
from bs4 import BeautifulSoup

def grab_focus():
    """Grabs focus on OSX when using the GUI

    Returns:
        null
    """
    if platform() == 'Darwin':
        system('/usr/bin/osascript -e \'tell app "Finder" to set frontmost of process "Python" to true\' ')


class Plugin(object):
    """Plugin"""

    def __init__(self, config):
        """
        Sets up a new CloudToken OKTA Plugin instance,
        using variables defined in the self properties below.

        Arguments:
            config -- parsed config.yml file (provided by cloudtoken)
        """
        self._config = config
        self._name = 'okta'
        self._description = 'Authenticate against OKTA.'
        self._authurl = 'api/v1/authn'
        self._headers = {'Accept':'application/json', 
         'Content-Type':'application/json'}
        self._content_options = {'multiOptionalFactorEnroll':'true', 
         'warnBeforePasswordExpired':'true'}
        try:
            self._url = config['okta_url']
            re.search('(https?://[\\w\\-.]+)/', self._url).group(1)
        except KeyError:
            print("Configuration key 'okta_url' not found. Exiting.")
            exit(1)
        except AttributeError:
            print("Configuration key 'okta_url' value does not seem to be a http(s) URL. Exiting.")
            exit(1)

    def __str__(self):
        """Return the self string"""
        return __file__

    @staticmethod
    def unset(args):
        """Framework function"""
        pass

    @staticmethod
    def arguments(defaults):
        """parses the arguments passed to the plugin"""
        parser = argparse.ArgumentParser()
        return parser

    def execute(self, data, args, flags):
        """The main execution of the program.

        Initial call to authenticate against OKTA.
        Second call with MFA to get Token.
        """
        url = self._url
        try:
            gui = self._config['gui']
        except KeyError:
            gui = False

        if gui is True:
            root = tkinter.Tk()
            root.title('CloudToken')
            root.withdraw()
            root.overrideredirect(True)
            root.geometry('0x0+0+0')
            if platform() == 'Darwin':
                system('/usr/bin/osascript -e \'tell app "Finder" to set frontmost of process "Python" to true\' ')
        session = requests.session()
        content = {'username':args.username, 
         'password':args.password,  'options':self._content_options}
        full_url = 'https://{}/{}'.format(parse.urlparse(url).netloc, self._authurl)
        response_data = session.post(full_url, headers=(self._headers), data=(json.dumps(content)))
        saml_response = json.loads(response_data.text)
        try:
            token = saml_response['stateToken']
            auth_id = saml_response['_embedded']['factors'][0]['id']
        except KeyError:
            print('There has been an authentication error')
            exit(1)

        verify_url = '{}/factors/{}/verify'.format(full_url, auth_id)
        verification_content = {'stateToken': token}
        if gui is False:
            selection = input('Please enter your MFA code: ')
            verification_content['passCode'] = selection
        else:
            if gui is True:
                root.call('wm', 'attributes', '.', '-topmost', '1')
                grab_focus()
                verification_content['passCode'] = tkinter.simpledialog.askstring('MFA Code', 'Enter your MFA code')
        verification_response = session.post(verify_url,
          headers=(self._headers),
          data=(json.dumps(verification_content)))
        session_token = json.loads(verification_response.text)['sessionToken']
        saml_url = '{}?sessionToken={}'.format(url, session_token)
        saml_response = session.get(saml_url)
        soup = BeautifulSoup(saml_response.text, 'html.parser')
        saml = soup.find('input', attrs={'name': 'SAMLResponse'})
        response_data = saml['value']
        data.append({'plugin':self._name,  'data':response_data})
        return data