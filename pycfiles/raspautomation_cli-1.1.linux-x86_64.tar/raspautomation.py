# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kipe/workspace/raspautomation_v2/cli/venv/lib/python2.7/site-packages/raspautomation_cli/scripts/raspautomation.py
# Compiled at: 2016-05-27 19:49:44
import os, click, raspautomation_cli as raspautomation

@click.group()
def cli():
    pass


@click.command()
@click.option('--url', prompt='URL', type=raspautomation.utils.URI)
@click.option('--token', prompt='Authentication token')
def auth(url, token):
    click.echo('Authentication started.')
    s = raspautomation.Server(url, token)
    if not s.test_auth():
        return
    s.refresh_data()
    click.echo('Server saved with name "%s".' % s.name)


@click.command()
@click.argument('server', type=str)
def refresh(server):
    click.echo('Refreshing information...')
    s = raspautomation.Server.find(server)
    s.refresh_data()
    s.save()


@click.command()
def clear():
    if click.confirm('Are you sure you want to clear all settings?'):
        if os.path.exists(raspautomation.server.CONF_FILE):
            os.unlink(raspautomation.server.CONF_FILE)
        click.echo('Cleared all settings.')


@click.command()
@click.argument('server', type=str)
@click.argument('method', type=click.Choice(['home', 'away', 'toggle']))
def presence(server, method):
    s = raspautomation.Server.find(server)
    if method == 'home':
        return s.presence.home()
    if method == 'away':
        return s.presence.away()
    if method == 'toggle':
        return s.presence.toggle()


@click.command()
@click.argument('server', type=str)
@click.argument('name', type=str)
@click.argument('method', type=click.Choice(['on', 'off', 'toggle', 'dim', 'set']))
@click.option('--level', type=int, default=0)
def io(server, name, method, level):
    s = raspautomation.Server.find(server)
    try:
        io = s.io.get(name)
        if io is None:
            raise IndexError
    except IndexError:
        raise IndexError('IO not found.')

    if method == 'on':
        return io.turn_on()
    else:
        if method == 'off':
            return io.turn_off()
        if method == 'toggle':
            return io.toggle()
        if method in ('dim', 'set'):
            return io.set(level)
        return


@click.command()
@click.argument('server', type=str)
@click.argument('name', type=str)
@click.argument('method', type=click.Choice(['on', 'off', 'toggle']))
@click.option('--level', type=int, default=0)
def camera(server, name, method, level):
    s = raspautomation.Server.find(server)
    try:
        camera = s.camera.get(name)
        if camera is None:
            raise IndexError
    except IndexError:
        raise IndexError('Camera not found.')

    if method == 'on':
        return camera.turn_on()
    else:
        if method == 'off':
            return camera.turn_off()
        if method == 'toggle':
            return camera.toggle()
        return


cli.add_command(auth)
cli.add_command(refresh)
cli.add_command(clear)
cli.add_command(presence)
cli.add_command(io)
cli.add_command(camera)
if __name__ == '__main__':
    cli()