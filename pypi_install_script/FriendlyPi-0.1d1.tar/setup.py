#     Copyright 2013-2014 Emiliano Mennucci
#
#     This file is part of FriendlyPi.
# 
#     FriendlyPi is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     FriendlyPi is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with FriendlyPi.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

entry_points_file = open('default_plugins.ini', 'rt')

setup(name='FriendlyPi',
version='0.1d1',
description = 'FriendlyPi server',
long_description = open('README.rst').read(),
author = 'Emiliano Mennucci',
author_email = 'ekumene@gmail.com',
url = 'https://github.com/happyemi/friendlypi',
install_requires = ['tornado==3.2'],
packages = ['plugins'],
package_dir = {'': 'src'},
scripts = ['src/friendlypi.py'],
license = "GPLv3",
data_files = [('html', ['html/index.html']),('docs', ['README.rst', 'LICENSE'])],
entry_points = entry_points_file.read(),
zip_safe = True,
classifiers = ['Development Status :: 2 - Pre-Alpha',
'Intended Audience :: System Administrators',
'Operating System :: POSIX :: Linux',
'Programming Language :: Python :: 3',
'Topic :: Internet :: WWW/HTTP',
'Topic :: System :: Systems Administration']
)
