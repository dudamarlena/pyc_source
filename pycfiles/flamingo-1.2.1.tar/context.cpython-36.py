# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/context.py
# Compiled at: 2020-03-11 04:50:15
# Size of source mod 2**32: 8028 bytes
import logging, shutil, os
from flamingo.core.data_model import ContentSet, AND, NOT, OR, Q, F
from flamingo.core.plugins.plugin_manager import PluginManager
from flamingo.core.parser import FileParser, ParsingError
from flamingo.core.plugins.media import add_media
from flamingo.core.utils.imports import acquire
from flamingo.core.types import OverlayObject

class Context(OverlayObject):
    _Context__overlay_ignore_attributes = [
     'content',
     'contents']

    def __init__(self, settings, contents=None, setup=True):
        super().__init__()
        self.settings = settings
        self.contents = contents
        self.content = None
        self.plugins = None
        if setup:
            self.setup()

    def setup(self):
        self.errors = []
        self.logger = logging.getLogger('flamingo')
        self.logger.debug('setting up context')
        self.plugins = PluginManager(self)
        self.plugins.run_plugin_hook('setup')
        self.plugins.run_plugin_hook('settings_setup')
        self.parser = FileParser(context=self)
        self.plugins.run_plugin_hook('parser_setup')
        templating_engine_class, path = acquire(self.settings.TEMPLATING_ENGINE)
        self.templating_engine = templating_engine_class(self)
        self.plugins.run_plugin_hook('templating_engine_setup', self.templating_engine)
        self.contents = self.contents or ContentSet()
        self.parse_all()
        self.plugins.run_plugin_hook('context_setup')

    def parse(self, content):
        previous_content = self.content
        self.content = content
        path = os.path.join(self.settings.CONTENT_ROOT, content['path'])
        self.logger.debug('reading %s ', path)
        try:
            try:
                self.parser.parse(path, content)
                self.plugins.run_plugin_hook('content_parsed', content)
            except ParsingError as e:
                content['_parsing_error'] = e
                self.errors.append(e)
                if hasattr(e, 'line'):
                    line = e.line
                    if content['content_offset']:
                        line += content['content_offset']
                    self.logger.error('%s:%s: %s', path, line, e)
                else:
                    self.logger.error('%s: %s', path, e)
            except Exception as e:
                content['_parsing_error'] = e
                self.errors.append(e)
                self.logger.error('exception occoured while reading %s', (content['path']),
                  exc_info=True)

        finally:
            self.content = previous_content

    def parse_all(self):
        self.content = None
        for path in self.get_source_paths():
            self.contents.add(path=(os.path.relpath(path, self.settings.CONTENT_ROOT)))

        for content in self.contents:
            if content['content_body']:
                pass
            else:
                self.parse(content)

        self.content = None
        self.plugins.run_plugin_hook('contents_parsed')

    def get_source_paths(self):
        self.logger.debug('searching for content')
        supported_extensions = self.parser.get_extensions()
        if self.settings.CONTENT_PATHS:
            self.logger.debug('using user defined content paths')
            for path in self.settings.CONTENT_PATHS:
                path = os.path.join(self.settings.CONTENT_ROOT, path)
                if not os.path.exists(path):
                    continue
                extension = os.path.splitext(path)[1][1:]
                if extension not in supported_extensions:
                    self.logger.debug("skipping '%s'. extension '%s' is not supported", path, extension)
                else:
                    yield path

        else:
            self.logger.debug('searching content with extension %s recursive in %s', repr(supported_extensions), self.settings.CONTENT_ROOT)
            for root, dirs, files in os.walk((self.settings.CONTENT_ROOT),
              followlinks=(self.settings.FOLLOW_LINKS)):
                for name in files:
                    extension = os.path.splitext(name)[1][1:]
                    if extension not in supported_extensions:
                        pass
                    else:
                        yield os.path.join(root, name)

    def render(self, content, template_name=''):
        template_name = template_name or content['template']
        self.logger.debug('rendering %s using %s', content['path'] or content, template_name)
        if not template_name:
            content['template_context'] = {}
            return content['content_body'] or ''
        else:
            template_context = {**{'content':content, 
             'context':self, 
             'AND':AND, 
             'NOT':NOT, 
             'OR':OR, 
             'Q':Q, 
             'F':F}, **(self.settings.EXTRA_CONTEXT)}
            if self.settings.PRE_RENDER_CONTENT:
                if content.get('is_template', True):
                    if not content['_content_body_rendered']:
                        self.logger.debug('pre rendering %s', content['path'] or content)
                        exitcode, output = self.templating_engine.pre_render_content(content, template_context)
                        if exitcode:
                            content['content_body'] = output
                            content['_content_body_rendered'] = True
                        else:
                            return output
            output = self.templating_engine.render(template_name, template_context)
            content['template_context'] = template_context
            return output

    def rm_rf(self, path, force=False):
        if self.settings.SKIP_FILE_OPERATIONS:
            if not force:
                return
        else:
            self.logger.debug('rm -rf %s', path)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)

    def mkdir_p(self, path, force=False):
        if self.settings.SKIP_FILE_OPERATIONS:
            if not force:
                return
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            self.logger.debug('mkdir -p %s', dirname)
            os.makedirs(dirname)

    def cp(self, source, destination, force=False):
        if self.settings.SKIP_FILE_OPERATIONS:
            if not force:
                return
        self.mkdir_p(destination)
        self.logger.debug('cp %s %s', source, destination)
        shutil.copy(source, destination)

    def write(self, path, text, mode='w+', force=False):
        if self.settings.SKIP_FILE_OPERATIONS:
            if not force:
                return
        self.logger.debug("writing '%s", path)
        with open(path, mode) as (f):
            f.write(text)

    def add_media(self, name, content=None, **extra_meta_data):
        content = content or self.content
        return add_media(name=name, context=self, content=content, **extra_meta_data)

    def build(self, clean=True):
        self.plugins.run_plugin_hook('pre_build')
        if clean:
            if os.path.exists(self.settings.OUTPUT_ROOT):
                self.rm_rf(self.settings.OUTPUT_ROOT)
        else:
            if self.settings.CONTENT_PATHS:
                contents = self.contents.filter(Q(path__in=(self.settings.CONTENT_PATHS)) | Q(i18n_path__in=(self.settings.CONTENT_PATHS)))
            else:
                contents = self.contents
        for content in contents:
            output_path = os.path.join(self.settings.OUTPUT_ROOT, content['output'])
            self.mkdir_p(output_path)
            self.write(output_path, self.render(content))

        self.plugins.run_plugin_hook('post_build')