# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pymod_init/cli.py
# Compiled at: 2018-12-15 03:04:00
import click
from os import makedirs
from jinja2 import Environment, PackageLoader

class TemplateFile:

    def __init__(self, tname, output_path):
        self.tname = tname
        self.output_path = output_path


@click.command()
@click.argument('package-name')
@click.option('-a', '--author')
@click.option('-e', '--author-email')
@click.option('-m', '--maintainer-email')
@click.option('-d', '--description')
@click.option('-u', '--url')
def init(package_name, **kwargs):
    ctx = dict(package_name=package_name, **kwargs)
    env = Environment(loader=PackageLoader('pymod_init', 'templates'))
    _make_dirs(package_name)
    _make_files(env, ctx)


def _make_dirs(package_name):

    def _make_package_dir(package_name):
        try:
            makedirs('%s' % package_name)
        except Exception as e:
            pass

    def _make_test_dir():
        try:
            makedirs('tests')
        except Exception as e:
            pass

    def _make_doc_dir():
        try:
            makedirs('docs')
        except Exception as e:
            pass

    _make_package_dir(package_name)
    _make_test_dir()
    _make_doc_dir()


def _make_files(env, ctx):
    template_files = [
     TemplateFile('.gitignore.j2', '.gitignore'),
     TemplateFile('requirements.txt.j2', 'requirements.txt'),
     TemplateFile('MANIFEST.in.j2', 'MANIFEST.in'),
     TemplateFile('README.md.j2', 'README.md'),
     TemplateFile('setup.py.j2', 'setup.py')]
    for f in template_files:
        template = env.get_template(f.tname)
        template_str = template.render(**ctx)
        with open(f.output_path, 'w') as (fo):
            fo.write(template_str)


if __name__ == '__main__':
    init()