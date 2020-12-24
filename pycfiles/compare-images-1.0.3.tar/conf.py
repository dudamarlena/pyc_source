# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Rudy\Projects\rudylattae\compare\doc\conf.py
# Compiled at: 2011-02-04 17:26:14
import sys, os
extensions = [
 'sphinx.ext.autodoc', 'sphinx.ext.doctest']
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'compare'
copyright = '2011, Rudy Lattae'
version = '0.2'
release = '0.2b'
exclude_patterns = [
 '_build']
pygments_style = 'default'
html_theme = 'nature'
html_title = '%s %s' % (project, release)
html_static_path = [
 '_static']
htmlhelp_basename = 'comparedoc'
latex_documents = [
 ('index', 'compare.tex', 'compare Documentation', 'Rudy Lattae', 'manual')]
man_pages = [
 (
  'index', 'compare', 'compare Documentation',
  [
   'Rudy Lattae'], 1)]