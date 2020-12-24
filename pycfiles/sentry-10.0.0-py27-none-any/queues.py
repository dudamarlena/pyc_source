# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/runner/commands/queues.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import click
from sentry.runner.decorators import configuration

@click.group()
def queues():
    """Manage Sentry queues."""
    pass


@queues.command()
@click.option('-S', 'sort_size', default=False, is_flag=True, help='Sort by size.')
@click.option('-r', 'reverse', default=False, is_flag=True, help='Reverse the sort order.')
@configuration
def list(sort_size, reverse):
    """List queues and their sizes."""
    from django.conf import settings
    from sentry.monitoring.queues import backend
    if backend is None:
        raise click.ClickException('unknown broker type')
    queues = backend.bulk_get_sizes([ q.name for q in settings.CELERY_QUEUES ])
    if sort_size:
        queues = sorted(queues, key=lambda q: (-q[1], q[0]), reverse=reverse)
    else:
        queues = sorted(queues, reverse=reverse)
    for queue in queues:
        click.echo('%s %d' % queue)

    return


@queues.command()
@click.option('-f', '--force', default=False, is_flag=True, help='Do not prompt for confirmation.')
@click.argument('queue')
@configuration
def purge(force, queue):
    """Purge all messages from a queue."""
    from sentry.monitoring.queues import get_queue_by_name, backend
    if get_queue_by_name(queue) is None:
        raise click.ClickException('unknown queue: %r' % queue)
    if backend is None:
        raise click.ClickException('unknown broker type')
    size = backend.get_size(queue)
    if size == 0:
        click.echo('Queue is empty, nothing to purge', err=True)
        return
    else:
        if not force:
            click.confirm("Are you sure you want to purge %d messages from the queue '%s'?" % (size, queue), abort=True)
        click.echo('Poof, %d messages deleted' % backend.purge_queue(queue), err=True)
        return