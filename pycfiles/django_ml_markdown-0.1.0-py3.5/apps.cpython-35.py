# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ml_markdown/apps.py
# Compiled at: 2017-02-19 08:19:13
# Size of source mod 2**32: 1378 bytes
"""
    Default configuration module
"""
from django.apps import AppConfig

class MlMarkdownConfig(AppConfig):
    __doc__ = '\n        Default configuration for ml_markdown\n    '
    name = 'ml_markdown'
    tags = [
     'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
     'p', 'div', 'pre', 'code', 'ul', 'ol', 'li',
     'table', 'thead', 'tbody', 'tr', 'th', 'td',
     'span', 'strong', 'em', 'a', 'img', 'blockquote',
     'hr', 'sup', 'sub', 'stroke']
    attributes = {'h1': ['id'], 
     'h2': ['id'], 
     'h3': ['id'], 
     'h4': ['id'], 
     'h5': ['id'], 
     'h6': ['id'], 
     'a': ['href'], 
     'img': ['src', 'alt'], 
     'div': ['class'], 
     'span': ['class'], 
     'sup': ['id'], 
     'li': ['id']}
    misaka_extensions = [
     'fenced-code',
     'footnotes',
     'math',
     'tables']