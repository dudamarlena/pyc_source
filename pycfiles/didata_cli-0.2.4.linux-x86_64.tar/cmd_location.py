# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jdunham/projects/didata_cli_jdunham/didata_cli/venv/lib/python2.7/site-packages/didata_cli/commands/cmd_location.py
# Compiled at: 2016-02-16 19:29:15
import click
from didata_cli.cli import pass_client
from libcloud.common.dimensiondata import DimensionDataAPIException
from didata_cli.utils import handle_dd_api_exception

@click.group()
@pass_client
def cli(client):
    pass


@cli.command()
@click.option('--datacenterId', type=click.UNPROCESSED, help='Filter by datacenter Id')
@pass_client
def list(client, datacenterid):
    try:
        locations = client.node.list_locations(ex_id=datacenterid)
        for location in locations:
            click.secho(('{0}').format(location.name), bold=True)
            click.secho(('ID: {0}').format(location.id))
            click.secho(('Description: {0}').format(location.country))
            click.secho('')

    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)