"""
Plugin used to setup the local environment:

- Add/remove gamma sanctioned PyPI repos in pip.conf
- ...

For example:

`gamma setup pip auto`

will setup the all repositories marked with `auto_install: True` in the default
repositories.yaml file into the user's `pip.conf`

`gamm setup pip add-repo <repo-name>`

will install the specified repository.

You can extend this command group to setup other resources via CLI plugins.
"""

import webbrowser

import click

from gamma.cli.services.pip.service import PipSetupService
from gamma.cli.services.project import ProjectService


@click.group()
@click.pass_obj
def cli(telemetry):
    """
    Allow you to setup your development environment
    """

    if telemetry is not None:
        telemetry.track_event("git new cmd")
        telemetry.flush()


@cli.group()
def pip():
    """
    Configure the user/site wide pip.conf file
    """


@pip.command()
def auto():
    """
    Auto configure Gamma default repositories.
    """

    pip_service = PipSetupService()
    pip_service.auto_install_repos()


@pip.command()
@click.argument("repo-names", nargs=-1)
def add_repo(repo_names):
    """
    Add one or more named repository to user "pip.conf" file.

    You can specify more than one repo name.
    """

    pip_service = PipSetupService()
    repos = []
    for repo_name in repo_names:
        repo = pip_service.get_repo(repo_name)
        if repo is None:
            s_reponame = click.style(repo_name, fg="cyan")
            raise click.ClickException(
                "Repository name " + s_reponame + " not found in registry."
            )
        repos.append(repo)

    session = {}
    for repo in repos:
        pip_service.install_repo(repo, session=session)


@pip.command()
def list_repos():
    """
    List known repositories in registry.
    """
    import tabulate

    pip_service = PipSetupService()

    headers = ["Provider", "Name", "Description", "Auto"]
    table = []

    for repo in pip_service.repositories:
        table.append(
            [repo.provider, repo.name, repo.description, "*" if repo.auto_setup else ""]
        )

    print(tabulate.tabulate(table, headers=headers, tablefmt="psql"))
