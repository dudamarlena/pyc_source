# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benepar/__init__.py
# Compiled at: 2020-05-05 12:30:15
# Size of source mod 2**32: 140 bytes
"""
benepar: Berkeley Neural Parser
"""
from .downloader import download
from .nltk_plugin import Parser
__all__ = [
 'Parser', 'download']