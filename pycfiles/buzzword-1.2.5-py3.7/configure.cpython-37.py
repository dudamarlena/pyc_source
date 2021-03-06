# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzzword/parts/configure.py
# Compiled at: 2019-08-23 08:59:14
# Size of source mod 2**32: 4603 bytes
"""
buzzword: command-line and .env processing
"""
import argparse, os
from dotenv import load_dotenv

def _from_cmdline():
    """
    Command line argument parsing
    """
    parser = argparse.ArgumentParser(description='Run the buzzword app for a given corpus.')
    parser.add_argument('-nl',
      '--load',
      default=True,
      action='store_true',
      required=False,
      help='Load corpus into memory. Longer startup, faster search.')
    parser.add_argument('-r',
      '--root',
      default='.',
      required=False,
      type=str,
      nargs='?',
      help='Space for the tool to store CSVs, uploaded data, etc.')
    parser.add_argument('-t',
      '--title', nargs='?', type=str, required=False, help='Title for app')
    parser.add_argument('-d',
      '--drop-columns',
      nargs='?',
      type=str,
      required=False,
      help='Dataset columns to remove before loading (comma-separated)')
    parser.add_argument('-m',
      '--max-dataset-rows',
      nargs='?',
      type=int,
      required=False,
      help='Truncate datasets at this many rows')
    parser.add_argument('-s',
      '--table-size',
      nargs='?',
      type=str,
      required=False,
      default='2000,200',
      help="Max table dimensions as str ('nrows,ncolumns')")
    parser.add_argument('-p',
      '--page-size',
      nargs='?',
      type=int,
      default=25,
      required=False,
      help='Rows to display per page')
    parser.add_argument('-debug',
      '--debug',
      default=False,
      action='store_true',
      required=False,
      help='Debug mode')
    parser.add_argument('-g',
      '--add-governor',
      default=False,
      action='store_true',
      required=False,
      help='Load governor attributes into dataset. Slow to load and uses more memory, but allows more kinds of searching/showing')
    parser.add_argument('-ne',
      '--no-env',
      default=False,
      action='store_true',
      required=False,
      help='Ignore config taken from .env file.')
    parser.add_argument('-c',
      '--corpora-file',
      default='corpora.json',
      type=str,
      nargs='?',
      help='Path to corpora.json')
    parser.add_argument('-e',
      '--env',
      nargs='?',
      type=str,
      required=False,
      default='.env',
      help='Path to .env file')
    kwargs = vars(parser.parse_args())
    if kwargs['drop_columns'] is not None:
        kwargs['drop_columns'] = kwargs['drop_columns'].split(',')
    if kwargs['table_size'] is not None:
        kwargs['table_size'] = [int(i) for i in kwargs['table_size'].split(',')][:2]
    return kwargs


def _configure_buzzword(name):
    """
    Configure application. First, look at command line args.
    If the user wants to use dotenv (--env flag), load from that.
    If not from main, use dotenv only.
    """
    cmd_config = _from_cmdline()
    env_path = cmd_config['env']
    if not os.path.isfile(env_path) or cmd_config['no_env']:
        return cmd_config
    env_conf = _from_env(env_path)
    return env_conf


def _from_env(env_path):
    """
    Read .env. Should return same as command line, except --env argument
    """
    trues = {
     '1', 'true', 'True', 'Y', 'y', 'yes', True}
    load_dotenv(dotenv_path=env_path)
    drop_columns = os.getenv('BUZZWORD_DROP_COLUMNS')
    if drop_columns:
        drop_columns = drop_columns.split(',')
    table_size = os.getenv('BUZZWORD_TABLE_SIZE')
    if table_size:
        table_size = [int(i) for i in table_size.split(',')]
    max_dataset_rows = os.getenv('BUZZWORD_MAX_DATASET_ROWS')
    if max_dataset_rows:
        if max_dataset_rows.strip():
            max_dataset_rows = int(max_dataset_rows.strip())
    return dict(corpora_file=(os.getenv('BUZZWORD_CORPORA_FILE', 'corpora.json')),
      root=(os.getenv('BUZZWORD_ROOT', '.')),
      debug=(os.getenv('BUZZWORD_DEBUG', True) in trues),
      load=(os.getenv('BUZZWORD_LOAD', True) in trues),
      add_governor=(os.getenv('BUZZWORD_ADD_GOVERNOR', False) in trues),
      title=(os.getenv('BUZZWORD_TITLE')),
      page_size=(int(os.getenv('BUZZWORD_PAGE_SIZE', 25))),
      max_dataset_rows=max_dataset_rows,
      drop_columns=drop_columns,
      table_size=table_size)