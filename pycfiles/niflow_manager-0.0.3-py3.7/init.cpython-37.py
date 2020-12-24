# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/niflow_manager/cli/init.py
# Compiled at: 2020-03-13 12:49:48
# Size of source mod 2**32: 3445 bytes
from pkg_resources import resource_filename as pkgr_fn
from pathlib import Path
import subprocess as sp, click
from util.git import git_variables
from util.fsutil import copytree, CopyPolicy

def normalize_path(name):
    path = Path(name).absolute()
    full_name = path.name
    if name != '.':
        if not full_name.startswith('niflow-'):
            full_name = 'niflow-' + full_name
            path = path.with_name(full_name)
    elif full_name.startswith('niflow-'):
        name_parts = full_name.split('-', 2)[1:]
    else:
        name_parts = full_name.split('-', 1)
    if len(name_parts) == 2:
        organization, workflow = name_parts
    else:
        organization = click.prompt('Organization name')
        workflow = click.prompt('Workflow name', default=(name_parts[0]))
        full_name = '-'.join(['niflow', organization, workflow])
        if name != '.':
            if click.confirm(f"Update path to {full_name}?", default=True):
                path = path.with_name(full_name)
        else:
            click.confirm(f'Niflow name "{full_name}" does not match directory "{path.name}". Proceed anyway?',
              abort=True)
    return (path, full_name, organization, workflow)


@click.argument('name', type=(click.Path()), default='.')
@click.option('--language', help='Language for new niflow')
@click.option('--bids',
  'bids_version',
  type=(click.Choice(['1.0'])),
  help='Niflow intended as a BIDS App')
def init(name, language, bids_version):
    path, full_name, organization, workflow = normalize_path(name)
    click.echo(f"Initializing workflow: {path.name} in {path.parent}")
    path.mkdir(parents=True, exist_ok=True)
    sp.run(['git', '-C', str(path), 'init'], check=True)
    try:
        git_vars = git_variables(path, 'user.name', 'user.email')
    except KeyError:
        username = click.prompt('Enter package author name')
        email = click.prompt('Enter package author email')
    else:
        username = git_vars['user.name']
        email = git_vars['user.email']
    mapping = {'USERNAME':username, 
     'USEREMAIL':email, 
     'ORGANIZATION':organization, 
     'WORKFLOW':workflow, 
     'FULLNAME':full_name}
    copytree((pkgr_fn('niflow_manager', 'data/templates/base')), path, mapping=mapping)
    if language is not None:
        language_dir = Path(pkgr_fn('niflow_manager', f"data/templates/{language}"))
        try:
            copytree(language_dir, path, mapping=mapping)
        except FileNotFoundError:
            raise ValueError(f"Unknown language: {language}")

    if bids_version is not None:
        if language is None:
            raise ValueError('BIDS App templates are language-specific; please specify --language')
        bids_app_dir = Path(pkgr_fn('niflow_manager', f"data/templates/{language}-bidsapp-{bids_version}"))
        try:
            copytree(bids_app_dir, path, policy=(CopyPolicy.OVERWRITE), mapping=mapping)
        except FileNotFoundError:
            raise ValueError(f"No BIDS App template for language: {language}")