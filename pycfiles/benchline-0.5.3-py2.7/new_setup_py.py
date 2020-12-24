# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/new_setup_py.py
# Compiled at: 2014-03-25 13:51:30
"""
Script to create a new setup.py file.
"""
from string import Template
import os, six, benchline.args, benchline.user_input

def validate_args(parser, options, args):
    if len(args) < 1:
        parser.error('The first positional argument must be the project name.')


def get_setup_py(project_str, version_str='0.0.1'):
    template = Template('# !/usr/bin/env python\n\nfrom setuptools import setup, find_packages\n\n# we only use the subset of markdown that is also valid reStructuredText so\n# that our README.md works on both github (markdown) and pypi (reStructuredText)\nwith open("README.md") as rm_file:\n    long_description = rm_file.read()\n\nsetup(name=\'${project}\',\n      version=\'${version}\',\n      description="TODO",\n      long_description=long_description,\n      author=\'TODO\',\n      author_email=\'TODO\',\n      url=\'TODO\',\n      packages=find_packages(),\n      data_files=[(\'\', [\'README.md\', \'LICENSE\'],)],\n      test_suite="${project}.test",\n      license="MIT",\n      install_requires=[\'TODO\'],\n      zip_safe=False,\n      entry_points={\n          \'console_scripts\': [\n              \'TODO = ${project}.todo:main\']}\n)\n')
    return template.substitute(project=project_str, version=version_str)


def write_setup_py(contents):
    """
    :param contents: setup.py contents
    :return: void
    """
    open('setup.py', 'w').write(contents)


def main():
    parser = benchline.args.make_parser(usage='usage: %%prog [options] project_name\n%s' % __doc__)
    parser.add_option('--version', action='store_true', help='version to put in the file. default=0.0.1', default='0.0.1')
    options, args = benchline.args.triage(parser, validate_args=validate_args)
    setup_py_str = get_setup_py(args[0], options.version)
    if os.path.exists('setup.py'):
        yn = benchline.user_input.select('setup.py exists.  overwrite?', ('y', 'n'))
        if yn == 'y':
            write_setup_py(setup_py_str)
        else:
            six.print_('no changes made to setup.py.  existing...')
    else:
        write_setup_py(setup_py_str)


if __name__ == '__main__':
    main()