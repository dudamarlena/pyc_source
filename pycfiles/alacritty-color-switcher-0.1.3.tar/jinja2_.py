# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/template/jinja2_.py
# Compiled at: 2010-03-23 13:32:22
from os import path
try:
    from jinja2 import Environment, BaseLoader, TemplateNotFound
except ImportError:
    raise ImportError('You must install the jinja2 package.')

__all__ = [
 'Jinja2']

class AbsolutePathLoader(BaseLoader):
    """Loads templates from an absolute path on the filesystem.
    
    Similar to the FileSystemLoader but without explicit search paths.
    """

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding

    def get_source(self, environment, template):
        filename = path.abspath(template)
        if not path.exists(filename):
            raise TemplateNotFound(template)
        f = file(filename)
        try:
            contents = f.read().decode(self.encoding)
        finally:
            f.close()

        mtime = path.getmtime(filename)

        def uptodate():
            try:
                return path.getmtime(filename) == mtime
            except OSError:
                return False

        return (
         contents, filename, uptodate)


class Jinja2(object):

    def __init__(self, **options):
        self.environment = Environment(loader=AbsolutePathLoader())

    def __call__(self, data, template, content_type='text/plain', **options):
        template = self.environment.get_template(template)
        return (
         content_type, template.render(data))