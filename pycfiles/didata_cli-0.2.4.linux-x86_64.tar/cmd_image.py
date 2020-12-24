# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jdunham/projects/didata_cli_jdunham/didata_cli/venv/lib/python2.7/site-packages/didata_cli/commands/cmd_image.py
# Compiled at: 2016-02-18 20:04:23
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
def list_base_images(client, datacenterid):
    try:
        images = client.node.list_images(location=datacenterid)
        for image in images:
            click.secho(('{}').format(image.extra['OS_displayName']), bold=True)
            click.secho(('ID: {0}').format(image.id))
            click.secho(('Description: {0}').format(image.extra['description']))
            click.secho(('CPU Count: {0} Cores per Socket: {1} Speed: {2}').format(image.extra['cpu'].cpu_count, image.extra['cpu'].cores_per_socket, image.extra['cpu'].performance))
            click.secho(('Memory: {0}GB').format(image.extra['memoryGb']))
            click.secho(('Location: {0}').format(image.extra['location'].id))
            click.secho('')

    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)


@cli.command()
@click.option('--datacenterId', type=click.UNPROCESSED, help='Filter by datacenter Id')
@pass_client
def list_customer_images(client, datacenterid):
    try:
        images = client.node.ex_list_customer_images(location=datacenterid)
        for image in images:
            click.secho(('{}').format(image.extra['OS_displayName']), bold=True)
            click.secho(('ID: {0}').format(image.id))
            click.secho(('Description: {0}').format(image.extra['description']))
            click.secho(('CPU Count: {0} Cores per Socket: {1} Speed: {2}').format(image.extra['cpu'].cpu_count, image.extra['cpu'].cores_per_socket, image.extra['cpu'].performance))
            click.secho(('Memory: {0}GB').format(image.extra['memoryGb']))
            click.secho(('Location: {0}').format(image.extra['location'].id))
            click.secho('')

    except DimensionDataAPIException as e:
        handle_dd_api_exception(e)