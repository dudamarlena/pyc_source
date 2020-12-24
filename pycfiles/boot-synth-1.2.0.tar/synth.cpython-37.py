# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bennettdixon/Projects/synth/synth/synth.py
# Compiled at: 2019-06-19 10:10:59
# Size of source mod 2**32: 7332 bytes
""" CLI portion of synth, a docker bootstrapping tool
    commands:
        - create: creates a docker wireframe with your desired
            frontend, backend, and database
 """
import click, os
from synth.part_builder import PartBuilder
from synth.part_builder import PartBuilderException
import shutil, traceback

@click.group()
def cli():
    """ synth is a tool to create and deploy wireframed docker
    images and compose files easily. It was created by Bennett
    Dixon and Jack Gindi."""
    pass


@cli.command()
@click.option('--name', '-n',
  default='my_project',
  help='name of your project')
@click.option('--frontend', '-f',
  default=None,
  help='frontend to use')
@click.option('--backend', '-b',
  default=None,
  help='backend to use')
@click.option('--database', '-d',
  default=None,
  help='database to use')
@click.option('--cache', '-c',
  default=None,
  help='caching service to use')
@click.option('--pipeline', '-p',
  default=None,
  help='ci/cd pipeline to use')
def create(name, frontend, backend, database, cache, pipeline):
    """ creates a synth wireframe with your desired frontend,
    backend, database, caching service, and ci/cd pipeline
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    copy_dir = root_dir + '/projects_master/nginx_router/'
    if not frontend:
        if not backend:
            if not database:
                if not cache:
                    click.echo("all synth services can't be None")
                    exit(1)
    try:
        os.mkdir(name)
        shutil.copyfile(root_dir + '/projects_master/README.md', '{}/README.md'.format(name))
    except FileExistsError:
        click.echo('Directory {} already exists.'.format(name) + ' Please choose a different name.')
        exit(1)

    os.makedirs('{}/nginx_router/nginx_conf'.format(name))
    shutil.copyfile(copy_dir + 'nginx_conf/default.conf', '{}/nginx_router/nginx_conf/default.conf'.format(name))
    shutil.copyfile(copy_dir + 'nginx_conf/nginx.conf', '{}/nginx_router/nginx_conf/nginx.conf'.format(name))
    shutil.copyfile(copy_dir + 'Dockerfile.dev', '{}/nginx_router/Dockerfile.dev'.format(name))
    shutil.copyfile(copy_dir + 'Dockerfile', '{}/nginx_router/Dockerfile'.format(name))
    shutil.copyfile(root_dir + '/projects_master/docker-compose.yml', '{}/docker-compose.yml'.format(name))
    front_enabled = False
    if frontend is not None:
        front_enabled = True
    back_enabled = False
    if backend is not None:
        back_enabled = True
    pb = PartBuilder(parts_root=(root_dir + '/parts'), project_name=name,
      front_enabled=front_enabled,
      back_enabled=back_enabled)
    if database is not None:
        if database == 'mysql':
            click.echo('MySQL 5.7.6 has permissions issues, using 5.7 instead')
        try:
            os.makedirs('{}/database/data'.format(name))
            pb.add_part(database)
        except PartBuilderException as pbe:
            try:
                click.echo(pbe)
                cleanup(name)
            finally:
                pbe = None
                del pbe

    if cache is not None:
        try:
            pb.add_part(cache)
        except PartBuilderException as pbe:
            try:
                click.echo(pbe)
                cleanup(name)
            finally:
                pbe = None
                del pbe

    if frontend is not None:
        try:
            shutil.copytree(copy_dir + 'frontend/{}'.format(frontend), '{}/nginx_router/frontend/'.format(name))
            pb.add_part(frontend, database, cache)
        except (PartBuilderException, FileNotFoundError) as desc_e:
            try:
                if type(desc_e) is FileNotFoundError:
                    click.echo('FileNotFoundError: {}'.format(desc_e))
                if type(desc_e) is PartBuilderException:
                    click.echo('PartBuilderException: {}'.format(desc_e))
                cleanup(name)
            finally:
                desc_e = None
                del desc_e

        except Exception as e:
            try:
                traceback.print_tb(e.__traceback__)
                cleanup(name)
            finally:
                e = None
                del e

    if backend is not None:
        try:
            shutil.copytree(copy_dir + 'backend/{}'.format(backend), '{}/nginx_router/backend/'.format(name))
            pb.add_part(backend, database, cache)
        except (PartBuilderException, FileNotFoundError) as desc_e:
            try:
                if type(desc_e) is FileNotFoundError:
                    click.echo('FileNotFoundError: {}'.format(desc_e))
                if type(desc_e) is PartBuilderException:
                    click.echo('PartBuilderException: {}'.format(desc_e))
                cleanup(name)
            finally:
                desc_e = None
                del desc_e

        except Exception as e:
            try:
                traceback.print_tb(e.__traceback__)
                cleanup(name)
            finally:
                e = None
                del e

    if pipeline is not None:
        try:
            pb.build_pipeline(name, pipeline, {'frontend':frontend, 
             'backend':backend, 
             'database':database, 
             'cache':cache})
        except PartBuilderException as desc_e:
            try:
                click.echo('PartBuilderException: {}'.format(desc_e))
                cleanup(name)
            finally:
                desc_e = None
                del desc_e

    click.echo('\nsynthesized project directory {}'.format(name))
    click.echo('run:\n\n\tcd {}; docker-compose up\n'.format(name))
    click.echo('to start your development containers!\n')


def cleanup(name):
    """ cleanup operation to remove directory of a failed create """
    shutil.rmtree(name)
    exit(1)


if __name__ == '__main__':
    cli()