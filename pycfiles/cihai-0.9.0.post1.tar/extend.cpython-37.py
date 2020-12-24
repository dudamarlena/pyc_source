# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/t/work/cihai/cihai/cihai/extend.py
# Compiled at: 2019-08-17 05:41:51
# Size of source mod 2**32: 3329 bytes
"""
Cihai Plugin System

Status: Experimental, API can change

As a pilot, the UNIHAN library, and an plugin for it, in #131 [1]_

You can bring any data layout / backend you like to cihai.

For convenience, you can use cihai's configuration namespace and SQLAlchemy settings.

You can also create plugins which extend another. So if Unihan doesn't have a lookup
for variant glyphs, this can be added.
"""
from __future__ import absolute_import, print_function, unicode_literals
from . import utils
from ._compat import string_types

class ConfigMixin(object):
    __doc__ = "\n    This piggybacks cihai's global config state, as well as your datasets.\n\n    Cihai will automatically manage the user's config, as well as your datasets,\n    neatly in XDG.\n\n    Raises\n    ------\n    Functions inside, and what you write relating to dataset config should return\n\n    CihaiDatasetConfigException (CihaiDatasetException)\n\n    config.cihai = links directly back to Cihai's configuration dictionary\n    (todo note: make this non-mutable property)\n\n    config : dict\n        your local user's config\n\n    check() : function, optional\n        this is ran on start. it can raise DatasetConfigException\n\n    default_config : your dataset's default configuration\n\n    get_default_config : override function in case you'd like custom configs (for\n        instnace if you want a platform to use a different db driver, or do version\n        checks, etc.)\n\n        internal functions use get_default_config()\n    "


class SQLAlchemyMixin(object):
    __doc__ = "Your dataset can use any backend you'd like, we provide a backend for you, that\n    automatically piggybacks on cihai's zero-config, XDG / SQLAchemy configuration. So\n    it's preconfigured for the user.\n\n    In addition, this mixin gives you access to any other of the user's sqlalchemy\n    sql that use this mixin. So if you want a dataset that utilitizes UNIHAN, you can\n    access that easily.\n\n    This will provide the following instance-level properties in methods:\n\n    When you have access, it's expected to keep your tables / databases namespaced so\n    they don't clobber.\n    "
    engine = None
    metadata = None
    session = None
    base = None


class Dataset(object):
    __doc__ = '\n    Cihai dataset, e.g. UNIHAN.\n\n    See Also\n    --------\n    cihai.data.unihan.dataset.Unihan : reference implementation\n    '

    def bootstrap(self):
        pass

    def add_plugin(self, _cls, namespace, bootstrap=True):
        if isinstance(_cls, string_types):
            _cls = utils.import_string(_cls)
        else:
            setattr(self, namespace, _cls())
            plugin = getattr(self, namespace)
            if hasattr(self, 'sql'):
                if isinstance(self, SQLAlchemyMixin):
                    plugin.sql = self.sql
            if bootstrap:
                if hasattr(plugin, 'bootstrap') and callable(plugin.bootstrap):
                    plugin.bootstrap()


class DatasetPlugin(object):
    __doc__ = '\n    Extend the functionality of datasets with custom methods, actions, etc.\n\n    See Also\n    --------\n    cihai.data.unihan.dataset.UnihanVariants : reference implementation\n    '