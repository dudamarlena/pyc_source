# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/hydro_cli.py
# Compiled at: 2016-03-22 15:09:41
import argparse, sys, os
from django.template import Template, Context
from django.conf import settings as django_settings
import django
__author__ = 'moshebasanchig'

def _create_file_from_template(template_file_name, destination_file_name, topology_name):
    with open(template_file_name, 'r') as (template_file):
        template_str = template_file.read()
    template = Template(template_str)
    context = Context({'topology_name': topology_name})
    file_contents = template.render(context)
    with open(destination_file_name, 'w') as (destination_file):
        destination_file.write(file_contents)


def scaffold(args):
    dir_name = args.dir_name
    topology_name = args.topology_name
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        if not django_settings.configured:
            django_settings.configure()
            django.setup()
    if os.path.exists(dir_name):
        print 'directory already exists. skipping.'
        sys.exit(1)
    os.makedirs(dir_name)
    open('%s/__init__.py' % dir_name, 'w').close()
    template_dir = '%s/templates' % os.path.dirname(os.path.realpath(__file__))
    _create_file_from_template('%s/conf.template' % template_dir, '%s/conf.py' % dir_name, topology_name)
    _create_file_from_template('%s/optimizer.template' % template_dir, '%s/optimizer.py' % dir_name, topology_name)
    _create_file_from_template('%s/topology1.template' % template_dir, '%s/topology1.py' % dir_name, topology_name)
    _create_file_from_template('%s/sample.template' % template_dir, '%s/sample.txt' % dir_name, topology_name)
    usage = "\n    Scaffolding completed successfully. Here's how to use your new topology:\n    ```\n    from hydro.hydro_cluster import LocalHydro\n    local_hydro = LocalHydro()\n    from {dir_name}.topology1 import {topology_name}Topology\n    local_hydro.register('{topology_name}', {topology_name}Topology())\n    result = local_hydro.submit('{topology_name}', {{}})\n    print result.stream\n    ```\n    "
    print usage.format(dir_name=dir_name, topology_name=topology_name)


def listen(args):
    raise BaseException('listen not implemented')


def submit(args):
    raise BaseException('submit not implemented')


def main():
    parser = argparse.ArgumentParser(description='Hydro management tool')
    subparsers = parser.add_subparsers()
    scaffold_parser = subparsers.add_parser('scaffold', help='scaffold a new topology')
    scaffold_parser.add_argument('dir_name', help='directory name for the topology')
    scaffold_parser.add_argument('topology_name', help='topology name, without the Topology suffix')
    scaffold_parser.set_defaults(func=scaffold)
    listen_parser = subparsers.add_parser('listen', help='start hydro in server mode')
    listen_parser.set_defaults(func=listen)
    submit_parser = subparsers.add_parser('submit', help='submit a topology to a remote server')
    submit_parser.add_argument('dir_name')
    submit_parser.set_defaults(func=submit)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()