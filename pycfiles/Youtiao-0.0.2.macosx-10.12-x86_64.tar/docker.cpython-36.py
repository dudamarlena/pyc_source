# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/quhujun/.pyenv/versions/3.6.0/Python.framework/Versions/3.6/lib/python3.6/site-packages/youtiao/commands/docker.py
# Compiled at: 2018-05-08 06:33:15
# Size of source mod 2**32: 1535 bytes
import click, docker

@click.command()
@click.option('--project-name', type=str, required=True, help='project name')
@click.option('--commit-ref-name', type=str, required=True, help='name of git branch or tag')
@click.option('--commit-sha', type=str, required=True, help='git commit hash')
@click.option('--workdir', type=click.Path(exists=True, file_okay=False, resolve_path=True), required=True)
@click.option('--registry-url', type=str, help='Docker registry URL', default=None)
def build(project_name, commit_ref_name, commit_sha, workdir, registry_url):
    """Build docker image"""
    repo_name = '{}/{}'.format(project_name.lower(), commit_ref_name)
    if registry_url is not None:
        repo_name = '{}/{}'.format(registry_url, repo_name)
    build_full_tag = '{}:{}'.format(repo_name, commit_sha)
    docker_cli = docker.from_env()
    click.secho('Building image {}'.format(build_full_tag))
    new_image, _ = docker_cli.images.build(path=workdir, tag=build_full_tag, rm=True)
    new_image.tag(repo_name, tag='latest')
    click.secho('Image built {}'.format(new_image.id))
    image_list = docker_cli.images.list(name=repo_name,
      filters={'before': build_full_tag})
    for img in image_list:
        click.secho('Delete old image of {}'.format(img.id))
        docker_cli.images.remove(image=(img.short_id), force=True)

    return new_image.short_id