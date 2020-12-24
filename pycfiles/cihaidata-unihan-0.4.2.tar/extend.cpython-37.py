# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/t/work/cihai/cihai/cihai/extend.py
# Compiled at: 2019-08-17 05:41:51
# Size of source mod 2**32: 3329 bytes
__doc__ = "\nCihai Plugin System\n\nStatus: Experimental, API can change\n\nAs a pilot, the UNIHAN library, and an plugin for it, in #131 [1]_\n\nYou can bring any data layout / backend you like to cihai.\n\nFor convenience, you can use cihai's configuration namespace and SQLAlchemy settings.\n\nYou can also create plugins which extend another. So if Unihan doesn't have a lookup\nfor variant glyphs, this can be added.\n"
from __future__ import absolute_import, print_function, unicode_literals
from . import utils
from ._compat import string_types

class ConfigMixin(object):
    """ConfigMixin"""
    pass


class SQLAlchemyMixin(object):
    """SQLAlchemyMixin"""
    engine = None
    metadata = None
    session = None
    base = None


class Dataset(object):
    """Dataset"""

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
    """DatasetPlugin"""
    pass