# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/winterstone/docs/conf.py
# Compiled at: 2011-04-27 06:25:39
import sys, os
sys.path.insert(0, os.path.abspath('..'))
extensions = [
 'sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.viewcode']
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'Winterstone'
copyright = '2011, Averrin'
version = '0.8.6.6'
release = '0.8.6.6'
exclude_patterns = [
 '_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = [
 '_static']
htmlhelp_basename = 'Winterstonedoc'
latex_documents = [
 ('index', 'Winterstone.tex', 'Winterstone Documentation', 'Averrin', 'manual')]
man_pages = [
 (
  'index', 'winterstone', 'Winterstone Documentation',
  [
   'Averrin'], 1)]