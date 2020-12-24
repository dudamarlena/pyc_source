# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pykaryote/utils/globals.py
# Compiled at: 2013-08-30 10:09:51
""" Globals loads settings from simulation configuration files.

Settings are loaded into an object called ``settings``
Typical usage::
    from pykaryote.utils.globals import settings as gv
    gv.init_globals(path_to_sim_cfg)
    x = gv.generation_limit

Configuration files have a weird, hackish syntax as a result of poor design
decisions early on. They are a mixture of INI and psudo-json. For more
information on simulation configuration file format, see the section of
that name in the reference documentation.

Ideally, config files would be converted to use pure JSON, but then backwards
compatibility with old config files would be lost.
"""
import ConfigParser as configparser, pkg_resources, json, os.path, re

def _parse_json_snippet(json_snippet):
    """Interprets a string as a snippet of json code.

    This allows json which is not wrapped as a full object to be loaded.
    """
    return json.loads(('{{"val": {} }}').format(json_snippet))['val']


def _read_config(config, dct=None):
    """Reads settings from a ConfigParser and returns a dict of option=value.

    Args:
        ``config`` (RawConfigParser): A RawConfigParser instance holding data
            from a sim.cfg file.
        ``dct`` (dict): A dictionary in which to store settings. If None,
            a dictionary is created.
    """
    if dct is not None:
        settings_dict = dct
    else:
        settings_dict = {}
    for section in config.sections():
        if section == 'runtime':
            recorded_actions = {}
            gens = [ g for g in config.options(section) ]
            for gen in gens:
                action_list = _parse_json_snippet(config.get(section, gen))
                recorded_actions[int(gen[3:])] = action_list

            if 'recorded_actions' not in settings_dict:
                settings_dict['recorded_actions'] = recorded_actions
            else:
                raise RuntimeError('Config file contains duplicate option: recorded_actions')
        for name, value in config.items(section):
            if name not in settings_dict:
                try:
                    val = value.replace('(', '[').replace(')', ']').replace('True', 'true').replace('False', 'false')
                    val = re.sub('^\\.(\\d)', '0.\\1', val)
                    val = re.sub('([,\\s\\[\\]])\\.(\\d)', '\\1 0.\\2', val)
                    value = _parse_json_snippet(val)
                except ValueError:
                    pass

                settings_dict[name] = value
            else:
                raise RuntimeError(('Configuration file contains duplicate values for option: {}').format(name))

    return settings_dict


class SettingsMetaclass(type):
    """Creates the SettingsNamespace class.

    Creates and initializes attributes from the master configuration file.
    """

    def __new__(cls, name, bases, dct):
        config_parser = configparser.RawConfigParser()
        with pkg_resources.resource_stream('pykaryote', os.path.join('configs', 'master.cfg')) as (f):
            config_parser.readfp(f)
        attrs = _read_config(config_parser, dct=dct)
        attrs['is_initialized'] = False
        return super(SettingsMetaclass, cls).__new__(cls, name, bases, attrs)


class SettingsNamespace(object):
    """Contains simulation configuration settings.

    Handles loading of configuration files. Settings default to those from
    ``master.cfg``. Uses a metaclass to create attributes to match the master
    config file.
    """
    __metaclass__ = SettingsMetaclass

    def __init__(self):
        self._update_calculations()

    def load(self, config_filename):
        """Loads data from a simulation configuration file.

        Data from the file overwrites the current settings. Missing data is
        not overwritten.
        Settings are type checked. If the types do not match those in
        'master.cfg', ValueError is thrown.
        """
        config_parser = configparser.RawConfigParser()
        with open(config_filename, 'r') as (f):
            config_parser.readfp(f)
        settings_dict = _read_config(config_parser)
        for key, value in settings_dict.iteritems():
            if type(value) != type(getattr(self, key)):
                t1, t2 = type(value), type(getattr(self, key))
                if not (t1 in (float, int) and t2 in (float, int)):
                    raise ValueError(('Type mismatch in attribute: {}.').format(key) + (' received: {}, expected: {}').format(t1, t2))
            setattr(self, key, value)

        self._update_calculations()
        self.is_initialized = True

    def _update_calculations(self):
        """Loads settings. To be called whenever settings values are changed.
        """
        self.num_chemicals = sum(self.chem_list)
        self.min_codon = -(self.num_gather + self.num_move + self.num_protein)
        self.grange = range(-self.num_gather, 0)
        self.mrange = range(-(self.num_gather + self.num_move), -self.num_gather)
        self.prange = range(self.min_codon, -(self.num_gather + self.num_move))

    def init_globals(self, config_file):
        """Alias for load(). Exists for backwards compatibility.
        """
        self.load(config_file)


def _initialize_settings():
    """Initializes ``settings`` object to default values from master.cfg file.

    To be called when the 'globals' module is loaded. This function uses
    meta-programming to create the 'SettingsNamespace' class from options
    in the config file, and the 'settings' instance is created. Defaults can
    be overwritten by calling settings.load(), which ensures that loaded
    settings are of the correct type.
    """
    global settings
    if settings is not None:
        raise RuntimeError('Settings have already been initialized to defaults. To override defaults, use settings.load()')
    settings = SettingsNamespace()
    return


settings = None
if settings is None:
    _initialize_settings()