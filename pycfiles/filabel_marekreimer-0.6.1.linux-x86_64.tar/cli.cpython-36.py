# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/filabel/cli.py
# Compiled at: 2018-12-31 12:32:10
# Size of source mod 2**32: 5427 bytes
import configparser, click, asyncio
from filabel.logic import AsyncFilabel, Filabel, Change
from filabel.utils import parse_labels
import sys

def stylize_label_change(change_type, label):
    """
    Stylize change with given type and changed label

    change_type: type of change
    label: name of changed label
    """
    if change_type == Change.ADD:
        return click.style(f"+ {label}", fg='green')
    else:
        if change_type == Change.DELETE:
            return click.style(f"- {label}", fg='red')
        return f"= {label}"


def print_pr(pr_link, result, asynch=False):
    """
    Print report of individual PR

    pr_link: Link to PR
    result: Result of labeling
    """
    if not asynch:
        click.secho('  ', nl=False)
    else:
        click.secho('PR', nl=False, bold=True)
        click.secho(f" {pr_link} - ", nl=False)
        if result is None:
            click.secho('FAIL', fg='red', bold=True)
        else:
            click.secho('OK', fg='green', bold=True)
            for label, t in result:
                if not asynch:
                    click.secho('  ', nl=False)
                click.secho(f"  {stylize_label_change(t, label)}")


def print_async_report(report):
    """
    Print Filabel asynchronous report to command line

    report: Report to be printed
    """
    if report.ok:
        for pr_link, result in report.prs.items():
            print_pr(pr_link, result, True)

        click.secho('REPO', nl=False, bold=True)
        click.secho(f" {report.repo} - ", nl=False)
        click.secho('OK', fg='green', bold=True)
    else:
        click.secho('REPO', nl=False, bold=True)
        click.secho(f" {report.repo} - ", nl=False)
        click.secho('FAIL', fg='red', bold=True)


def print_report(report):
    """
    Print Filabel report to command line

    report: Report to be printed
    """
    click.secho('REPO', nl=False, bold=True)
    click.secho(f" {report.repo} - ", nl=False)
    if report.ok:
        click.secho('OK', fg='green', bold=True)
        for pr_link, result in report.prs.items():
            print_pr(pr_link, result)

    else:
        click.secho('FAIL', fg='red', bold=True)


def get_token(config_auth):
    """
    Extract token from auth config and do the checks

    config_auth: ConfigParser with loaded configuration of auth
    """
    if config_auth is None:
        click.secho('Auth configuration not supplied!', err=True)
        exit(1)
    try:
        cfg_auth = configparser.ConfigParser()
        cfg_auth.read_file(config_auth)
        return cfg_auth.get('github', 'token')
    except Exception:
        click.secho('Auth configuration not usable!', err=True)
        exit(1)


def get_labels(config_labels):
    """
    Extract labels from labels config and do the checks

    config_labels: ConfigParser with loaded configuration of labels
    """
    if config_labels is None:
        click.secho('Labels configuration not supplied!', err=True)
        exit(1)
    try:
        cfg_labels = configparser.ConfigParser()
        cfg_labels.read_file(config_labels)
        return parse_labels(cfg_labels)
    except Exception:
        click.secho('Labels configuration not usable!', err=True)
        exit(1)


def check_reposlugs(reposlugs):
    """
    Check formatting of reposlugs (contains 1 "/")

    reposlugs: List of reposlugs (i.e. "owner/repo")
    """
    for reposlug in reposlugs:
        if len(reposlug.split('/')) != 2:
            click.secho(f"Reposlug {reposlug} not valid!", err=True)
            exit(1)


@click.command('filabel')
@click.argument('reposlugs', nargs=(-1))
@click.option('-s', '--state', type=(click.Choice(['open', 'closed', 'all'])), default='open',
  show_default=True,
  help='Filter pulls by state.')
@click.option('-d/-D', '--delete-old/--no-delete-old', default=True, show_default=True,
  help='Delete labels that do not match anymore.')
@click.option('-b', '--base', type=str, metavar='BRANCH', help='Filter pulls by base (PR target) branch name.')
@click.option('-a', '--config-auth', type=(click.File('r')), help='File with authorization configuration.')
@click.option('-l', '--config-labels', type=(click.File('r')), help='File with labels configuration.')
@click.option('-x', '--async', 'asynch', default=False, is_flag=True,
  help='Use asynchronnous (faster) logic.')
def cli(reposlugs, state, delete_old, base, config_auth, config_labels, asynch):
    """
    CLI tool for filename-pattern-based labeling of GitHub PRs
    """
    token = get_token(config_auth)
    labels = get_labels(config_labels)
    check_reposlugs(reposlugs)
    if asynch:
        asyncio.run(run_async(reposlugs, token, labels, state, base, delete_old))
    else:
        fl = Filabel(token, labels, state, base, delete_old)
        for repo in reposlugs:
            report = fl.run_repo(repo)
            print_report(report)


async def run_async(reposlugs, token, labels, state, base, delete_old):
    """
    Function to manage labeling individual repositories asynchronnously.
    """
    fl = AsyncFilabel(token, labels, state, base, delete_old)
    loop = asyncio.get_event_loop()
    for future in asyncio.as_completed((map(fl.run_repo, reposlugs)), loop=loop):
        res = await future
        print_async_report(res)

    await fl.github.session.close()