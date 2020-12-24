# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/alphahome/cmdline.py
# Compiled at: 2017-08-05 23:18:06
import sys, argparse, os, git
from cmd.command import Application

def _generate_templates(name):
    os.mkdir(name)
    os.chdir(name)
    pkg_pth = os.path.split(os.path.realpath(__file__))[0]
    app_pth = os.path.join(pkg_pth, 'templates', 'app')
    models = os.path.join(app_pth, 'models.tmpl')
    views = os.path.join(app_pth, 'views.tmpl')
    including = os.path.join(app_pth, 'including.tmpl')
    with open('models.py', 'wb') as (f):
        f.write(open(models, 'rb').read())
    with open('views.py', 'wb') as (f):
        f.write(open(views, 'rb').read())
    with open('INCLUDING', 'wb') as (f):
        f.write(open(including, 'rb').read())
    with open('__init__.py', 'wb') as (f):
        f.write('')


def execute(argv=None, settings=None):
    if argv is None:
        argv = sys.argv
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser()
    parser.add_argument('operator', choices=('bind', 'generate', 'upload'))
    parser.add_argument('--name', '-n', help='name for your app')
    args = parser.parse_args()
    operator = args.operator
    if operator == 'bind':
        app = Application()
        app.bind()
    elif operator == 'generate':
        name = args.name
        if name is None:
            print '需要指定名称 [--name or -n]'
            return
        _generate_templates(name)
    elif operator == 'upload':
        app = Application()
        app.upload()
    return


if __name__ == '__main__':
    execute()