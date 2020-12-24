# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/cli/nas_init.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 3174 bytes
import argparse, os, sys
PKG_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def add_subparser(subparsers):
    subparser_name = 'nas-init'
    function_to_call = main
    subparser = subparsers.add_parser(subparser_name,
      help='Tool to init a neural architecture search package or a neural architecture search problem folder.')
    subparser.add_argument('--new-pckg', type=str, help='Name of the new neural architecture package to create.')
    subparser.add_argument('--new-pb', type=str, help='Name of the new neural architecture search folder to create.')
    subparser.set_defaults(func=function_to_call)


def main(new_pckg, new_pb, *args, **kwargs):
    pb_files = [
     '__init__.py',
     'problem.py',
     'load_data.py',
     'search_space.py']
    if new_pckg is not None:
        path = new_pckg
        try:
            os.mkdir(path)
        except OSError:
            print('Creation of the directory %s failed' % path)
        else:
            print('Successfully created the directory %s ' % path)
            with open(os.path.join(path, 'setup.py'), 'w') as (fp):
                fp.write(f"from setuptools import setup\n\nsetup(\n    name='{new_pckg}',\n    packages=['{new_pckg}'],\n    install_requires=[]\n)")
        path = os.path.join(path, new_pckg)
        try:
            os.mkdir(path)
        except OSError:
            print('Creation of the directory %s failed' % path)
        else:
            print('Successfully created the directory %s ' % path)
            with open(os.path.join(path, '__init__.py'), 'w') as (fp):
                pass
            path = '/'.join(path.split('/')[:-1])
            os.chdir(path)
            cmd = 'pip install -e .'
            os.system(cmd)
        if new_pb is not None:
            os.chdir(new_pckg)
            create_problem_folder(new_pb, pb_files)
    elif new_pb is not None:
        create_problem_folder(new_pb, pb_files)


def create_problem_folder(new_pb, pb_files):
    path = os.path.join(os.getcwd(), new_pb)
    pckg_name = path.split('/')[(-2)]
    try:
        os.mkdir(path)
    except OSError:
        print('Creation of the directory %s failed' % path)
    else:
        print('Successfully created the directory %s ' % path)
        for fname in pb_files:
            file_path = os.path.join(path, fname)
            with open(file_path, 'w') as (fnew):
                print(f"create file: {file_path}")
                tmpl_name = fname.split('.')[0] + '.tmpl'
                if fname == 'problem.py':
                    fnew.write(render(tmpl_name, pckg=pckg_name,
                      pb_folder=new_pb))
                else:
                    fnew.write(render(tmpl_name))


from jinja2 import Environment, PackageLoader

def render(file, **kwargs):
    env = Environment(loader=(PackageLoader('deephyper', 'core/cli/templates')))
    template = env.get_template(file)
    rendering = (template.render)(**kwargs)
    return rendering