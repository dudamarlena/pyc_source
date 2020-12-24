# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rgeda/project/repo/webbpsf/astropy_helpers/astropy_helpers/sphinx/conf.py
# Compiled at: 2019-07-20 17:47:20
# Size of source mod 2**32: 11549 bytes
import os, sys, warnings
from os import path
import sphinx
from distutils.version import LooseVersion
needs_sphinx = '1.3'
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

def check_sphinx_version(expected_version):
    sphinx_version = LooseVersion(sphinx.__version__)
    expected_version = LooseVersion(expected_version)
    if sphinx_version < expected_version:
        raise RuntimeError('At least Sphinx version {0} is required to build this documentation.  Found {1}.'.format(expected_version, sphinx_version))


intersphinx_mapping = {'python':('https://docs.python.org/3/', (None, 'http://data.astropy.org/intersphinx/python3.inv')), 
 'pythonloc':(
  'http://docs.python.org/',
  path.abspath(path.join(path.dirname(__file__), 'local/python3_local_links.inv'))), 
 'numpy':('https://docs.scipy.org/doc/numpy/', (None, 'http://data.astropy.org/intersphinx/numpy.inv')), 
 'scipy':('https://docs.scipy.org/doc/scipy/reference/', (None, 'http://data.astropy.org/intersphinx/scipy.inv')), 
 'matplotlib':('http://matplotlib.org/', (None, 'http://data.astropy.org/intersphinx/matplotlib.inv')), 
 'astropy':('http://docs.astropy.org/en/stable/', None), 
 'h5py':('http://docs.h5py.org/en/stable/', None)}
exclude_patterns = [
 '_build']
source_suffix = '.rst'
master_doc = 'index'
default_role = 'obj'
rst_epilog = '\n.. _Astropy: http://astropy.org\n'
suppress_warnings = [
 'app.add_directive']
extensions = [
 'sphinx.ext.autodoc',
 'sphinx.ext.intersphinx',
 'sphinx.ext.todo',
 'sphinx.ext.coverage',
 'sphinx.ext.inheritance_diagram',
 'sphinx.ext.viewcode',
 'astropy_helpers.extern.numpydoc',
 'astropy_helpers.extern.automodapi.automodapi',
 'astropy_helpers.extern.automodapi.smart_resolver',
 'astropy_helpers.sphinx.ext.tocdepthfix',
 'astropy_helpers.sphinx.ext.doctest',
 'astropy_helpers.sphinx.ext.changelog_links']
if (on_rtd or LooseVersion(sphinx.__version__)) < LooseVersion('1.4'):
    extensions.append('sphinx.ext.pngmath')
else:
    extensions.append('sphinx.ext.mathjax')
try:
    import matplotlib.sphinxext.plot_directive
    extensions += [matplotlib.sphinxext.plot_directive.__name__]
except (ImportError, AttributeError):
    warnings.warn("matplotlib's plot_directive could not be imported. Inline plots will not be included in the output")

numpydoc_show_class_members = False
autosummary_generate = True
automodapi_toctreedirnm = 'api'
autoclass_content = 'both'
graphviz_output_format = 'svg'
graphviz_dot_args = [
 '-Nfontsize=10',
 '-Nfontname=Helvetica Neue, Helvetica, Arial, sans-serif',
 '-Efontsize=10',
 '-Efontname=Helvetica Neue, Helvetica, Arial, sans-serif',
 '-Gfontsize=10',
 '-Gfontname=Helvetica Neue, Helvetica, Arial, sans-serif']
html_theme_path = [
 path.abspath(path.join(path.dirname(__file__), 'themes'))]
html_theme = 'bootstrap-astropy'
html_sidebars = {'**':[
  'localtoc.html'], 
 'search':[],  'genindex':[],  'py-modindex':[]}
html_favicon = path.join(html_theme_path[0], html_theme, 'static', 'astropy_logo.ico')
html_last_updated_fmt = '%d %b %Y'
latex_toplevel_sectioning = 'part'
latex_elements = {}
latex_elements['preamble'] = '\n% Use a more modern-looking monospace font\n\\usepackage{inconsolata}\n\n% The enumitem package provides unlimited nesting of lists and enums.\n% Sphinx may use this in the future, in which case this can be removed.\n% See https://bitbucket.org/birkenfeld/sphinx/issue/777/latex-output-too-deeply-nested\n\\usepackage{enumitem}\n\\setlistdepth{15}\n\n% In the parameters section, place a newline after the Parameters\n% header.  (This is stolen directly from Numpy\'s conf.py, since it\n% affects Numpy-style docstrings).\n\\usepackage{expdlist}\n\\let\\latexdescription=\\description\n\\def\\description{\\latexdescription{}{} \\breaklabel}\n\n% Support the superscript Unicode numbers used by the "unicode" units\n% formatter\n\\DeclareUnicodeCharacter{2070}{\\ensuremath{^0}}\n\\DeclareUnicodeCharacter{00B9}{\\ensuremath{^1}}\n\\DeclareUnicodeCharacter{00B2}{\\ensuremath{^2}}\n\\DeclareUnicodeCharacter{00B3}{\\ensuremath{^3}}\n\\DeclareUnicodeCharacter{2074}{\\ensuremath{^4}}\n\\DeclareUnicodeCharacter{2075}{\\ensuremath{^5}}\n\\DeclareUnicodeCharacter{2076}{\\ensuremath{^6}}\n\\DeclareUnicodeCharacter{2077}{\\ensuremath{^7}}\n\\DeclareUnicodeCharacter{2078}{\\ensuremath{^8}}\n\\DeclareUnicodeCharacter{2079}{\\ensuremath{^9}}\n\\DeclareUnicodeCharacter{207B}{\\ensuremath{^-}}\n\\DeclareUnicodeCharacter{00B0}{\\ensuremath{^{\\circ}}}\n\\DeclareUnicodeCharacter{2032}{\\ensuremath{^{\\prime}}}\n\\DeclareUnicodeCharacter{2033}{\\ensuremath{^{\\prime\\prime}}}\n\n% Make the "warning" and "notes" sections use a sans-serif font to\n% make them stand out more.\n\\renewenvironment{notice}[2]{\n  \\def\\py@noticetype{#1}\n  \\csname py@noticestart@#1\\endcsname\n  \\textsf{\\textbf{#2}}\n}{\\csname py@noticeend@\\py@noticetype\\endcsname}\n'
linkcheck_timeout = 60