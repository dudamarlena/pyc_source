# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/justin/src/plow/lib/python/doc/conf.py
# Compiled at: 2013-05-22 06:10:35
import sys, os
extensions = [
 'sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.coverage', 'sphinx.ext.viewcode']
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'Plow'
copyright = '2013, Matthew Chambers, Justin Israel'
version = '0.4'
release = '0.4.4'
exclude_patterns = [
 '_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = [
 '_static']
htmlhelp_basename = 'Plowdoc'
latex_elements = {}
latex_documents = [
 ('index', 'Plow.tex', 'Plow Client Documentation', 'Matthew Chambers, Justin Israel, Johan Aberg, Wan Bachtiar',
 'manual')]
man_pages = [
 (
  'index', 'plow', 'Plow Client Documentation',
  [
   'Matthew Chambers, Justin Israel, Johan Aberg, Wan Bachtiar'], 1)]
texinfo_documents = [
 ('index', 'Plow', 'Plow Client Documentation', 'Matthew Chambers, Justin Israel, Johan Aberg, Wan Bachtiar',
 'Plow', 'One line description of project.', 'Miscellaneous')]
intersphinx_mapping = {'http://docs.python.org/': None}