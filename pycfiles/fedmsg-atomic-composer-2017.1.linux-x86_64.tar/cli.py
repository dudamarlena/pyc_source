# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/fedmsg_atomic_composer/cli.py
# Compiled at: 2016-10-12 09:09:27
import click, time, tempfile, pprint
from fedmsg_atomic_composer.composer import AtomicComposer
from fedmsg_atomic_composer.config import config

def get_release(release):
    releases = config['releases']
    if release not in releases:
        raise click.BadParameter('Unknown release. Valid releases are: %s' % releases.keys())
    return releases[release]


@click.group()
def cli():
    pass


@cli.command(help='Compose an ostree for a given release')
@click.argument('release')
def compose(release):
    release = get_release(release)
    composer = AtomicComposer()
    result = composer.compose(release)
    if result['result'] == 'success':
        click.echo(('{name} tree successfuly composed').format(**result))
    else:
        click.echo(('{name} tree compose failed').format(**result))
        click.echo(str(result))
    click.echo(('Log: {log_file}').format(**result))


@cli.command(help='List available releases')
@click.option('--json', is_flag=True)
def releases(json):
    if json:
        click.echo(pprint.pformat(config['releases']))
    else:
        for release in config['releases']:
            click.echo(release)


@cli.command()
@click.argument('release')
def clean(release):
    release = get_release(release)
    composer = AtomicComposer()
    release['tmp_dir'] = tempfile.mkdtemp()
    release['timestamp'] = time.strftime('%y%m%d.%H%M')
    composer.setup_logger(release)
    composer.generate_mock_config(release)
    composer.mock_cmd(release, '--clean')


if __name__ == '__main__':
    cli()