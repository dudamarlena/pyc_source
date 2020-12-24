# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dame/__main__.py
# Compiled at: 2020-05-04 14:48:31
# Size of source mod 2**32: 5594 bytes
"""
dame.

:license: Apache 2.0
"""
from pathlib import Path
import click, semver
from modelcatalog import ApiException, Configuration
import dame
from dame import _utils
from dame.cli_methods import verify_input_parameters, run_method_setup, show_model_configuration_details, print_table_list
from dame.configuration import configure_credentials, DEFAULT_PROFILE
from dame.modelcatalogapi import get_setup, get_model_configuration, list_model_configuration, list_setup
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

@click.group()
@click.option('--verbose', '-v', default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    lv = '.'.join(_utils.get_latest_version().split('.')[:3])
    cv = '.'.join(dame.__version__.split('.')[:3])
    if semver.compare(lv, cv) > 0:
        click.secho(f"WARNING: You are using dame-cli version {dame.__version__}, however version {lv} is available.\nYou should consider upgrading via the 'pip install --upgrade dame-cli' command.",
          fg='yellow')


@cli.command(help='Configure credentials')
@click.option('--profile',
  '-p',
  envvar='MINT_PROFILE',
  type=str,
  default='default',
  metavar='<profile-name>')
@click.option('--server', prompt='Model Catalog API', help='The Model Catalog API',
  required=True,
  default=(Configuration().host),
  show_default=True)
@click.option('--username', prompt='Username', help='Your email.',
  required=True,
  default='mint@isi.edu',
  show_default=True)
def configure(server, username, profile='default'):
    try:
        configure_credentials(server, username, profile)
    except Exception:
        click.secho('Failed', fg='red')

    click.secho('Success', fg='green')


@cli.command(help='Show dame-cli version.')
def version():
    click.echo(f"DAME: v{dame.__version__}")


@cli.command(help='Open the Model Catalog in your browser')
def browse():
    click.launch('https://models.mint.isi.edu')


@cli.command(help='Run a model configuration or model configuration setup')
@click.argument('name',
  type=(click.STRING))
@click.option('--profile',
  '-p',
  envvar='MINT_PROFILE',
  type=str,
  default='default',
  metavar='<profile-name>')
@click.option('--data',
  '-d',
  type=click.Path(exists=False, dir_okay=True, resolve_path=True),
  default='data')
@click.option('--interactive/--non-interactive', default=True)
def run(name, interactive, profile, data):
    if not Path(data).exists():
        data = None
    else:
        data = Path(data)
    try:
        config = get_model_configuration(name, profile=profile)
    except ApiException as e:
        try:
            click.secho('{}'.format(e.reason))
            exit(0)
        finally:
            e = None
            del e

    click.clear()
    if 'ModelConfigurationSetup' in config.type:
        resource = get_setup(name, profile=profile)
    else:
        if 'ModelConfiguration' in config.type:
            resource = get_model_configuration(name, profile=profile)
        else:
            try:
                show_model_configuration_details(resource)
            except AttributeError as e:
                try:
                    click.secho(('Unable to run it: {}'.format(str(e))), fg='red')
                    exit(1)
                finally:
                    e = None
                    del e

        try:
            verify_input_parameters(resource, interactive, data)
        except ValueError as e:
            try:
                click.secho('Unable to run. Please use interactive mode', fg='yellow')
                exit(1)
            finally:
                e = None
                del e

        run_method_setup(resource, interactive, data)


@cli.group()
def model_configuration():
    """Manages model configurations"""
    pass


@model_configuration.command(name='list', help='List configurations')
@click.option('--profile',
  '-p',
  envvar='MINT_PROFILE',
  type=str,
  default=DEFAULT_PROFILE,
  metavar='<profile-name>')
def model_configuration_list(profile):
    items = list_model_configuration(label=None, profile=profile)
    print_table_list(items)


@click.argument('name',
  type=(click.STRING))
@model_configuration.command(name='show', help='Show model configuration')
@click.option('--profile',
  '-p',
  envvar='MINT_PROFILE',
  type=str,
  default=DEFAULT_PROFILE,
  metavar='<profile-name>')
def model_configuration_show(name, profile):
    try:
        _setup = get_model_configuration(name, profile=profile)
    except ApiException as e:
        try:
            click.secho('{}'.format(e.reason))
            exit(1)
        finally:
            e = None
            del e

    try:
        show_model_configuration_details(_setup)
    except AttributeError as e:
        try:
            click.secho(('This setup is not executable.\n'.format(e)), fg='red')
        finally:
            e = None
            del e


@cli.group()
def setup():
    """Manages model configuration setup"""
    pass


@setup.command(name='list', help='List model configuration setups')
@click.option('--profile',
  '-p',
  envvar='MINT_PROFILE',
  type=str,
  default=DEFAULT_PROFILE,
  metavar='<profile-name>')
def setup_list(profile):
    items = list_setup(label=None, profile=profile)
    print_table_list(items)


@click.argument('name',
  type=(click.STRING))
@setup.command(name='show', help='Show model configuration setups')
@click.option('--profile',
  '-p',
  envvar='MINT_PROFILE',
  type=str,
  default=DEFAULT_PROFILE,
  metavar='<profile-name>')
def setup_show(name, profile):
    try:
        _setup = get_setup(name, profile=profile)
    except ApiException as e:
        try:
            click.secho('{}'.format(e.reason))
            exit(1)
        finally:
            e = None
            del e

    try:
        show_model_configuration_details(_setup)
    except AttributeError as e:
        try:
            click.secho(('This setup is not executable.\n'.format(e)), fg='red')
        finally:
            e = None
            del e