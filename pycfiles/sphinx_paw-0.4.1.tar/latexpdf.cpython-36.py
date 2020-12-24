# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amarin/dev/sphinx-mediatel/src/sphinx_paw/builders/latexpdf.py
# Compiled at: 2019-11-19 18:55:14
# Size of source mod 2**32: 3009 bytes
import jinja2
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx_paw.constants import PACKAGE_NAME
from sphinx_paw.builders.constants.latexpdf import FILENAME_FOOTER
from sphinx_paw.builders.constants.latexpdf import FILENAME_PREAMBLE
from sphinx_paw.configurable import ConfigFile
from sphinx_paw.configurable import set_config_value
from sphinx_paw.rewritable import rewritable_file_content
logger = logging.getLogger(__name__)

def jinja_for_latex():
    """Make jinja2 env for templating latex"""
    return jinja2.Environment(block_start_string='\\BLOCK{',
      block_end_string='}',
      variable_start_string='\\VAR{',
      variable_end_string='}',
      comment_start_string='\\#{',
      comment_end_string='}',
      line_statement_prefix='%%',
      line_comment_prefix='%#',
      trim_blocks=True)


def init_latex(app, config):
    """Configure confluence builder options"""
    if not isinstance(app, Sphinx):
        raise AssertionError
    elif not isinstance(config, ConfigFile):
        raise AssertionError
    config.assert_has_section('metadata')
    set_config_value(app, 'latex_engine', 'xelatex')
    set_config_value(app, 'latex_paper_size', 'a4')
    set_config_value(app, 'latex_show_urls', 'footnotes')
    set_config_value(app, 'latex_use_xindy', True)
    set_config_value(app, 'latex_domain_indices', True)
    preamble = rewritable_file_content(app, FILENAME_PREAMBLE)
    at_end_of_body = rewritable_file_content(app, FILENAME_FOOTER)
    from sphinx.locale import get_translation
    _ = get_translation(PACKAGE_NAME)
    template = jinja_for_latex().from_string(at_end_of_body)
    context = dict(list_of_images_title=(_('List of images')),
      list_of_tables_title=(_('List of tables')),
      list_of_listings_title=(_('List of listings')))
    logger.info(f"Render atendofbody.tex with context {context}")
    at_end_of_body = (template.render)(**context)
    set_config_value(app, 'latex_elements', {'preamble':preamble, 
     'atendofbody':at_end_of_body, 
     'pointsize':'10pt', 
     'fncychap':'', 
     'extraclassoptions':'openany,oneside', 
     'sphinxsetup':'hmargin={1in,1in}, vmargin={1in,1in}, marginpar=0.1in'})
    latex_document = (
     app.config['master_doc'],
     app.config['package'] + '.tex',
     app.config['project'],
     app.config['author'],
     'manual',
     False)
    set_config_value(app, 'latex_documents', [
     latex_document])