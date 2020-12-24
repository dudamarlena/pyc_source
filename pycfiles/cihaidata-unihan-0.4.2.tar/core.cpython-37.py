# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/t/work/cihai/cihai/cihai/core.py
# Compiled at: 2019-08-17 05:41:51
# Size of source mod 2**32: 4513 bytes
__doc__ = 'Cihai core functionality.'
from __future__ import absolute_import, print_function, unicode_literals
import logging, os, kaptan
from appdirs import AppDirs
from . import exc, extend
from ._compat import string_types
from .config import expand_config
from .constants import DEFAULT_CONFIG, UNIHAN_CONFIG
from .db import Database
from .utils import import_string, merge_dict
log = logging.getLogger(__name__)

class Cihai(object):
    """Cihai"""
    default_config = DEFAULT_CONFIG

    def __init__(self, config=None, unihan=True):
        """
        Parameters
        ----------
        config : dict, optional
        unihan : boolean, optional
            Bootstrap the core UNIHAN dataset (recommended)
        """
        if config is None:
            config = {}
        else:
            self.config = merge_dict(self.default_config, config)
            if unihan:
                self.config = merge_dict(UNIHAN_CONFIG, self.config)
            dirs = AppDirs('cihai', 'cihai team')
            expand_config(self.config, dirs)
            os.path.exists(dirs.user_data_dir) or os.makedirs(dirs.user_data_dir)
        self.sql = Database(self.config)
        self.bootstrap()

    def bootstrap(self):
        for namespace, class_string in self.config.get('datasets', {}).items():
            self.add_dataset(class_string, namespace)

        for dataset, plugins in self.config.get('plugins', {}).items():
            for namespace, class_string in plugins.items():
                getattr(self, dataset).add_plugin(class_string, namespace)

    def add_dataset(self, _cls, namespace):
        if isinstance(_cls, string_types):
            _cls = import_string(_cls)
        setattr(self, namespace, _cls())
        dataset = getattr(self, namespace)
        if isinstance(dataset, extend.SQLAlchemyMixin):
            dataset.sql = self.sql

    @classmethod
    def from_file(cls, config_path=None, *args, **kwargs):
        """
        Create a Cihai instance from a JSON or YAML config.

        Parameters
        ----------
        config_path : str, optional
            path to custom config file

        Returns
        -------
        :class:`Cihai` :
            application object
        """
        config_reader = kaptan.Kaptan()
        config = {}
        if config_path:
            if not os.path.exists(config_path):
                raise exc.CihaiException('{0} does not exist.'.format(os.path.abspath(config_path)))
            if not any((config_path.endswith(ext) for ext in ('json', 'yml', 'yaml',
                                                              'ini'))):
                raise exc.CihaiException('{0} does not have a yaml,yml,json,ini extend.'.format(os.path.abspath(config_path)))
            else:
                custom_config = config_reader.import_config(config_path).get()
                config = merge_dict(config, custom_config)
        return cls(config)