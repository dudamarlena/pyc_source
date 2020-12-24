# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/t/work/cihai/cihai/cihai/core.py
# Compiled at: 2019-08-17 05:41:51
# Size of source mod 2**32: 4513 bytes
"""Cihai core functionality."""
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
    __doc__ = '\n    Central application object.\n\n    By default, this automatically adds the UNIHAN dataset.\n\n    Attributes\n    ----------\n    config : dict\n\n    Notes\n    -----\n    Inspired by the early pypa/warehouse applicaton object [1]_.\n\n    **Configuration templates**\n\n    The ``config`` :py:class:`dict` parameter supports a basic template system\n    for replacing :term:`XDG Base Directory` directory variables, tildes\n    and environmentas variables. This is done by passing the option dict\n    through :func:`cihai.config.expand_config` during initialization.\n\n    Examples\n    --------\n    To use cihai programatically, invoke and install the UNIHAN [2]_ dataset:\n\n    .. literalinclude:: ../examples/basic_usage.py\n        :language: python\n\n    Above: :attr:`~cihai.data.unihan.bootstrap.is_bootstrapped` can check if the system\n    has the database installed.\n\n    References\n    ----------\n    .. [1] UNICODE HAN DATABASE (UNIHAN) documentation.\n       https://www.unicode.org/reports/tr38/. Accessed March 31st, 2018.\n    .. [2] PyPA Warehouse on GitHub. https://github.com/pypa/warehouse.\n       Accessed sometime in 2013.\n    '
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