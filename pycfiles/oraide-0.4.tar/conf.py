# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ddbeck/src/oraide/docs/conf.py
# Compiled at: 2013-08-20 19:54:14
import sys, os
extensions = [
 'sphinx.ext.autodoc', 'sphinx.ext.doctest',
 'sphinx.ext.intersphinx', 'sphinx.ext.extlinks']
if sys.version_info[0] == 2:
    if os.environ.get('READTHEDOCS', None) is None:
        extensions.append('sphinxcontrib.spelling')
else:
    sys.stdout.write('note: spellcheck is Python 2 only\n')
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'Oraide'
copyright = '2013, Daniel D. Beck'
try:
    import oraide
    version = oraide.__version__
except ImportError:
    print 'Oraide must be installed to build the documentation.'
    sys.exit(1)

del oraide
release = version
exclude_patterns = [
 '_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = [
 '_static']
htmlhelp_basename = 'Oraidedoc'
latex_elements = {}
latex_documents = [
 ('index', 'Oraide.tex', 'Oraide Documentation', 'Daniel D. Beck', 'manual')]
man_pages = [
 (
  'index', 'oraide', 'Oraide Documentation',
  [
   'Daniel D. Beck'], 1)]
texinfo_documents = [
 ('index', 'Oraide', 'Oraide Documentation', 'Daniel D. Beck', 'Oraide', 'One line description of project.',
 'Miscellaneous')]
intersphinx_mapping = {'python': ('http://docs.python.org/3.2', None)}
spelling_show_suggestions = False
extlinks = {'issue': ('https://github.com/ddbeck/oraide/issues/%s', 'Issue #')}