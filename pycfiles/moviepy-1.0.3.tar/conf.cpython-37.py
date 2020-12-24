# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomburrows/Python/moviepy-dev/moviepy/docs/conf.py
# Compiled at: 2020-02-22 10:43:15
# Size of source mod 2**32: 9936 bytes
import os, sys, sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('.'))
extensions = [
 'sphinx.ext.autodoc', 'sphinx.ext.todo',
 'sphinx.ext.viewcode', 'sphinx.ext.autosummary', 'numpydoc']
numpydoc_class_members_toctree = False
numpydoc_show_class_members = False
autosummary_generate = True
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'MoviePy'
copyright = '2017, Zulko'
exclude_patterns = [
 '_build']
pygments_style = 'sphinx'
sys.path.append(os.path.abspath('_themes'))
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_logo = '_static/logo_small.jpeg'
html_static_path = [
 '_static']
htmlhelp_basename = 'MoviePydoc'
latex_elements = {}
latex_documents = [
 ('index', 'MoviePy.tex', 'MoviePy Documentation', 'Zulko', 'manual')]
man_pages = [
 (
  'index', 'moviepy', 'MoviePy Documentation',
  [
   'Zulko'], 1)]
texinfo_documents = [
 ('index', 'MoviePy', 'MoviePy Documentation', 'Zulko', 'MoviePy', 'One line description of project.',
 'Miscellaneous')]
epub_title = 'MoviePy'
epub_author = 'Zulko'
epub_publisher = 'Zulko'
epub_copyright = '2017, Zulko'