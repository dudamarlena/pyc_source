# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/docfly-project/docfly/__init__.py
# Compiled at: 2020-04-15 23:18:53
"""
docfly package.
"""
from __future__ import print_function
__version__ = '0.0.18'
__short_description__ = 'A utility tool to help you build better sphinx documents.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@me.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@me.com'
__github_username__ = 'MacHu-GWU'
try:
    from .api_reference_doc import ApiReferenceDoc
    from .doctree import DocTree
except Exception as e:
    print(e)