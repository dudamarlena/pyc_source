# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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