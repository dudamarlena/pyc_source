# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cmusselle/Mango/Workspace/masonry/package/src/masonry/cli.py
# Compiled at: 2017-10-24 10:06:44
# Size of source mod 2**32: 3562 bytes
"""Masonry

A tool for working with composable project templates. 

Commands:
    init  - initialise a new project 
    add   - add a template to an existing project
    check - check a particular project or template layer renders correctly

Usage:
    mason init [-v] [-o DIR] [PROJECT]
    mason add [-v] [-o DIR] [TEMPLATE ...]
    mason check [-v] [PROJECT]
    mason (-h | --help)
    mason --version

Arguments:
  PROJECT      URL/Filepath to directory for project type. Should contain
               subdiectories for all templates and a metadata.json file.
               Can also specify a template subdirectory, and if so, this
               is used as the template instead of the default for the project.

  TEMPLATE     Name of one or more templates to add to an existing project.

Options:
  -o DIR --output=DIR  Project directory to create/add to [default: .]
  -h --help            Show this screen.
  --version            Show version.
  -v                   Increase verbosity of output
"""
import os
from sys import exit
from pathlib import Path
from docopt import docopt
from . import __version__
try:
    from schema import Schema, And, Or, Use, SchemaError
except ImportError:
    exit('This example requires that `schema` data-validation library is installed: \n    pip install schema\nhttps://github.com/halst/schema')

def parse_args(argv=None):
    args = docopt(__doc__, version=__version__, argv=argv)
    return args


def validate_args(args):

    def template_path_exists(template):
        if template:
            template_path = os.path.join(args['PROJECT'], template)
            return os.path.exists(template_path)
        else:
            return True

    def mason_file_exists(output):
        mason_path = os.path.join(output, '.mason')
        return os.path.exists(mason_path)

    if args['init']:
        schema = Schema({str: object})
    else:
        if args['add']:
            schema = Schema({str: object})
        else:
            if args['check']:
                schema = Schema({str: object})
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)


def parse_and_validate_args(argv):
    parsed_args = parse_args(argv)
    validate_args(parsed_args)
    return parsed_args


def parse_project_argument(arg):
    template = None
    project_argument = Path(arg).resolve()
    project_metadata = project_argument / 'metadata.json'
    if project_metadata.exists():
        project_dir = arg
    else:
        if (project_argument.parent / 'metadata.json').exists():
            project_dir = project_argument.parent.as_posix()
            template = project_argument.name
    return (
     project_dir, template)