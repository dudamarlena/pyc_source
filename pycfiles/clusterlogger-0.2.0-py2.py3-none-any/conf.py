# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ajoly/git/clusterlib/doc/conf.py
# Compiled at: 2014-11-07 11:12:57
import sys, os
sys.path.append(os.path.abspath('sphinxext'))
import sphinx_bootstrap_theme
extensions = [
 'sphinx.ext.mathjax',
 'sphinx.ext.autodoc',
 'sphinx.ext.autosummary',
 'sphinx.ext.doctest',
 'sphinx.ext.mathjax',
 'numpy_ext.numpydoc']
autosummary_generate = True
autodoc_default_flags = ['members', 'inherited-members']
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'clusterlib'
copyright = '2014, Arnaud Joly'
version = 'dev'
release = 'dev'
exclude_patterns = [
 '_build']
pygments_style = 'sphinx'
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_static_path = [
 '_static']
html_show_sphinx = False
htmlhelp_basename = 'clusterlibdoc'
html_theme_options = {'navbar_title': 'Clusterlib', 
   'navbar_links': [
                  ('User guide', 'user_guide'),
                  ('References', 'references'),
                  ("What's new?", 'whats_new')], 
   'navbar_sidebarrel': False, 
   'navbar_pagenav': False, 
   'globaltoc_depth': 0, 
   'globaltoc_includehidden': 'false', 
   'navbar_class': 'navbar', 
   'navbar_fixed_top': 'true', 
   'source_link_position': 'None', 
   'bootswatch_theme': 'lumen', 
   'bootstrap_version': '3'}
latex_elements = {}
latex_documents = [
 ('index', 'clusterlib.tex', 'clusterlib Documentation', 'Arnaud Joly', 'manual')]
man_pages = [
 (
  'index', 'clusterlib', 'clusterlib Documentation',
  [
   'Arnaud Joly'], 1)]
texinfo_documents = [
 ('index', 'clusterlib', 'clusterlib Documentation', 'Arnaud Joly', 'clusterlib', 'One line description of project.',
 'Miscellaneous')]