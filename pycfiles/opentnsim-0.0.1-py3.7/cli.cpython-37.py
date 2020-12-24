# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\opentnsim\cli.py
# Compiled at: 2019-07-18 03:25:05
# Size of source mod 2**32: 775 bytes
"""Console script for opentnsim."""
import sys, click, opentnsim.server

@click.group()
def cli(args=None):
    """OpenTNSim simulation."""
    click.echo('Replace this message by putting your code into opentnsim.cli.main')
    click.echo('See click documentation at http://click.pocoo.org/')
    return 0


@cli.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000, type=int)
@click.option('--debug/--no-debug', default=False)
def serve(host, port, debug, args=None):
    """Run a flask server with the backend code"""
    app = opentnsim.server.app
    app.run(host=host, debug=debug, port=port)


if __name__ == '__main__':
    sys.exit(cli())