# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/templ8/templ8/main.py
# Compiled at: 2020-03-03 15:12:46
# Size of source mod 2**32: 3201 bytes
import os, sys, shutil, ruamel.yaml
from inspect import cleandoc
from typing import List, Tuple, Any
from docopt import docopt
from pathlib import Path
from glob import iglob
from jinja2 import Environment, FileSystemLoader
from pyimport import path_guard
path_guard('..')
from exceptions import OutputDirInvalid, ConfigPathInvalid
from utils import pretty_log, get_child_files, stringer
from models import Context, Spec, Alias, Callback
CLI = cleandoc('\n    Usage:\n      templ8 <config_path> <output_dir> [NAMES ...] [--overwrite --dry-run]\n\n    Options:\n      --overwrite\n      --dry-run\n    ')
SPECS = [
 Spec('common', [
  Context('name'),
  Context('version', '0.1.0'),
  Context('description'),
  Context('author')]),
 Spec('package', [
  Context('author_email'),
  Context('author_github'),
  Context('github_url'),
  Context('twine_username')], {'src': Alias(Context('name'), lambda x: stringer(x))}),
 Spec('webapp', [
  Context('github_url')], {'server': Alias(Context('name'), lambda x: stringer(x) + '_server')}, [
  Callback(['ng', 'new', 'blah'])])]

def entrypoint() -> None:
    arguments = docopt(CLI)
    config_path, output_dir = arguments['<config_path>'], arguments['<output_dir>']
    options = {'overwrite':arguments['--overwrite'],  'dry-run':arguments['--dry-run'],  'specified_names':arguments['NAMES']}
    if not os.path.exists(config_path):
        raise ConfigPathInvalid(config_path)
    if os.path.isfile(output_dir):
        raise OutputDirInvalid(output_dir)
    with open(config_path, 'r') as (stream):
        config = ruamel.yaml.load(stream, Loader=(ruamel.yaml.Loader))
    main(config, output_dir, options)


def main(config: dict, output_dir: str, options: dict) -> None:
    specs = [spec for spec in SPECS if spec.check_condition(config)]
    context_dict = bundle_context(specs)
    for spec in specs:
        for template in load_templates(spec):
            generate_output(template)

        spec.run_callbacks()


def bundle_context(specs) -> dict:
    context_dict = dict([context.emit_from_config(config) for spec in specs for context in spec.context_set])
    context_dict.update({spec.root_name:True for spec in specs})
    context_dict.update({folder_name:spec.folder_aliases[folder_name].resolve(config) for spec in specs for folder_name in spec.folder_aliases})
    return context_dict


def generate_output(template) -> None:
    Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)
    if os.path.exists(output_path):
        if not options['overwrite']:
            pretty_log(output_path + ' exists; skipping')
    else:
        if options['dry-run']:
            pretty_log('Would write: ' + output_path)
        else:
            with open(output_path, 'w') as (f):
                f.write(template.render(context_dict))
                pretty_log('Generated: ' + output_path)


if __name__ == '__main__':
    entrypoint()