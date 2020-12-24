# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/plot/post_train.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1287 bytes
"""Deephyper analytics - post-training study

usage:

::

    $ deephyper-analytics post mybalsamdb/data/workflow_folder

"""
import os, argparse
from deephyper.core.plot.jn_loader import NbEdit
HERE = os.path.dirname(os.path.abspath(__file__))

def post_train_analytics(path_to_data_folder):
    editor = NbEdit((os.path.join(HERE, 'stub/post_train.ipynb')), path_to_save='dh-analytics-post.ipynb')
    venv_name = os.environ.get('VIRTUAL_ENV').split('/')[(-1)]
    editor.setkernel(venv_name)
    editor.edit(0, '{{path_to_data_folder}}', path_to_data_folder)
    editor.edit(1, '{{path_to_data_folder}}', f"'{path_to_data_folder}'")
    editor.write()
    editor.execute()


def add_subparser(subparsers):
    subparser_name = 'post'
    function_to_call = main
    parser_parse = subparsers.add_parser(subparser_name,
      help='Tool to generate analytics from a post-training experiment (jupyter notebook).')
    parser_parse.add_argument('path',
      type=str, help='Path to the workflow folder of the experiment. The workflow folder is located in "database/data/workflow_folders", it is the folder containing all task folders.')
    return (
     subparser_name, function_to_call)


def main(path, *args, **kwargs):
    post_train_analytics(path_to_data_folder=path)