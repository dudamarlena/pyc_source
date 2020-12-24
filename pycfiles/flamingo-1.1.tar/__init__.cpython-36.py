# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/__init__.py
# Compiled at: 2020-02-26 10:48:47
# Size of source mod 2**32: 494 bytes
import os
from flamingo.core.data_model import Content, ContentSet, F, Q
from flamingo.core.plugins.plugin_manager import hook
_dirname = os.path.dirname(__file__)
VERSION = (0, 12, 2)
VERSION_STRING = '.'.join([str(i) for i in VERSION])
THEME_ROOT = os.path.join(_dirname, 'theme')
PROJECT_TEMPLATES_ROOT = os.path.join(_dirname, 'project_templates')
PROJECT_TEMPLATES_DATA_PATH = os.path.join(PROJECT_TEMPLATES_ROOT, 'data.ini')