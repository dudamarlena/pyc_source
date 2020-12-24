# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amarin/dev/sphinx-mediatel/src/sphinx_paw/builders/confluence.py
# Compiled at: 2019-11-19 10:51:04
# Size of source mod 2**32: 1474 bytes
import importlib
from sphinx.application import Sphinx
from sphinx_paw.configurable import ConfigFile
from sphinx_paw.configurable import ConfigFileSection
from sphinx_paw.constants import REBUILD_ON_CHANGE
from sphinx_paw.exceptions import RequireExtensionModule
from sphinx_paw.utils import get_private_section_name
extension_module = 'sphinxcontrib.confluencebuilder'
section_name = 'confluence'

def init_confluence(app, config):
    """Configure confluence builder options"""
    if not isinstance(app, Sphinx):
        raise AssertionError
    else:
        if not isinstance(config, ConfigFile):
            raise AssertionError
        else:
            private_section_name = get_private_section_name(config, 'confluence')
            if not config.has_section(private_section_name):
                return
            try:
                importlib.import_module(extension_module)
            except Exception:
                raise RequireExtensionModule('Required %s' % extension_module)

        app.add_config_value('confluence_publish', True, REBUILD_ON_CHANGE)
        confluence = config.get_section(private_section_name)
        assert isinstance(confluence, ConfigFileSection)
    confluence.configure('space_name', None, 'confluence_space_name')
    confluence.configure('parent_page', None, 'confluence_parent_page')
    confluence.configure('server', None, 'confluence_server_url')
    confluence.configure('username', None, 'confluence_server_user')
    confluence.configure('password', None, 'confluence_server_pass')
    app.setup_extension('sphinxcontrib.confluencebuilder')