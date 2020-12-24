# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/utils/format.py
# Compiled at: 2019-12-18 15:57:23
# Size of source mod 2**32: 1896 bytes
"""

Copyright (C) 2018-2020 Vanessa Sochat.

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

"""
from helpme.logger import bot
import hashlib, os, sys, re

def envars_to_markdown(envars, title='Environment'):
    """generate a markdown list of a list of environment variable tuples

       Parameters
       ==========
       title: A title for the section (defaults to "Environment"
       envars: a list of tuples for the environment, e.g.:

            [('TERM', 'xterm-256color'),
             ('SHELL', '/bin/bash'),
             ('USER', 'vanessa'),
             ('LD_LIBRARY_PATH', ':/usr/local/pulse')]

    """
    markdown = ''
    if envars not in [None, '', []]:
        markdown += '\n## %s\n' % title
        for envar in envars:
            markdown += ' - **%s**: %s\n' % (envar[0], envar[1])

    return markdown


def format_code_block(code, language='python'):
    """format a chunk of code (usually a dictionary) into a code block.
    """
    return '```%s\n%s\n```' % (
     language,
     code)


def generate_identifier_hash(identifier):
    """generate a unique identifier (hash) for the issue"""
    hash_object = hashlib.md5(identifier.encode('utf-8'))
    return 'md5.%s' % hash_object.hexdigest()