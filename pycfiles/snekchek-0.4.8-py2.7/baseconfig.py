# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/baseconfig.py
# Compiled at: 2020-03-03 07:34:32
"""Base config for entry points."""
from __future__ import unicode_literals
import os, configobj
__all__ = ('config', )
config = configobj.ConfigObj({b'all': {b'linters': [
                       b'flake8',
                       b'pylint',
                       b'yapf',
                       b'isort',
                       b'pyroma',
                       b'safety',
                       b'dodgy',
                       b'vulture',
                       b'pytest',
                       b'pypi']}, 
   b'pypi': {b'TWINE_USERNAME': os.environ.get(b'TWINE_USERNAME', b'abc'), 
             b'TWINE_PASSWORD': os.environ.get(b'TWINE_PASSWORD', b'abc'), 
             b'sign': False, 
             b'TWINE_REPOSITORY': b'pypi', 
             b'quiet': False}, 
   b'flake8': {b'max-line-length': 79, 
               b'exclude': [
                          b'build', b'dist'], 
               b'ignore': [], b'quiet': False}, 
   b'pylint': {b'quiet': False}, b'yapf': {b'inplace': True, b'quiet': False}, b'isort': {b'line_length': 79, 
              b'multi_line_output': True, 
              b'inplace': True, 
              b'indent': b'    ', 
              b'sections': (b'FUTURE,STDLIB,THIRDPARTY,FIRSTPARTY,LOCALFOLDER').split(b','), 
              b'quiet': False}, 
   b'bandit': {b'quiet': False}, b'style': {b'inplace': True, b'quiet': False}, b'pyroma': {b'quiet': False}, b'vulture': {b'min-confidence': 60, 
                b'verbose': False, 
                b'exclude': [], b'sort-by-size': False, 
                b'quiet': False}, 
   b'safety': {b'quiet': False, 
               b'ignore': [], b'pyup_key': b'', 
               b'db_path': b''}, 
   b'dodgy': {b'quiet': False, b'ignore_paths': []}, b'pytest': {b'quiet': False, b'testpaths': b'tests'}, b'unittest': {b'quiet': False, b'testpaths': b'tests'}, b'black': {b'quiet': False, 
              b'line_length': 79, 
              b'exclude': b'', 
              b'versions': [ b'PY' + version for version in ('27', '33', '34', '35', '36', '37', '38')
                         ]}})