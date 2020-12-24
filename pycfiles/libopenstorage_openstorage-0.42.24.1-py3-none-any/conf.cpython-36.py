# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/importlib-metadata/importlib_metadata/docs/conf.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 5468 bytes
extensions = [
 'rst.linker',
 'sphinx.ext.autodoc',
 'sphinx.ext.coverage',
 'sphinx.ext.doctest',
 'sphinx.ext.intersphinx',
 'sphinx.ext.viewcode']
templates_path = [
 '_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'importlib_metadata'
copyright = '2017-2019, Jason R. Coombs, Barry Warsaw'
author = 'Jason R. Coombs, Barry Warsaw'
version = '0.1'
release = '0.1'
language = None
exclude_patterns = [
 '_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'default'
html_sidebars = {'**': [
        'relations.html',
        'searchbox.html']}
htmlhelp_basename = 'importlib_metadatadoc'
latex_elements = {}
latex_documents = [
 (
  master_doc, 'importlib_metadata.tex',
  'importlib\\_metadata Documentation',
  'Brett Cannon, Barry Warsaw', 'manual')]
man_pages = [
 (
  master_doc, 'importlib_metadata', 'importlib_metadata Documentation',
  [
   author], 1)]
texinfo_documents = [
 (
  master_doc, 'importlib_metadata', 'importlib_metadata Documentation',
  author, 'importlib_metadata', 'One line description of project.',
  'Miscellaneous')]
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
link_files = {'changelog.rst': dict(replace=[
                   dict(pattern='^(?m)((?P<scm_version>v?\\d+(\\.\\d+){1,2}))\\n[-=]+\\n',
                     with_scm='{text}\n{rev[timestamp]:%Y-%m-%d}\n\n')])}