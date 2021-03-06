# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flask_scaffold.py
# Compiled at: 2018-05-13 14:26:49
# Size of source mod 2**32: 4447 bytes
import os, base64
from os import getcwd, mkdir, path
import sys, click, yaml
from jinja2 import Template
import chalk
TREE_DESCRIPTION_FILE = 'structure.yml'
APP_NAME = None
BASE_PATH = getcwd()
TEMPLATE_PATH = path.join(BASE_PATH, 'stubs', '{}.jinja2')

def _make_dir(name):
    mkdir(name)


def _make_file(name):
    open(name, 'a').close()


def _build_path(base, name, *args):
    global APP_NAME
    return (path.join)(base, name, *args).replace('(APP_NAME)', APP_NAME)


def _parse_tree(tree, base=BASE_PATH):
    tree_type = type(tree)
    if tree_type is dict:
        dir_, tree_ = tree.popitem()
        _make_dir(_build_path(base, dir_))
        _parse_tree(tree_, base=(_build_path(base, dir_)))
    else:
        if tree_type is list:
            for i in tree:
                _parse_tree(i, base=base)

        else:
            _make_file(_build_path(base, tree))


def _scaffold(template, target_path, **kwargs):
    with open(TEMPLATE_PATH.format(template), 'r') as (f):
        template = Template(f.read())
    (template.stream)(**kwargs).dump(target_path)


def _chalk(text, color, app_name=True, **kwargs):
    color = getattr(chalk, color)
    text = color(text, **kwargs)
    if app_name:
        text = color(('[%s] ' % APP_NAME), bold=True) + text
    click.echo(text)


def generate_requirements(app_path):
    requirements = 'click==6.7\n                    Flask==0.12.2\n                    flask-mongoengine==0.9.5\n                    Flask-WTF==0.14.2\n                    itsdangerous==0.24\n                    Jinja2==2.10\n                    MarkupSafe==1.0\n                    mongoengine==0.15.0\n                    pymongo==3.6.1\n                    python-dateutil==2.7.0\n                    six==1.11.0\n                    Werkzeug==0.14.1\n                    WTForms==2.1'.replace(' ', '')
    with open(path.join(app_path, 'requirements.txt'), 'a') as (f):
        f.write(requirements)


def generate_run(app_path):
    path_ = path.join(app_path, 'run.py')
    _scaffold('run.py', path_, app_name=APP_NAME)


def generate_init(app_path):
    path_ = path.join(app_path, APP_NAME, '__init__.py')
    _scaffold('__init__.py', path_)


def generate_models(app_path):
    path_ = path.join(app_path, APP_NAME, 'models.py')
    _scaffold('models.py', path_)


def generate_config(app_path):
    path_ = path.join(app_path, 'config.py')
    secret_key = base64.b64encode(os.urandom(24))
    _scaffold('config.py', path_, secret_key=secret_key, app_name=APP_NAME)
    path_ = path.join(app_path, 'instance', 'config.py')
    _scaffold('instance.config.py', path_)


def generate_api_views(app_path):
    path_ = path.join(app_path, APP_NAME, 'api', 'views.py')
    _scaffold('api.views.py', path_)


def generate_web_views(app_path):
    path_ = path.join(app_path, APP_NAME, 'web', 'views.py')
    _scaffold('web.views.py', path_)


def generate_web_templates(app_path):
    templates_path = path.join(app_path, APP_NAME, 'web', 'templates')
    _scaffold('base.html', (path.join(templates_path, 'base.html')), app_name=APP_NAME)
    _scaffold('index.html', (path.join(templates_path, 'index.html')), app_name=APP_NAME)


@click.group()
def main():
    pass


@main.command('new')
@click.argument('app_name')
def new(app_name):
    global APP_NAME
    APP_NAME = app_name
    _chalk('Generating directory structure...', 'white')
    tree = yaml.load(open(TREE_DESCRIPTION_FILE))
    try:
        _parse_tree(tree)
    except:
        _chalk('Error while generating directory structure. Aborting...', 'red')
        exit(1)

    _chalk('Generating file contents...', 'white')
    app_path = _build_path(BASE_PATH, app_name)
    generate_requirements(app_path)
    generate_run(app_path)
    generate_init(app_path)
    generate_models(app_path)
    generate_config(app_path)
    generate_api_views(app_path)
    generate_web_views(app_path)
    generate_web_templates(app_path)
    _chalk('Process completed!', 'green')
    _chalk("Post-install steps: (Don't forget to create a virtual environment!)", 'magenta', app_name=False, bold=True)
    _chalk(('\t$ cd {}'.format(app_name)), 'white', app_name=False, bold=True)
    _chalk('\t$ pip install -r requirements.txt', 'white', app_name=False, bold=True)


if __name__ == '__main__':
    main()