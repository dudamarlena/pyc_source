# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/rst/sphinx_compat.py
# Compiled at: 2020-03-20 20:42:04
# Size of source mod 2**32: 6013 bytes
from tempfile import TemporaryDirectory
from copy import deepcopy
import shutil, os
from sphinx.jinja2glue import _tobool, _todim, _toint
from sphinx.config import Config
import sphinx
from docutils.parsers.rst import Directive, directives
from docutils.nodes import raw, title

def toctree(context):

    class TOCTree(Directive):
        has_content = True

        def run(self):
            context.content['toctree_options'] = {}
            context.content['toctree'] = []
            for line in self.content:
                if not line:
                    continue
                context.content['toctree'].append(str(line))

            return []

    return TOCTree


class StyleSheet:

    def __init__(self, filename):
        self.filename = filename


def gen_sphinx_template_context():
    config = Config()
    context = {'embedded':False, 
     'project':config.project, 
     'release':'', 
     'version':config.version, 
     'last_updated':'', 
     'copyright':config.copyright, 
     'master_doc':config.master_doc, 
     'use_opensearch':False, 
     'docstitle':'foo', 
     'shorttitle':'foo', 
     'show_copyright':False, 
     'show_sphinx':False, 
     'has_source':False, 
     'show_source':'', 
     'sourcelink_suffix':'', 
     'file_suffix':'', 
     'link_suffix':'', 
     'language':config.language, 
     'css_files':[],  'script_files':[],  'sphinx_version':'', 
     'style':'', 
     'rellinks':[],  'builder':'', 
     'parents':[],  'logo':'', 
     'favicon':'', 
     'html5_doctype':'', 
     'hasdoc':lambda *args, **kwargs: False, 
     'gettext':lambda *args, **kwargs: '', 
     'pathto':lambda *args, **kwargs: '#', 
     'css_tag':lambda s: '<link rel="stylesheet" href="{}" type="text/css" />'.format(s.filename), 
     'js_tag':lambda s: '<script src="{}"></script>'.format(s.filename)}
    return deepcopy(context)


class rstSphinxCompat:
    THEME_NAME = 'classic'

    def __init__(self, *args, **kwargs):
        self.temp_dir = TemporaryDirectory()
        os.makedirs(os.path.join(self.temp_dir.name, 'templates'))
        os.makedirs(os.path.join(self.temp_dir.name, 'static'))
        sphinx_theme_root = os.path.join(os.path.dirname(sphinx.__file__), 'themes')
        for i in os.listdir(sphinx_theme_root):
            os.symlink(os.path.join(sphinx_theme_root, i), os.path.join(self.temp_dir.name, 'templates', i))

        self.THEME_PATHS = [
         self.temp_dir.name]
        print(self.THEME_PATHS)

    def rst_document_parsed(self, context, document):

        def callback(text):
            return '{} <a href="#"></a>'.format(text)

        def gen_toc(children, toc, level=1):
            for child in children[:]:
                if isinstance(child, title):
                    toc.append((child.astext(), level))
                    new_text = callback(child.astext())
                    child.children = [
                     raw('', new_text, format='html')]

        context.content['toc'] = []
        gen_toc(document.children, context.content['toc'])

    def templating_engine_setup(self, context, templating_engine):
        templating_engine.env.filters['tobool'] = _tobool
        templating_engine.env.filters['toint'] = _toint
        templating_engine.env.filters['todim'] = _todim
        sphinx_theme_path = os.path.join(os.path.dirname(sphinx.__file__), 'themes', self.THEME_NAME)
        sphinx_theme_static_root = os.path.join(sphinx_theme_path, 'static')
        theme_static_root = os.path.join(self.temp_dir.name, 'static')
        for static_file in os.listdir(sphinx_theme_static_root):
            if static_file.endswith('_t'):
                template_name = os.path.join('static', static_file)
                template_context = gen_sphinx_template_context()
                destination = os.path.join(theme_static_root, static_file[:-2])
                with open(destination, 'w+') as (f):
                    f.write(templating_engine.render(template_name, template_context))
                continue
            source = os.path.join(sphinx_theme_static_root, static_file)
            destination = os.path.join(theme_static_root, static_file)
            shutil.copy(source, destination)

    def template_context_setup(self, context, content, template_name, template_context):
        template_context.clear()
        sphinx_template_context = gen_sphinx_template_context()
        for i in os.listdir(os.path.join(self.temp_dir.name, 'static')):
            if i.endswith('.css'):
                sphinx_template_context['css_files'].append(StyleSheet(os.path.join('/static', i)))
            if i.endswith('.js'):
                continue
                sphinx_template_context['script_files'].append(StyleSheet(os.path.join('/static', i)))

        for k, v in sphinx_template_context.items():
            template_context[k] = v

        template_context['body'] = content['content_body']
        template_context['context'] = context
        template_context['content'] = content

    def parser_setup(self, context):
        directives.register_directive('toctree', toctree(context))

    def contents_parsed(self, context):
        context.settings.MENU = []
        contents = context.contents.filter(toctree__isnull=False)