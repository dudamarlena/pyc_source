# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/benepar/__init__.py
# Compiled at: 2020-05-05 12:30:15
# Size of source mod 2**32: 140 bytes
__doc__ = '\nbenepar: Berkeley Neural Parser\n'
from .downloader import download
from .nltk_plugin import Parser
__all__ = [
 'Parser', 'download']