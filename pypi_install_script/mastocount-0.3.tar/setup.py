# Copyright 2017-2018 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#!/usr/bin/env python3

# Setup for Mastocount
'''Setup for Mastocount'''

from setuptools import setup, find_packages

CLASSIFIERS = [
    'Intended Audience :: End Users/Desktop',
    'Environment :: Console',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
]

setup(
    name='mastocount',
    version='0.3',
    license='GNU GPL v3',
    description='Mastocount retrieves the number of followers of these accounts and print detailed numbers and the total number',
    long_description='Mastocount takes several Mastodon accounts credentials, retrieve the number of followers of these accounts and print detailed numbers and the total number',
    author = 'Carl Chenet',
    author_email = 'chaica@ohmytux.com',
    url = 'https://gitlab.com/chaica/mastocount',
    classifiers=CLASSIFIERS,
    download_url='https://gitlab.com/chaica/mastocount',
    packages=find_packages(),
    scripts=['scripts/mastocount', 'scripts/register_mastocount_app'],
    install_requires=['Mastodon.py', 'elasticsearch'],
)
