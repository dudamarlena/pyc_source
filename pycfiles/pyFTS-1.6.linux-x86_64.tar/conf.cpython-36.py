# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/conf.py
# Compiled at: 2018-04-12 16:13:04
# Size of source mod 2**32: 5381 bytes
project = 'pyFTS'
copyright = '2018, Petrônio Cândido de Lima e Silva'
author = 'Petrônio Cândido de Lima e Silva'
version = ''
release = '1.2.2'
extensions = [
 'sphinx.ext.autodoc',
 'sphinx.ext.intersphinx',
 'sphinx.ext.todo',
 'sphinx.ext.mathjax',
 'sphinx.ext.viewcode',
 'sphinx.ext.githubpages']
templates_path = [
 '.templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = [
 '.static']
htmlhelp_basename = 'pyFTSdoc'
latex_elements = {}
latex_documents = [
 (
  master_doc, 'pyFTS.tex', 'pyFTS Documentation',
  'Petrônio Cândido de Lima e Silva', 'manual')]
man_pages = [
 (
  master_doc, 'pyfts', 'pyFTS Documentation',
  [
   author], 1)]
texinfo_documents = [
 (
  master_doc, 'pyFTS', 'pyFTS Documentation',
  author, 'pyFTS', 'One line description of project.',
  'Miscellaneous')]
intersphinx_mapping = {'https://docs.python.org/': None}
todo_include_todos = True