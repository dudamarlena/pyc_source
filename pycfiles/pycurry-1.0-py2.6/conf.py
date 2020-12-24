# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycurry\doc\conf.py
# Compiled at: 2009-10-25 07:44:47
import sys, os
extensions = [
 'sphinx.ext.autodoc', 'sphinx.ext.todo']
todo_include_todos = True
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'pycurry'
copyright = '2009, Fons Dijkstra'
version = '1.0'
release = '1.0'
exclude_trees = [
 '_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = [
 '_static']
htmlhelp_basename = 'pycurrydoc'
latex_documents = [
 ('index', 'pycurry.tex', 'pycurry Documentation', 'Fons Dijkstra', 'manual')]