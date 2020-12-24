# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/futurefinity/template.py
# Compiled at: 2016-06-10 18:06:56
# Size of source mod 2**32: 3646 bytes
from typing import Union
import asyncio, os, functools
try:
    from jinja2 import Template
except ImportError:
    Template = None

def render_template(template_name: str):
    """
    Decorator to render template gracefully.

    Only effective when nothing is written.

    Example:

    .. code-block:: python3

      @render_template("index.htm")
      async def get(self, *args, **kwargs):
          return {'content': 'Hello, World!!'}

    """

    def decorator(f):

        @functools.wraps(f)
        async def wrapper(self, *args, **kwargs):
            template_dict = await f(self, *args, **kwargs)
            if self._body_written:
                return
            self.render(template_name, template_dict)

        return wrapper

    return decorator


class TemplateLoader:
    __doc__ = '\n    The TemplateLoader.\n\n    The Default template loader of FutureFinity.\n    '

    def __init__(self, template_path: Union[(list, str)], cache_template: bool=True):
        if Template is None:
            raise NotImplementedError('Currently, `futurefinity.template` needs Jinja2 to work. Please install it before using template rendering.')
        if isinstance(template_path, str):
            self.template_path = [
             template_path]
        else:
            if isinstance(template_path, list):
                self.template_path = template_path
            else:
                raise ValueError('Unsupported template_path type.')
        self.cache_template = cache_template
        self._template_cache = {}

    def find_abs_path(self, template_name: str) -> str:
        """
        Find the absolute path of the template from the template_path.

        If no matched file found, it will raise a ``FileNotFoundError``.
        """
        for current_path in self.template_path:
            file_path = os.path.join(os.path.realpath(current_path), template_name)
            if os.path.exists(file_path):
                return file_path

        raise FileNotFoundError('No such file %s in template_path' % repr(template_name))

    def load_template_file_content(self, file_path):
        """
        Load a file synchronously. This function can be put into a thread
        executor to load the file content concurrently.
        """
        with open(file_path) as (tpl):
            return tpl.read()

    def load_template(self, template_name: str) -> 'Template':
        """
        Load and parse the template.
        """
        if template_name in self._template_cache:
            return self._template_cache[template_name]
        file_path = self.find_abs_path(template_name)
        template_content = self.load_template_file_content(file_path)
        parsed_tpl = Template(template_content)
        if self.cache_template:
            self._template_cache[template_name] = parsed_tpl
        return parsed_tpl