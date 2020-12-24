# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/meya_config.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
import fnmatch, os
from meya_cli.path_utils import has_hidden_component
MEYA_CONFIG_FILE = 'meya-config.yaml'
REST_API_VERSION = '1.0.0'
USER_AGENT_STRING = 'meya-cli'
DEFAULT_API_ROOT = 'https://api.meya.ai/'
DEFAULT_WATCH_COMMAND_DELAY = 2
DEFAULT_AUTO_SYNC_FILES = ('cms/*.yaml', 'cms/*.csv', 'flows/*.yaml', 'components/*.py',
                           'components/*.js', 'intents.yaml', 'requirements.txt')

class MeyaConfig(object):

    def __init__(self, root_dir, api_key, bot_id, api_root=None, ignore_files=[], ignore_dot_files=True, autosync_files=DEFAULT_AUTO_SYNC_FILES, verbose=False, watch_command_delay=DEFAULT_WATCH_COMMAND_DELAY):
        assert isinstance(ignore_files, list)
        for ignore_pattern in ignore_files:
            assert isinstance(ignore_pattern, (str, unicode))

        self.root_dir = root_dir
        self.api_key = api_key
        self.api_root = api_root or DEFAULT_API_ROOT
        self.bot_id = bot_id
        self.ignore_files = ignore_files
        self.ignore_dot_files = ignore_dot_files
        self.autosync_files = autosync_files
        self.verbose = verbose
        self.watch_command_delay = watch_command_delay

    def should_ignore_path(self, path):
        meya_path = os.path.relpath(path, start=self.root_dir)
        rel_path = os.path.relpath(path)
        for ignore_pattern in self.ignore_files:
            if fnmatch.fnmatch(meya_path, ignore_pattern):
                print('SKIPPING ' + rel_path + " due to 'ignore_files' rule '" + ignore_pattern + "'.")
                return True

        if meya_path.startswith('..'):
            print('SKIPPING ' + rel_path + '; outside of project folder.')
            return True
        if self.ignore_dot_files and has_hidden_component(meya_path):
            if self.verbose:
                print('SKIPPING ' + rel_path + '; ignoring hidden (dot prefix) files.')
            return True
        return False

    def should_upload_path(self, path):
        meya_path = os.path.relpath(path, start=self.root_dir)
        rel_path = os.path.relpath(path)
        if self.should_ignore_path(path):
            return False
        if meya_path == MEYA_CONFIG_FILE:
            print('SKIPPING ' + rel_path + '; not uploading local config file.')
            return False
        if not os.path.isfile(path):
            if not os.path.exists(path):
                print('SKIPPING ' + rel_path + '; no local copy found.')
            else:
                print('SKIPPING ' + rel_path + '; not a regular file.')
            return False
        return True

    def path_matches_autosync_patterns(self, path):
        meya_path = os.path.relpath(path, start=self.root_dir)
        for autosync_pattern in self.autosync_files:
            if fnmatch.fnmatch(meya_path, autosync_pattern):
                return True

        return False


def parse_meya_config(root_dir, local_path):
    import poyo
    with open(local_path, 'r') as (f):
        definition = poyo.parse_string(f.read())
    api_key = definition['api_key']
    bot_id = definition.get('bot_id')
    api_root = definition.get('api_root', DEFAULT_API_ROOT)
    ignore_files = definition.get('ignore_files', [])
    ignore_dot_files = definition.get('ignore_dot_files', True)
    autosync_files = definition.get('autosync_files', DEFAULT_AUTO_SYNC_FILES)
    verbose = definition.get('verbose', False)
    watch_command_delay = definition.get('watch_command_delay', DEFAULT_WATCH_COMMAND_DELAY)
    return MeyaConfig(root_dir, api_key, bot_id, api_root, ignore_files, ignore_dot_files, autosync_files, verbose, watch_command_delay)


def find_meya_config(start_path):
    """
    Traverse path up parent directories until a directory
    with MEYA_CONFIG_FILE is found.
    """
    root_dir = start_path
    try:
        while True:
            local_path = os.path.join(root_dir, MEYA_CONFIG_FILE)
            if os.path.isfile(local_path):
                return parse_meya_config(root_dir, local_path)
            new_root = os.path.dirname(root_dir)
            if new_root == root_dir:
                break
            root_dir = new_root

    except IOError:
        pass

    return