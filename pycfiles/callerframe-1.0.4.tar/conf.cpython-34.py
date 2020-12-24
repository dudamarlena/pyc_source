# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simone/Projects/Sources/callerframe/docs/source/conf.py
# Compiled at: 2015-10-05 08:51:43
# Size of source mod 2**32: 11602 bytes
import sys, os, shlex
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import callerframe
release = callerframe.__version__
VERSION_INFO = [int(i) for i in release.split('.')]
version = '.'.join(str(i) for i in VERSION_INFO[:2])
extensions = [
 'sphinx.ext.autodoc',
 'sphinx.ext.napoleon',
 'sphinx.ext.autosummary',
 'sphinx.ext.doctest',
 'sphinx.ext.coverage',
 'sphinx.ext.viewcode',
 'sphinx.ext.intersphinx']
napoleon_use_param = True
intersphinx_mapping = {'python': ('https://docs.python.org/3.5', None)}
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'callerframe'
copyright = '2015, Simone Campagna'
author = 'Simone Campagna'
pygments_style = 'sphinx'
todo_include_todos = False
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    except ImportError:
        pass

htmlhelp_basename = 'callerframedoc'
latex_elements = {}
latex_documents = [
 (
  master_doc, 'callerframe.tex', 'callerframe Documentation',
  'Simone Campagna', 'manual')]
man_pages = [
 (
  master_doc, 'callerframe', 'callerframe Documentation',
  [
   author], 1)]
texinfo_documents = [
 (
  master_doc, 'callerframe', 'callerframe Documentation',
  author, 'callerframe', 'Python decorator adding caller frame info to function globals.',
  'Miscellaneous')]
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = [
 'search.html']