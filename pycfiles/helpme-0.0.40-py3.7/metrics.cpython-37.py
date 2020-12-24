# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/utils/metrics.py
# Compiled at: 2019-12-18 15:57:23
# Size of source mod 2**32: 3954 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This particular module is derived from the wtf plugin of datalad/datalad,
which is released under an MIT license. See the license for details
https://github.com/datalad/datalad/blob/master/COPYING

"""
from helpme.logger import bot
from functools import partial
from collections import OrderedDict
import os, locale, platform, sys

class MetricsCollector(object):

    def __init__(self, decor='markdown'):
        """Generate metrics for a system, primarily python and system
           related. This is intended to submit to an issue report to help
           with debugging.
        """
        self.SECTION_CALLABLES = {'python':self.describe_python, 
         'system':self.describe_system}
        self.metrics = dict()
        self.calculate_metrics()

    def __str__(self):
        return '[helpme|metrics]'

    def __repr__(self):
        return self.__str__()

    def get_encoding_info(self):
        """Return a dictionary with various encoding/locale information
           https://github.com/datalad/datalad/blob/master/datalad/utils.py#L2108
        """
        return OrderedDict([
         (
          'default', sys.getdefaultencoding()),
         (
          'filesystem', sys.getfilesystemencoding()),
         (
          'locale.prefered', locale.getpreferredencoding())])

    def get_linux_distribution(self):
        """Compatibility wrapper for {platform,distro}.linux_distribution().
           https://github.com/datalad/datalad/blob/master/datalad/utils.py#L77
        """
        if hasattr(platform, 'linux_distribution'):
            result = platform.linux_distribution()
        else:
            import distro
            result = distro.linux_distribution(full_distribution_name=False)
        return result

    def describe_system(self):
        """collect metrics about the user system, including type, name
           release, version, encoding, and distribution
        """
        try:
            dist = self.get_linux_distribution()
        except Exception as exc:
            try:
                bot.warning('Failed to get distribution information: %s' % exc)
                dist = tuple()
            finally:
                exc = None
                del exc

        return {'type':os.name, 
         'name':platform.system(), 
         'release':platform.release(), 
         'version':platform.version(), 
         'distribution':' '.join([
          _t2s(dist), _t2s(platform.mac_ver()), _t2s(platform.win32_ver())]).rstrip(), 
         'encoding':self.get_encoding_info()}

    def calculate_metrics(self):
        """calculate the metrics in the SECTION_CALLABLES"""
        for name, func in self.SECTION_CALLABLES.items():
            self.metrics[name] = func()

    def describe_python(self):
        """Return the version and implementation of python"""
        return {'version':platform.python_version(), 
         'implementation':platform.python_implementation()}


def _t2s(t):
    res = []
    for e in t:
        if isinstance(e, tuple):
            es = _t2s(e)
            if es != '':
                res += ['(%s)' % es]
            elif e != '':
                res += [e]

    return '/'.join(res)