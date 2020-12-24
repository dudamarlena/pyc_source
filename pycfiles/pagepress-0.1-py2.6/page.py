# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/pagepress/page.py
# Compiled at: 2012-03-23 03:34:40
import datetime

class Page:

    def __init__(self, generator, path, mtime, content, **kwargs):
        self.generator = generator
        self.path = path
        self.content = content
        self.mtime = mtime
        self.metadata = kwargs

    def change_extension(self, extension):
        i = self.path[(-1)].rfind('.')
        basename = self.path[(-1)][0:i]
        self.path[-1] = basename + extension

    def url(self):
        return '/' + ('/').join(self.path)

    def render(self, **kwargs):
        return self.content


class Templated(Page):
    template_extension = '.mako'

    def __init__(self, generator, **kwargs):
        template_name = kwargs.pop('template', None)
        Page.__init__(self, generator, **kwargs)
        if not template_name:
            template_path = self.path[:]
            i = self.path[(-1)].rfind('.')
            basename = self.path[(-1)][0:i]
            template_path[-1] = basename + self.template_extension
            template_name = ('/').join(template_path)
            self.change_extension('.html')
        else:
            i = template_name.rfind('.')
            if template_name[i:] == '.mako':
                self.change_extension('.html')
            else:
                self.change_extension(template_name[i:])
        self.template = generator.templates.get_template(template_name)
        return

    def render(self, **kwargs):
        return self.template.render(pagepress=self.generator, page=self)


class HTML(Templated):
    pass


class Blog(HTML):

    def __init__(self, **kwargs):
        self.title = kwargs.pop('title')
        self.published = kwargs.pop('published', None)
        if self.published is not None:
            (day, month, year) = [ int(i) for i in self.published.split('/') ]
            self.published = datetime.date(year, month, day)
        HTML.__init__(self, **kwargs)
        return