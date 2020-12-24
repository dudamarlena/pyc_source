# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/local/local.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 658 bytes
"""
Command group for "local" suite for commands. It provides common CLI arguments, template parsing capabilities,
setting up stdin/stdout etc
"""
import click
import invoke.cli as invoke_cli
import start_api.cli as start_api_cli
import generate_event.cli as generate_event_cli
import start_lambda.cli as start_lambda_cli

@click.group()
def cli():
    """
    Run your Serverless application locally for quick development & testing
    """
    pass


cli.add_command(invoke_cli)
cli.add_command(start_api_cli)
cli.add_command(generate_event_cli)
cli.add_command(start_lambda_cli)