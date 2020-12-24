# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\config.py
# Compiled at: 2020-03-18 12:09:09
# Size of source mod 2**32: 5173 bytes
import reapy
from reapy.errors import OutsideREAPERError
from reapy.reascripts import activate_reapy_server
from configparser import ConfigParser
from collections import OrderedDict
import json, os, shutil
REAPY_SERVER_PORT = 2306
WEB_INTERFACE_PORT = 2307

class CaseInsensitiveDict(OrderedDict):
    __doc__ = 'OrderedDict with case-insensitive keys.'

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._dict = OrderedDict(*args, **kwargs)
        for key, value in self._dict.items():
            self._dict[key.lower()] = value

    def __contains__(self, key):
        return key.lower() in self._dict

    def __getitem__(self, key):
        return self._dict[key.lower()]

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._dict[key.lower()] = value


class Config(ConfigParser):
    __doc__ = 'Parser for REAPER .ini file.'

    def __init__(self):
        super(Config, self).__init__(strict=False, delimiters='=', dict_type=CaseInsensitiveDict)
        self.optionxform = str
        self.ini_file = reapy.get_ini_file()
        self.read((self.ini_file), encoding='utf8')

    def write(self):
        before_reapy_file = self.ini_file + '.before-reapy.bak'
        if not os.path.exists(before_reapy_file):
            shutil.copy(self.ini_file, before_reapy_file)
        shutil.copy(self.ini_file, self.ini_file + '.bak')
        with open((self.ini_file), 'w', encoding='utf8') as (f):
            super(Config, self).write(f, False)


def create_new_web_interface(port):
    """
    Create a Web interface in REAPER at a specified port.

    It is added by writing a line directly in REAPER .ini file. Thus
    it will only be available on restart.

    Parameters
    ----------
    port : int
        Web interface port.
    """
    config = Config()
    csurf_count = int(config['reaper'].get('csurf_cnt', '0'))
    csurf_count += 1
    config['reaper']['csurf_cnt'] = str(csurf_count)
    key = 'csurf_{}'.format(csurf_count - 1)
    config['reaper'][key] = "HTTP 0 {} '' 'index.html' 0 ''".format(port)
    config.write()


def delete_web_interface(port):
    """
    Delete Web interface listening to a specified port.

    It is deleted by writing a line directly in REAPER .ini file. Thus
    it will only be deleted on restart.

    Parameters
    ----------
    port : int
        Web interface port.
    """
    config = Config()
    csurf_count = int(config['reaper']['csurf_cnt'])
    for i in range(csurf_count):
        string = config['reaper']['csurf_{}'.format(i)]
        if string.startswith('HTTP') and string.split(' ')[2] == str(port):
            webi_index = i

    del config['reaper']['csurf_{}'.format(webi_index)]
    for i in range(webi_index, csurf_count - 1):
        next_line = config['reaper']['csurf_{}'.format(i + 1)]
        config['reaper']['csurf_{}'.format(i)] = next_line

    config['reaper']['csurf_cnt'] = str(csurf_count - 1)
    config.write()


def disable_dist_api():
    """
    Disable distant API.

    Delete ``reapy`` Web interface, and remove the ReaScript
    ``reapy.reascripts.activate_reapy_server`` from the
    Actions list.
    """
    if not reapy.is_inside_reaper():
        raise OutsideREAPERError
    delete_web_interface(WEB_INTERFACE_PORT)
    reascript_path = get_activate_reapy_server_path()
    reapy.remove_reascript(reascript_path)
    message = 'reapy will be disabled as soon as you restart REAPER.'
    reapy.show_message_box(message)


def enable_dist_api():
    """
    Enable distant API.

    Create a Web interface and add the ReaScript
    ``reapy.reascripts.activate_reapy_server`` to the Actions list.
    """
    if not reapy.is_inside_reaper():
        raise OutsideREAPERError
    create_new_web_interface(WEB_INTERFACE_PORT)
    reascript_path = get_activate_reapy_server_path()
    action_id = reapy.add_reascript(reascript_path)
    command_name = json.dumps(reapy.get_command_name(action_id))
    section, key, value = 'reapy', 'activate_reapy_server', command_name
    reapy.set_ext_state(section, key, value, persist=True)
    message = 'reapy successfully enabled!\n\nPlease restart REAPER.\n\nYou will then be able to import reapy from the outside.'
    reapy.show_message_box(message)


def get_activate_reapy_server_path():
    """Return path to the ``activate_reapy_server`` ReaScript."""
    script_path = os.path.abspath(activate_reapy_server.__file__)
    if script_path.endswith(('.pyc', '.pyw')):
        script_path = script_path[:-1]
    return script_path