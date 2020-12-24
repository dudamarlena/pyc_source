# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/main.py
# Compiled at: 2020-04-01 02:43:02
# Size of source mod 2**32: 1469 bytes
import click, os, os.path, sh
HERE = os.path.abspath(os.path.dirname(__file__))

@click.group()
def cli():
    pass


def get_templates():
    dirs = os.scandir(os.path.join(HERE, 'templates'))
    templates = []
    for entry in dirs:
        if entry.is_dir():
            templates.append(entry.name)

    return templates


@cli.command()
@click.option('-t', '--template', default='simple', help='template')
@click.argument('project_name')
def create(template, project_name):
    templates = get_templates()
    if template not in templates:
        click.echo(('%s template not found' % template), err=True)
        return
    project_dir = './' + project_name
    sh.mkdir('-p', project_dir)
    sh.cp('-rf', os.path.join(HERE, f"templates/{template}/"), project_dir)
    for f in sh.find(project_dir, '-name', '*.py'):
        sh.sed('-i', '', '-e', 's/%s/%s/g' % ('proj', project_name), f.strip())

    for f in sh.find(project_dir, '-name', 'Dockerfile*'):
        sh.sed('-i', '', '-e', 's/%s/%s/g' % ('proj', project_name), f.strip())

    if template == 'simple':
        sh.sed('-i', '', '-e', 's/%s/%s/g' % ('proj', project_name), './%s/migrations/script.py.mako' % project_name)
    sh.mv(os.path.join(project_dir, 'proj'), os.path.join(project_dir, project_name))


@cli.command()
def list():
    templates = get_templates()
    for t in templates:
        print(t)


if __name__ == '__main__':
    cli()