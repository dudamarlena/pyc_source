# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ws/project/ws_rfid/snappets/doc/conf.py
# Compiled at: 2018-09-20 20:34:36
import sys, os

def setdefaultencoding(encoding=None, quiet=False):
    if encoding is None:
        encoding = 'utf-8'
    try:
        isinstance('', basestring)
        if not hasattr(sys, '_setdefaultencoding'):
            reload(sys)
            setattr(sys, '_setdefaultencoding', getattr(sys, 'setdefaultencoding'))
        sys._setdefaultencoding(encoding)
    except NameError:
        pass

    return


setdefaultencoding('utf-8')
try:
    printf = eval('print')
except SyntaxError:
    printf_dict = dict()
    try:
        exec 'from __future__ import print_function\nprintf=print' in printf_dict
        printf = printf_dict['printf']
    except SyntaxError:

        def printf(*args, **kwd):
            fout = kwd.get('file', sys.stdout)
            w = fout.write
            if args:
                w(str(args[0]))
            sep = kwd.get('sep', ' ')
            for a in args[1:]:
                w(sep)
                w(str(a))

            w(kwd.get('end', '\n'))


    del printf_dict

try:
    ('{0}').format(0)

    def sformat(fmtspec, *args, **kwargs):
        return fmtspec.format(*args, **kwargs)


except AttributeError:
    try:
        import stringformat

        def sformat(fmtspec, *args, **kwargs):
            return stringformat.FormattableString(fmtspec).format(*args, **kwargs)


    except ImportError:
        printf('error: stringformat missing. Try `easy_install stringformat`.', file=sys.stderr)

printe = printf
dbg_fwid = globals().get('dbg_fwid', 15)
_last_local = None
_new_path = []
_std_path = []
for _dir in sys.path:
    if _dir.startswith('/usr/local/'):
        _last_local = _dir
    elif _dir.endswith('/dist-packages') or _dir.endswith('/site-packages'):
        _std_path.append(_dir)
        continue
    _new_path.append(_dir)

if _std_path and _last_local is not None:
    _first_std_indx = sys.path.index(_std_path[0])
    _last_local_indx = sys.path.index(_last_local)
    if _last_local_indx > _first_std_indx:
        printe(sformat('#    :PRC:    moved {0} from {1} to {2}', _std_path, [ sys.path.index(_d) for _d in _std_path ], _last_local_indx + 1))
        _insert_indx = _new_path.index(_last_local) + 1
        _new_path[_insert_indx:_insert_indx] = _std_path
        sys.path = _new_path
here = os.path.abspath(os.path.dirname(__file__))
top_dir = os.path.abspath(os.path.join(here, os.path.pardir))
sys.path.insert(0, top_dir)
project = 'Snappets'
copyright = '2018, Wolfgang Scherer'
author = 'Wolfgang Scherer'
with open(os.path.join(top_dir, '.version'), 'r') as (fh):
    release = fh.read().strip()
version = ('.').join(release.split('.')[:3])
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
language = None
exclude_patterns = [
 '_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = [
 '_static']
htmlhelp_basename = 'Snappetsdoc'
latex_elements = {}
latex_documents = [
 (
  master_doc, 'Snappets.tex', 'Snappets Documentation',
  'Wolfgang Scherer', 'manual')]
man_pages = [
 (
  master_doc, 'snappets', 'Snappets Documentation',
  [
   author], 1)]
texinfo_documents = [
 (
  master_doc, 'Snappets', 'Snappets Documentation',
  author, 'Snappets', 'One line description of project.',
  'Miscellaneous')]
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = [
 'search.html']
intersphinx_mapping = {'https://docs.python.org/': None}
todo_include_todos = True
my_preferred_themes = [
 'bootstrap',
 'guzzle',
 'sphinx_rtd_theme',
 'alabaster',
 'default']
for _my_preferred_theme in my_preferred_themes:
    if _my_preferred_theme == 'bootstrap':
        try:
            import sphinx_bootstrap_theme
            printe(sformat('#    :DBG:    {1:<{0}s}: ]{2!s}[', dbg_fwid, 'bootstrap', sphinx_bootstrap_theme.__version__))
            html_theme = 'bootstrap'
            html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
            html_theme_options = {'navbar_title': project, 
               'navbar_links': [], 'bootswatch_theme': 'flatly'}
            break
        except ImportError:
            continue

    if _my_preferred_theme == 'guzzle':
        try:
            import guzzle_sphinx_theme
            html_theme = 'guzzle_sphinx_theme'
            html_translator_class = 'guzzle_sphinx_theme.HTMLTranslator'
            html_theme_path = guzzle_sphinx_theme.html_theme_path()
            extensions.append('guzzle_sphinx_theme')
            html_theme_options = {'project_nav_name': project}
            break
        except ImportError:
            continue

    if _my_preferred_theme == 'sphinx_rtd_theme':
        try:
            import sphinx_rtd_theme
            html_theme = 'sphinx_rtd_theme'
            html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
            break
        except ImportError:
            continue

    if _my_preferred_theme == 'alabaster':
        try:
            import alabaster
            html_theme = 'alabaster'
            break
        except ImportError:
            continue

    html_theme = 'default'
    break

source_suffix = [
 '.rst', '.rst.auto']
latex_elements = {}
latex_elements['papersize'] = 'a4paper'
latex_elements['pointsize'] = '10pt'
latex_elements['preamble'] = '\n%% box drawing characters used for e.g. RAKE symbol\n\\usepackage{pmboxdraw}\n\\ifdefined\\DeclareUnicodeCharacter\n%% check mark\n\\DeclareUnicodeCharacter{221A}{{\\tiny \\raisebox{1ex}[\\ht\\strutbox][0pt]{$\\sqrt{}$}}}\n\\fi\n'
imgmath_image_format = 'svg'
extensions.append('sphinx.ext.graphviz')
graphviz_output_format = 'svg'
try:
    import du_comment_role
    extensions.append('du_comment_role')
except:
    from docutils.parsers.rst import directives
    from docutils.parsers.rst.languages import en
    from docutils.parsers.rst.roles import register_canonical_role

    def icomment_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
        return ([], [])


    en.roles['icomment'] = 'icomment'
    register_canonical_role('comment', icomment_role)
    icomment_role.options = {'format': directives.unchanged, 
       'raw': directives.flag}
    en.roles['span'] = 'span'
    register_canonical_role('span', icomment_role)

check_extensions = []
check_extensions.append('sphinxcontrib.plantuml')
plantuml_output_format = 'svg'
plantuml_latex_output_format = 'pdf'
check_extensions.append('sphinxcontrib.needs')
check_extensions.append('sphinxcontrib.mercurial')
for _ext in check_extensions:
    try:
        exec 'import ' + _ext in {}
        extensions.append(_ext)
    except:
        print ('warning: extension {0} failed').format(_ext)

def setup(app):
    if os.path.exists('_static/bootstrap3-sub-menu.css'):
        app.add_stylesheet('bootstrap3-sub-menu.css')
    if os.path.exists('_static/wsx-tables.js'):
        app.add_javascript('wsx-tables.js')