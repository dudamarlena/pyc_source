# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/steven/Documents/Projects/radio/EOR/OthersCodes/21cmFAST/21cmFAST/src/py21cmfast/_cfg.py
# Compiled at: 2020-02-13 15:47:20
# Size of source mod 2**32: 2822 bytes
__doc__ = 'Open and read the configuration file.'
import contextlib, copy, warnings
from os import path
from . import yaml

class ConfigurationError(Exception):
    """ConfigurationError"""
    pass


class Config(dict):
    """Config"""
    _defaults = {'direc':'~/21cmFAST-cache', 
     'regenerate':False,  'write':True}
    _aliases = {'direc': ('boxdir', )}

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        do_write = False
        for k, v in self._defaults.items():
            if k not in self:
                if k not in self._aliases:
                    warnings.warn('Your configuration file is out of date. Updating...')
                    do_write = True
                    self[k] = v
                else:
                    for alias in self._aliases[k]:
                        if alias in self:
                            do_write = True
                            warnings.warn("Your configuration file has old key '{}' which has been re-named '{}'. Updating...".format(alias, k))
                            self[k] = self[alias]
                            del self[alias]

                    assert do_write, "The configuration file has key '{}' which is not known to 21cmFAST.".format(alias)

        if do_write:
            self.write()

    @contextlib.contextmanager
    def use(self, **kwargs):
        """Context manager for using certain configuration options for a set time."""
        backup = self.copy()
        for k, v in kwargs.items():
            self[k] = v

        yield self
        for k in kwargs:
            self[k] = backup[k]

    def write(self, fname=None):
        """Write current configuration to file to make it permanent."""
        fname = fname or 
        with open(fname, 'w') as (fl):
            yaml.dump(self._as_dict(), fl)

    def _as_dict(self):
        """The plain dict defining the instance."""
        return {k:v for k, v in self.items()}

    @classmethod
    def load(cls, file_name):
        """Create a Config object from a config file."""
        cls.file_name = file_name
        with open(file_name, 'r') as (fl):
            config = yaml.load(fl)
        return cls(config)


config = Config.load(path.expanduser(path.join('~', '.21cmfast', 'config.yml')))
default_config = copy.deepcopy(config)