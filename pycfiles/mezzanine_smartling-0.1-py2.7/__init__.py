# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/craig.williams/.virtualenvs/test-trans/lib/python2.7/site-packages/mezzanine_smartling/__init__.py
# Compiled at: 2015-09-16 23:20:55
"""
Developed by Craig J Williams
"""
from .managers import default_relational_manager
manager = default_relational_manager
register = default_relational_manager.register
get_registered_models = default_relational_manager.get_registered_models