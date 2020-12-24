# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/cli.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 1689 bytes
import asyncio, json, click, yaml as _yaml
from . import __version__
from .client import Kong, KongError
from .utils import local_ip

@click.command()
@click.option('--version', is_flag=True, default=False, help='Display version and exit')
@click.option('--ip', is_flag=True, default=False, help='Show local IP address')
@click.option('--key-auth',
  help='Create or display an authentication key for a consumer')
@click.option('--yaml', type=(click.File('r')), help='Yaml configuration to upload')
@click.pass_context
def kong(ctx, version, ip, key_auth, yaml):
    if version:
        click.echo(__version__)
    else:
        if ip:
            click.echo(local_ip())
        else:
            if key_auth:
                return _run(_auth_key(ctx, key_auth))
            if yaml:
                return _run(_yml(ctx, yaml))
            click.echo(ctx.get_help())


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


async def _yml(ctx, yaml):
    async with Kong() as cli:
        try:
            result = await cli.apply_json(_yaml.load(yaml, Loader=(_yaml.FullLoader)))
            click.echo(json.dumps(result, indent=4))
        except KongError as exc:
            try:
                raise click.ClickException(str(exc))
            finally:
                exc = None
                del exc


async def _auth_key(ctx, consumer):
    async with Kong() as cli:
        try:
            c = await cli.consumers.get(consumer)
            keys = await c.keyauths.get_list()
            if keys:
                key = keys[0]
            else:
                key = await c.keyauths.create()
            click.echo(json.dumps((key.data), indent=4))
        except KongError as exc:
            try:
                raise click.ClickException(str(exc))
            finally:
                exc = None
                del exc


def main():
    kong()