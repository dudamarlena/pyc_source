# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/stefan/Workspace/Collectors/docs/conf.py
# Compiled at: 2010-03-26 11:18:39
import sys, os
sys.path.append(os.path.abspath('..'))
extensions = [
 'sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
templates_path = [
 '_templates']
source_suffix = '.txt'
master_doc = 'index'
project = 'Collectors'
copyright = '2010, Stefan Scherfke and Ontje Lünsdorf'
version = '0.2'
release = '0.2'
exclude_trees = [
 '_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = [
 '_static']
htmlhelp_basename = 'Collectorsdoc'
latex_documents = [
 ('index', 'Collectors.tex', 'Collectors Documentation', 'Stefan Scherfke and Ontje Lünsdorf',
 'manual')]
intersphinx_mapping = {'http://docs.python.org/': None, 
   'http://simpy.sourceforge.net/SimPyDocs/': None}