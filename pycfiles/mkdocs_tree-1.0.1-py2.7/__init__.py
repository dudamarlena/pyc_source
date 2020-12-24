# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mkdocs_tree\__init__.py
# Compiled at: 2014-11-24 13:59:29
from mkdocs import events
from . import build
from . import config as tree_config

def init_extension(config):
    """
    Intitializes the `tree` extension for mkdocs.

    ### Parameters
        config | <dict>
    """
    tree_config.docs_dir = config.get('docs_dir', 'docs')
    events.register_callback(events.BuildPage, build.create_tree)