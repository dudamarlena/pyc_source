# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/commands/support_ids.py
# Compiled at: 2015-06-05 14:22:06
from __future__ import absolute_import
import click
from catalyze import cli, client, git, project, output
from catalyze.helpers import environments, services

@cli.command('support-ids', short_help='Prints out various helpful IDs.')
def support_ids():
    """Prints out various helpful IDs that can be pasted into support tickets."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    del settings['token']
    for pair in settings.items():
        output.write('%s: %s' % pair)