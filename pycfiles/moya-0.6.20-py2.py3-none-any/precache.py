# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/precache.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
from ...command import SubCommand
from ...wsgi import WSGIApplication
from ...compat import text_type
from ...context.expression import Expression

class PreCache(SubCommand):
    """Load resources in to cache in advance"""
    help = b'pre-cache resources to speed up initial requests '

    def add_arguments(self, parser):
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to projects settings file')
        return

    def run(self):
        console = self.console
        console.text(b'loading project', bold=True)
        application = WSGIApplication(self.location, self.get_settings(), disable_autoreload=True, master_settings=self.master_settings)
        archive = application.archive
        try:
            templates_fs = archive.get_filesystem(b'templates')
        except KeyError:
            self.error(b'templates filesystem not found')
        else:
            template_engine = archive.get_template_engine()
            paths = list(templates_fs.walk.files(filter=[b'*.html']))
            console.text(b'pre-caching templates', bold=True)
            failed_templates = []
            with console.progress(b'pre-caching templates', width=20) as (progress):
                progress.set_num_steps(len(paths))
                for path in paths:
                    progress.step(msg=path)
                    try:
                        template_engine.env.get_template(path)
                    except Exception as e:
                        failed_templates.append((path, text_type(e)))

        if archive.has_cache(b'parser'):
            parser_cache = archive.get_cache(b'parser')
            console.text(b'pre-caching expressions', bold=True)
            elements = []
            for lib in archive.libs.values():
                for _type, _elements in lib.elements_by_type.items():
                    elements.extend(_elements)

            with console.progress(b'caching expressions', width=20) as (progress):
                progress.set_num_steps(len(elements))
                for el in elements:
                    progress.step(msg=getattr(el, b'libid', b''))
                    el.compile_expressions()

            Expression.dump(parser_cache)
        else:
            console.error(b"no 'parser' cache available to store expressions")
        console.text(b'done', fg=b'green', bold=True)