# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/template/jinja2_.py
# Compiled at: 2012-05-23 13:16:55
from __future__ import unicode_literals
from os import path
try:
    from jinja2 import Environment, BaseLoader, TemplateNotFound
except ImportError:
    raise ImportError(b'You must install the jinja2 package.')

__all__ = [
 b'Jinja2']

class AbsolutePathLoader(BaseLoader):
    """Loads templates from an absolute path on the filesystem.
    
    Similar to the FileSystemLoader but without explicit search paths.
    """

    def __init__(self, encoding=b'utf-8'):
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

        return (contents, filename, uptodate)


class Jinja2(object):

    def __init__(self, **options):
        self.environment = Environment(loader=AbsolutePathLoader())

    def __call__(self, data, template, content_type=b'text/html', **options):
        template = self.environment.get_template(template)
        return (
         content_type, template.render(data))