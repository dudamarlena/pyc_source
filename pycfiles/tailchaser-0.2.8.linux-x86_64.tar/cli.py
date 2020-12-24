# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cabox/envs/tailchaser/lib/python2.7/site-packages/tailchaser/cli.py
# Compiled at: 2016-05-01 14:29:05
"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mtailchaser` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``tailchaser.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``tailchaser.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import logging, sys
from .tailer import Tailer
log = logging.getLogger(__name__)

def main(argv=sys.argv, consumer=None):
    """

    Args:
        argv (list): List of arguments
        consumer: an optional consumer

    Returns:
        int: A return code

    Does stuff.
    """
    Tailer.cli(argv, consumer=consumer)
    return 0