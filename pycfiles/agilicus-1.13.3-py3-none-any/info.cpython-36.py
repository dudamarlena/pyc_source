# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/github/info.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 202 bytes
import json, click
from ..utils import gitrepo

@click.command()
def info():
    """Display information about repository
    """
    info = gitrepo()
    click.echo(json.dumps(info, indent=4))