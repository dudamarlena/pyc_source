# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amarin/dev/sphinx-mediatel/src/sphinx_paw/main_params.py
# Compiled at: 2019-11-19 19:00:53
# Size of source mod 2**32: 2639 bytes
"""Init Sphinx params"""
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx_paw.constants import PACKAGE_NAME
from sphinx_paw import ConfigFile
from sphinx_paw import init_confluence
from sphinx_paw import init_latex
from sphinx_paw import Plugin
from sphinx_paw.builders.htmldir import init_html
from sphinx_paw.configurable import set_config_value
from sphinx_paw.utils import get_main_sphinx_section_name
from os import getenv
logger = logging.getLogger(__name__)
builders_order = {'confluence':init_confluence, 
 'latex':init_latex, 
 'html':init_html}

def init_main_params(app, config):
    """Configure confluence builder options"""
    if not isinstance(app, Sphinx):
        raise AssertionError
    elif not isinstance(config, ConfigFile):
        raise AssertionError
    logger.info('Init plugins')
    Plugin.run_all_found(app, config)
    logger.info('Prepare configurations')
    sphinx_config = config.get_section(get_main_sphinx_section_name())
    builders = sphinx_config.builder
    source_suffix = [
     '.rst']
    set_config_value(app, 'source_suffix', source_suffix)
    master_doc = 'index'
    set_config_value(app, 'master_doc', master_doc)
    exclude_patterns = []
    set_config_value(app, 'exclude_patterns', exclude_patterns)
    set_config_value(app, 'numfig', True)
    numfig_secnum_depth = 0
    set_config_value(app, 'numfig_secnum_depth', numfig_secnum_depth)
    from sphinx.locale import get_translation
    _ = get_translation(PACKAGE_NAME)
    logger.info(f"Attach translation {_.__name__}[{app.config.language}]")
    numfig_format = {'figure':_('Fig. %s'), 
     'table':_('Table %s'), 
     'code-block':_('Listing %s'), 
     'section':_('Section')}
    logger.info(f"Numfig format f{numfig_format}")
    set_config_value(app, 'numfig_format', numfig_format)
    pygments_style = 'friendly'
    set_config_value(app, 'pygments_style', pygments_style)
    today_fmt = '%x'
    set_config_value(app, 'today_fmt', today_fmt)
    templates_path = [
     '_templates']
    set_config_value(app, 'templates_path', templates_path)
    logger.info('Configure builders')
    for builder_name, builder_init in builders_order.items():
        if builder_name not in builders:
            pass
        else:
            builder_init(app, config)

    app.setup_extension('sphinx_vcs_changelog')