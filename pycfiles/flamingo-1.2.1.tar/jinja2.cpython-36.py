# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/templating/jinja2.py
# Compiled at: 2020-02-26 05:03:46
# Size of source mod 2**32: 9614 bytes
import traceback, datetime, tempfile, hashlib, logging, code, html, os
from jinja2 import Environment, FileSystemLoader, contextfunction
from jinja2 import TemplateNotFound, TemplateSyntaxError
from flamingo.core.templating.base import TemplatingEngine
from flamingo.core.errors import ObjectDoesNotExist
from flamingo.core.utils.imports import acquire
from flamingo.core.utils.pprint import pformat
from flamingo import THEME_ROOT
try:
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
    from pygments.util import ClassNotFound
    from pygments import highlight as pygments_highlight
    PYGMENTS = True
except ImportError:
    PYGMENTS = False

try:
    import IPython
    IPYTHON = True
except ImportError:
    IPYTHON = False

ERROR_TEMPLATE = os.path.join(os.path.dirname(__file__), 'jinja2_error.html')
logger = logging.getLogger('flamingo.core.templating.Jinja2')

def silent_none(value):
    if value is None:
        return ''
    else:
        return value


def html_escape(obj):
    if not isinstance(obj, str):
        obj = str(obj)
    return html.escape(obj)


@contextfunction
def _shell(context):
    if IPYTHON:
        IPython.embed()
    else:
        code.interact(local=(globals()))


def _import(*args, **kwargs):
    return acquire(*args, **kwargs)[0]


@contextfunction
def link(context, path, name='', lang=''):
    i18n = 'flamingo.plugins.I18N' in context['context'].settings.PLUGINS
    try:
        content = context['context'].contents.get(path=path)
    except ObjectDoesNotExist:
        content = None

    if content:
        if i18n:
            lang = lang or context['content']['lang']
            if content['lang'] != lang:
                content = context['context'].contents.get(id=(content['id']), lang=lang)
    if not content:
        content_path = context['content']['path']
        if not content_path:
            if i18n:
                if context['content']['translations']:
                    content_path = context['content']['translations'].values('path')[0]
        context['context'].logger.error('%s: can not resolve link target ("%s", "%s")', content_path, path, name)
        return ''
    else:
        if not name:
            return content['url']
        return '<a href="{}">{}</a>'.format(content['url'], name)


class FlamingoEnvironment(Environment):

    def __init__(self, flamingo_context, *args, **kwargs):
        self.flamingo_context = flamingo_context
        (super().__init__)(*args, **kwargs)

    def get_template(self, *args, **kwargs):
        template_name = args[0]
        if '.' in template_name:
            return (super().get_template)(*args, **kwargs)
        else:
            try:
                expression = self.compile_expression(template_name)
                template_name = expression(**dict(self.flamingo_context.settings))
            except Exception:
                template_name = ''

            if template_name:
                return (super().get_template)(template_name, *(args[1:]), **kwargs)
            return (super().get_template)(*args, **kwargs)


class Jinja2(TemplatingEngine):

    def __init__(self, context):
        super().__init__(context)
        self.contents = {}
        self.tempdir = tempfile.TemporaryDirectory()
        template_dirs = [os.path.join(i, 'templates') for i in self.theme_paths] + [
         self.tempdir.name]
        self.env = FlamingoEnvironment(context,
          loader=(FileSystemLoader(template_dirs)),
          finalize=silent_none)
        self.env.globals['link'] = link
        self.env.globals['import'] = _import
        self.env.globals['_shell'] = _shell
        if self.context.settings.LIVE_SERVER_RUNNING:
            if self.context.settings.JINJA2_TRACEBACKS:
                autoescape = not self.context.settings.JINJA2_TRACEBACKS_PYGMENTS
                self.error_env = Environment(loader=(FileSystemLoader([
                 os.path.join(THEME_ROOT, 'templates/jinja2')])),
                  autoescape=autoescape,
                  finalize=silent_none)
                self.error_env.globals['gen_snippet'] = self.gen_snippet
                self.error_env.globals['pformat'] = pformat
                self.error_env.globals['html_escape'] = html_escape
                self.error_env.globals['_shell'] = _shell

    def gen_snippet(self, path, lineno, show_linenos=True):
        context_lines = self.context.settings.JINJA2_TRACEBACKS_CONTEXT_LINES
        index = lineno - 1
        lines = open(path, 'r').read().splitlines()
        context_lines_top = lines[index - context_lines:index]
        context_lines_bottom = lines[index + 1:index + context_lines + 1]
        for line in context_lines_top[:]:
            if line:
                break
            context_lines_top.remove(line)

        for line in context_lines_bottom[::-1]:
            if line:
                break
            context_lines_bottom.pop()

        snippet = '\n'.join([
         *context_lines_top,
         
          lines[index],
         *context_lines_bottom])
        try:
            lexer = get_lexer_for_filename(path)
        except ClassNotFound:
            lexer = get_lexer_by_name('text')

        if show_linenos:
            formatter = HtmlFormatter(linenos='inline',
              hl_lines=[
             len(context_lines_top) + 1],
              linenostart=(lineno - len(context_lines_top)))
        else:
            formatter = HtmlFormatter(hl_lines=[
             len(context_lines_top) + 1])
        return pygments_highlight(snippet, lexer, formatter)

    def _render_exception(self, exception):
        stack = []
        for frame in traceback.extract_tb(exception.__traceback__)[::-1]:
            filename = frame.filename
            content_path = ''
            if filename in self.contents:
                content_path = self.contents[filename]['path']
                if not content_path:
                    if self.contents[filename]['original_path']:
                        content_path = self.contents[filename]['original_path']
            stack.append((
             filename, frame.lineno, content_path))

        if isinstance(exception, (TemplateSyntaxError, TemplateNotFound)):
            stack = [i for i in stack if os.path.splitext(i[0])[1] != '.py']
        if isinstance(exception, TemplateSyntaxError):
            if len(stack) > 1:
                if stack[0] == stack[(-1)]:
                    stack = stack[:-1]
        template = self.error_env.get_template('error.html')
        return template.render(context=(self.context),
          exception=exception,
          stack=stack,
          TemplateNotFound=TemplateNotFound,
          isinstance=isinstance)

    def _render(self, template_name, template_context, handle_exceptions=True):
        if not self.context.settings.LIVE_SERVER_RUNNING or not self.context.settings.JINJA2_TRACEBACKS:
            return (True,
             (self.env.get_template(template_name).render)(**template_context))
        else:
            if 'content' in template_context and '_parsing_error' in template_context['content']:
                exception = template_context['content']['_parsing_error']
            else:
                exception = None
            try:
                return (
                 True,
                 (self.env.get_template(template_name).render)(**template_context))
            except Exception as e:
                logger.debug(e, exc_info=True)
                exception = e

            if not handle_exceptions:
                raise exception
            try:
                return (
                 False, self._render_exception(exception))
            except Exception as e:
                logger.error('Exception occurred while rendering %s', e,
                  exc_info=True)

        raise exception

    def render(self, template_name, template_context, handle_exceptions=True):
        return self._render(template_name, template_context, handle_exceptions)[1]

    def pre_render_content(self, content, template_context):
        if not content['content_body'] or '{' not in content['content_body']:
            return (
             True, content['content_body'])
        if not self.context.settings.LIVE_SERVER_RUNNING or not self.context.settings.JINJA2_TRACEBACKS:
            template = self.env.from_string(content['content_body'])
            return (
             True, (template.render)(**template_context))
        path = ''
        try:
            content_path = content['path']
            if not content_path:
                if content['original_path']:
                    content_path = content['original_path']
                else:
                    content_path = ''
            name = '{}{}'.format(hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest(), os.path.splitext(content_path)[1])
            path = os.path.join(self.tempdir.name, name)
            self.contents[path] = content
            with open(path, 'w+') as (f):
                f.write(content['content_body'])
            return self._render(name, template_context)
        finally:
            if path:
                if path in self.contents:
                    self.contents.pop(path)