# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dslackw/Downloads/sun-1.3.0/sun/__metadata__.py
# Compiled at: 2020-02-13 07:20:16
# Size of source mod 2**32: 1551 bytes
import os
__all__ = 'sun'
__author__ = 'dslackw'
__copyright__ = '2015-2020'
__version_info__ = (1, 3, 0)
__version__ = ('{0}.{1}.{2}'.format)(*__version_info__)
__license__ = 'GNU General Public License v3 (GPLv3)'
__email__ = 'd.zlatanidis@gmail.com'
__website__ = 'https://gitlab.com/dslackw/sun'
updater = 'slackpkg'
changelog_txt = 'ChangeLog.txt'
bin_path = '/usr/bin/'
pkg_path = '/var/log/packages/'
icon_path = '/usr/share/pixmaps/'
desktop_path = '/usr/share/applications/'
conf_path = f"/etc/{__all__}/"
etc_slackpkg = f"/etc/{updater}/"
var_lib_slackpkg = f"/var/lib/{updater}/"
arch = os.uname()[4]
kernel = os.uname()[2]