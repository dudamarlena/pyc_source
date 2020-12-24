# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/axon_conabio/management/commands.py
# Compiled at: 2018-12-10 18:39:29
import os, click
from .train import train as tr
from .evaluate import evaluate as ev
from .make_project import make_project as mp
from .config import get_config
from .utils import get_base_project, get_model_path, get_all_objects

@click.group()
def main():
    pass


@main.command()
@click.argument('name', required=False)
@click.option('--path')
@click.option('--retrain', is_flag=True)
def train(name, path, retrain):
    if retrain:
        msg = 'Retrain option is set. This will erase all summaries'
        msg += ' and checkpoints currently available for this model.'
        msg += ' Do you wish to continue?'
        click.confirm(msg, abort=True)
    if name is not None:
        project = get_base_project(os.path.abspath('.') + '/')
    elif path is not None:
        project = get_base_project(path)
    else:
        msg = 'Name of model or path to model must be supplied'
        raise click.UsageError(msg)
    config_path = None
    if project is not None:
        config_path = os.path.join(project, '.project', 'axon_config.yaml')
    config = get_config(path=config_path)
    if name is not None:
        path = get_model_path(name, project, config)
    if not os.path.exists(path):
        msg = 'No model with name {name} was found. Available models: {list}'
        model_list = (', ').join(get_all_objects('model'))
        msg = msg.format(name=name, list=model_list)
        raise click.UsageError(msg)
    tr(path, config, project, retrain=retrain)
    return


@main.command()
@click.argument('type', type=click.Choice([
 'architecture',
 'loss',
 'metric',
 'model',
 'product',
 'dataset']))
@click.option('--path')
def list(type, path):
    if path is None:
        path = '.'
    project = get_base_project(path)
    config_path = os.path.join(project, '.project', 'axon_config.yaml')
    config = get_config(path=config_path)
    result = get_all_objects(type, project=project, config=config)
    msg = ('Available {}:').format(type)
    for n, name in enumerate(result):
        msg += ('\n\t{}. {}').format(n + 1, name)

    click.echo(msg)
    return


@main.command()
@click.argument('name', required=False)
@click.option('--path')
@click.option('--ckpt', type=int)
def evaluate(name, path, ckpt):
    if name is not None:
        project = get_base_project(os.path.abspath('.') + '/')
    elif path is not None:
        project = get_base_project(path)
    else:
        msg = 'Name of model or path to model must be supplied'
        raise click.UsageError(msg)
    if project is None:
        msg = 'You (or the target directory) are not inside an'
        msg += ' axon project!'
        raise click.UsageError(msg)
    config_path = os.path.join(project, '.project', 'axon_config.yaml')
    config = get_config(path=config_path)
    if name is not None:
        path = get_model_path(name, project, config)
    if not os.path.exists(path):
        msg = 'No model with name {name} was found. Available models: {list}'
        model_list = (', ').join(get_all_objects('model', project=project, config=config))
        msg = msg.format(name=name, list=model_list)
        raise click.UsageError(msg)
    ev(path, config, project, ckpt)
    return


@main.command()
@click.argument('path', type=click.Path(exists=False))
@click.option('--config', type=click.Path(exists=True))
def make_project(path, config):
    config = get_config(path=config)
    mp(path, config)