# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/delucks/.pyenv/versions/3.8.1/lib/python3.8/site-packages/todo/configuration.py
# Compiled at: 2020-02-16 21:27:11
# Size of source mod 2**32: 5184 bytes
import os, platform, yaml
from todo.exceptions import GTDException

class Configuration:
    __doc__ = 'hold global configuration for this application. This class has required\n    arguments of the properties we need to connect to the Trello API and some\n    other properties that modify global state during each run\n\n    Possible configuration properties:\n        Age of cards to show in yellow/red\n        Color of labels\n        "Primary color" for UI elements, maybe hardcoded secondary colors too\n    '

    def __init__(self, api_key, api_secret, oauth_token, oauth_token_secret, **kwargs):
        self.api_key = api_key
        self.api_secret = api_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.board = kwargs.get('board', None)
        self.test_board = kwargs.get('test_board', None)
        self.banner = kwargs.get('banner', True)
        self.color = kwargs.get('color', True)
        self.inbox_list = kwargs.get('inbox_list', None)
        self.prompt_for_open_attachments = kwargs.get('prompt_for_open_attachments', None)
        self.prompt_for_untagged_cards = kwargs.get('prompt_for_untagged_cards', None)

    def __repr__(self):
        return '\n'.join([
         'GTD Configuration:',
         '  API key: ' + self.api_key,
         '  API secret: ' + self.api_secret,
         '  OAuth token: ' + self.oauth_token,
         '  OAuth secret: ' + self.oauth_token_secret,
         f"  Primary board: {self.board}",
         f"  Inbox list: {self.inbox_list}",
         f"  Banner? {self.banner}",
         f"  Use ANSI color? {self.color}",
         '  Prompt for:',
         f"    Untagged cards? {self.prompt_for_untagged_cards}",
         f"    Opening attachments? {self.prompt_for_open_attachments}"])

    def __str__(self):
        return repr(self)

    @staticmethod
    def suggest_config_location():
        """Do some platform detection and suggest a place for the users' config file to go"""
        system = platform.system()
        if system == 'Windows':
            print('gtd.py support for Windows is rudimentary to none. Try to put your config file in $HOME/.gtd.yaml and run the script again')
            raise GTDException(0)
        else:
            if system == 'Darwin':
                preferred_location = os.path.expanduser('~/Library/Application Support/gtd/gtd.yaml')
            else:
                if system == 'Linux':
                    preferred_location = os.path.expanduser('~/.config/gtd/gtd.yaml')
                else:
                    preferred_location = os.path.expanduser('~/.gtd.yaml')
        return preferred_location

    @staticmethod
    def all_config_locations():
        return [os.path.expanduser(x) for x in ('~/.gtd.yaml', '~/.config/gtd/gtd.yaml',
                                                '~/Library/Application Support/gtd/gtd.yaml',
                                                '~/.local/etc/gtd.yaml', '~/.local/etc/gtd/gtd.yaml')]

    @staticmethod
    def find_config_file():
        for possible_loc in Configuration.all_config_locations():
            if os.path.isfile(possible_loc):
                return possible_loc
        else:
            raise GTDException(1)

    @staticmethod
    def from_file(filename=None):
        if filename is None:
            filename = Configuration.find_config_file()
        with open(filename, 'r') as (config_yaml):
            file_config = yaml.safe_load(config_yaml)
        for prop in ('api_key', 'api_secret', 'oauth_token', 'oauth_token_secret'):
            if file_config.get(prop, None) is not None:
                continue
            else:
                print(f"A required property {prop} in your configuration was not found!")
                print(f"Check the file {filename}")
                raise GTDException(1)
        else:
            return Configuration((file_config['api_key']),
              (file_config['api_secret']),
              (file_config['oauth_token']),
              (file_config['oauth_token_secret']),
              board=(file_config.get('board', None)),
              test_board=(file_config.get('test_board', None)),
              color=(file_config.get('color', True)),
              banner=(file_config.get('banner', False)),
              inbox_list=(file_config.get('inbox_list', None)),
              prompt_for_open_attachments=(file_config.get('prompt_for_open_attachments', False)),
              prompt_for_untagged_cards=(file_config.get('prompt_for_untagged_cards', True)))