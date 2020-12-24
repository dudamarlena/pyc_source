# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/tools/setup/lib/setup.py
# Compiled at: 2016-12-03 14:53:38
# Size of source mod 2**32: 9597 bytes
"""
The setup module handles all Setup related tasks:

Install/remove plugins and their dependencies
Update OF and its dependencies using pip
Manage folder location
Manage startup scripts
Be scriptable
Create a settings file format
Manage databases
Handle certificate (for now, or should they be in the db?)
Update Plugins using git

Deps: dulwich

"""
import os, sys, tempfile
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import json
from distlib.compat import ZipFile
from dulwich import porcelain
from of.common.dictionaries import set_property_if_in_dict
from of.common.internal import not_implemented
from of.common.settings import JSONXPath
default_config_repo = 'https://github.com/OptimalBPM/of-config.git'
default_of_install = {'installLocation': '~/of/', 
 'pluginsFolder': 'plugins', 
 'plugins': {'admin': {'url': 'https://github.com/OptimalBPM/of-admin.git', 
                       'branch': 'main'}}}

class Setup:
    __doc__ = '\n    The setup class handles installing and setting up an OF-based system.\n    '
    setup_location = None
    install_location = None
    plugins_folder = None
    install_repository_url = None
    plugins = None

    def __init__(self, _setup_definition=None, _setup_filename=None, _default_of_install=False, *args, **kw):
        if _default_of_install:
            self.read_settings(default_of_install)
        else:
            if _setup_definition is not None:
                self.read_settings(_setup_definition)
            elif _setup_filename is not None:
                self.load_from_file(_setup_filename=_setup_filename)

    def load_from_file(self, _setup_filename):
        with open(_setup_filename, 'r') as (f):
            _setup_definition = json.load(f)
        self.read_settings(_setup_definition)

    def as_dict(self):
        return {'installLocation': self.install_location, 
         'pluginsFolder': self.plugins_folder, 
         'installRepositoryUrl': self.install_repository_url, 
         'plugins': self.plugins}

    def load_install(self, _install_folder):
        _exp_path = os.path.expanduser(_install_folder)
        self.plugins_folder = None
        if os.path.exists(os.path.join(_exp_path, 'config.json')):
            _config = JSONXPath(os.path.join(_exp_path, 'config.json'))
            self.plugins_folder = _config.get_path('broker/pluginsFolder', _default='plugins')
        self.install_repository_url = 'Fetching remotes from GIT repo not implemented'
        self.install_location = _install_folder
        if self.plugins_folder is None:
            self.plugins_folder = os.path.join(_exp_path, 'plugins')
        self.plugins = {}
        if not os.path.exists(self.plugins_folder):
            pass
        else:
            _plugin_names = os.listdir(self.plugins_folder)
            for _plugin_name in _plugin_names:
                _curr_plugin_folder = os.path.join(self.plugins_folder, _plugin_name)
                if os.path.isdir(_curr_plugin_folder) and _plugin_name[0:2] != '__' and _plugin_name[0] != '.':
                    _definitions = JSONXPath(os.path.join(_curr_plugin_folder, 'definitions.json'))
                    _description = _definitions.get('plugins/' + _plugin_name + '/description', 'No description found in plugin definition')
                    self.plugins[_plugin_name] = {'name': _plugin_name, 'description': _description}

    def read_settings(self, _setup_definition):
        set_property_if_in_dict(self, 'install_location', _setup_definition, _convert_underscore=True)
        set_property_if_in_dict(self, 'plugins_folder', _setup_definition, _convert_underscore=True, _default_value='plugins')
        set_property_if_in_dict(self, 'install_repository_url', _setup_definition, _default_value=default_config_repo, _convert_underscore=True)
        set_property_if_in_dict(self, 'plugins', _setup_definition, _convert_underscore=True)

    @not_implemented
    def uninstall_config(self):
        pass

    @not_implemented
    def uninstall_plugin(self):
        pass

    @not_implemented
    def uninstall(self):
        pass

    def install_config(self):
        if self.install_location is None:
            _folder_location = os.path.expanduser('~/of')
        else:
            _folder_location = os.path.expanduser(self.install_location)
        if not os.path.exists(_folder_location):
            print('\nInstalling configuration and startup scripts at:\n' + _folder_location)
            print('-----------------------------------------------------')
            print('Cloning ' + self.install_repository_url + ' into ' + _folder_location)
            _repo = porcelain.clone(source=self.install_repository_url, target=_folder_location, checkout=True)
            _config = _repo.get_config()
            _config.set(('remote "origin"'.encode('ascii'),), 'url'.encode('ascii'), self.install_repository_url.encode('ascii'))
            _config.write_to_path()
            print('Done.')
        else:
            raise Exception('Error installing the configuration files at "' + _folder_location + '", directory already exists.')

    def install_plugin_binaries(self, _folder):
        try:
            with open(os.path.join(_folder, 'definitions.json'), 'r') as (f):
                _settings = json.load(f)
            try:
                for _curr_plugin_name, _curr_plugin_value in _settings['plugins'].items():
                    if 'binaries' in _curr_plugin_value:
                        print('\nInstalling and expanding compressed content...')
                        print('----------------------------------------------')
                        for _curr_binary in _curr_plugin_value['binaries']:
                            _source_file = urlopen(_curr_binary['url'])
                            _tempfile = tempfile.TemporaryFile(mode='w+b')
                            sys.stdout.write('Downloading ' + _curr_binary['url'] + ' (' + str(_source_file.info()['Content-Length']) + ' bytes) into temporary area...')
                            sys.stdout.flush()
                            _tempfile.write(_source_file.read())
                            print('..done.')
                            _target_folder = os.path.join(_folder, _curr_binary['target'])
                            sys.stdout.write('Extracting all files into ' + _target_folder)
                            sys.stdout.flush()
                            with ZipFile(_tempfile) as (_zipfile):
                                _zipfile.extractall(path=_target_folder)
                            _tempfile.close()
                            print('..done.')

            except HTTPError as e:
                print('An error occured when downloading a binary (' + _curr_binary['url'] + '): ' + str(e))
            except URLError as e:
                print('An URL-related error occurred when downloading binary (' + _curr_binary['url'] + '): ' + str(e))

        except FileNotFoundError:
            print('No definition file found, ignoring installing plugin binaries in ' + _folder)
        except Exception as e:
            print('An error occurred installing binaries in ' + _folder + ':' + str(e))

    def install_plugin(self, _plugins_location, _plugin_name, _plugin_info):
        _curr_target = os.path.join(_plugins_location, _plugin_name)
        print('Cloning ' + _plugin_info['url'] + ' into ' + _curr_target)
        _repo = porcelain.clone(source=_plugin_info['url'], target=_curr_target, checkout=True)
        _config = _repo.get_config()
        _config.set(('remote "origin"'.encode('ascii'),), 'url'.encode('ascii'), _plugin_info['url'].encode('ascii'))
        _config.write_to_path()
        print('Done.')
        self.install_plugin_binaries(_curr_target)

    def install_plugins(self):
        if self.plugins_folder is None:
            _plugins_location = os.path.join(os.path.expanduser(self.install_location), 'plugins')
        else:
            if not os.path.isabs(self.plugins_folder):
                _plugins_location = os.path.join(os.path.expanduser(self.install_location), self.plugins_folder)
            else:
                _plugins_location = os.path.expanduser(self.plugins_folder)
        if not os.path.exists(_plugins_location):
            os.mkdir(_plugins_location)
        print('\nInstall plugins at: \n' + _plugins_location)
        for _plugin_name, _plugin_info in self.plugins.items():
            self.install_plugin(_plugins_location, _plugin_name, _plugin_info)

    def install(self):
        self.install_config()
        self.install_plugins()
        print('\nSetup is complete, system is installed.')