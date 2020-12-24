# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/truffle/global_constants.py
# Compiled at: 2017-07-10 04:45:28
"""Description: List of constants maintained for python backend."""
SUPPORTED_LANGS = '.py'
SUPPORTED_LANGS_REGEX = '.py$'
TRUFFLE_DOCSTRING_REGEX = 'Description:((\n)|.)*Args:((\n)|.)*Returns:((\n)|.)*Raises:((\n)|.)*'
INCLUDE_LIST = [
 '.py$', '.md$', '.txt$', '.js$', '.html$', '.htm$', '.css$']
EXCLUDE_LIST = [
 '.git*', '.DS_Store', '.pyc$', '__pycache__', '.ico']
COUNT_ID = 0