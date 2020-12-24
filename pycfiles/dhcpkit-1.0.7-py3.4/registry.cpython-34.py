# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/registry.py
# Compiled at: 2017-06-25 12:38:10
# Size of source mod 2**32: 2335 bytes
"""
Base class for pkg_resources based registries
"""
import collections, logging, pkg_resources
from dhcpkit.utils import camelcase_to_dash
logger = logging.getLogger(__name__)

class Registry(collections.UserDict):
    __doc__ = '\n    Base class for registries\n    '
    entry_point = 'dhcpkit.NONE'

    def __init__(self):
        """
        A custom dictionary that initialises itself with the entry points from pkg_resources
        """
        super().__init__()
        self.by_name = {}
        entry_points = pkg_resources.iter_entry_points(group=self.entry_point)
        for entry_point in entry_points:
            try:
                name = int(entry_point.name)
            except ValueError:
                name = entry_point.name

            if name in self.data:
                logger.warning('Multiple entry points found for {} {}, using {}'.format(self.__class__.__name__, name, self.data[name]))
                continue
            try:
                loaded = entry_point.load()
                self.data[name] = loaded
                alternative_name = self.get_name(loaded)
                self.by_name[alternative_name] = loaded
            except pkg_resources.VersionConflict as e:
                logger.critical('Entry point {} for {} is not compatible: {}'.format(entry_point, self.__class__.__name__, e))
                continue
            except ImportError:
                logger.exception('Entry point {} for {} could not be loaded'.format(entry_point, self.__class__.__name__))
                continue

    def get_name(self, item: object) -> str:
        """
        Get the name for the by_name mapping.

        :param item: The item to determine the name of
        :return: The name to use as key in the mapping
        """
        return camelcase_to_dash(item.__name__)