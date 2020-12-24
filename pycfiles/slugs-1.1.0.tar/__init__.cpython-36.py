# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/peter/slugs/slugs/__init__.py
# Compiled at: 2018-03-12 11:15:11
# Size of source mod 2**32: 1035 bytes
import os, re
version_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'version.py')
with open(version_path, 'r') as (version_file):
    mo = re.search("^.*= '(\\d\\.\\d\\..*)'$", version_file.read(), re.MULTILINE)
    __version__ = mo.group(1)
__all__ = [
 'app',
 'controllers',
 'plugins']