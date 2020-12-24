# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\gearbox\doc\source\conf.py
# Compiled at: 2015-04-24 15:26:25
extensions = [
 'sphinx.ext.autodoc',
 'sphinx.ext.doctest',
 'sphinx.ext.intersphinx',
 'sphinx.ext.todo',
 'sphinx.ext.coverage',
 'sphinx.ext.mathjax',
 'sphinx.ext.ifconfig',
 'sphinx.ext.viewcode']
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'python-gearbox'
copyright = '2015, Eduardo M. Fírvida Donéstevez'
author = 'Eduardo M. Fírvida Donéstevez'
version = '0.1'
release = '0.1'
language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True
html_theme = 'alabaster'
html_static_path = [
 '_static']
htmlhelp_basename = 'python-gearboxdoc'
latex_elements = {}
latex_documents = [
 (
  master_doc, 'python-gearbox.tex', 'python-gearbox Documentation',
  'Eduardo M. Fírvida Donéstevez', 'manual')]
man_pages = [
 (
  master_doc, 'python-gearbox', 'python-gearbox Documentation',
  [
   author], 1)]
texinfo_documents = [
 (
  master_doc, 'python-gearbox', 'python-gearbox Documentation',
  author, 'python-gearbox', 'One line description of project.',
  'Miscellaneous')]
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = [
 'search.html']
intersphinx_mapping = {'https://docs.python.org/': None}