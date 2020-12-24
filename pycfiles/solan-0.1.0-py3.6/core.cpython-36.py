# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solan/core.py
# Compiled at: 2019-05-04 10:50:47
# Size of source mod 2**32: 797 bytes
import click, http.server, os

@click.command()
@click.option('-p', '--port', type=int, default=8000, show_default=True)
@click.argument('directory', type=click.Path(exists=True))
def run(directory, port):
    click.echo('Sharing {}'.format(directory))
    os.chdir(directory)
    click.echo('Running the server')
    solan_server = http.server.HTTPServer
    solan_handler = http.server.SimpleHTTPRequestHandler
    solan_server_address = ('', port)
    httpd = solan_server(solan_server_address, solan_handler)
    click.echo('Service on {url}:{port}'.format(url='XXXXXX',
      port=port))
    httpd.serve_forever()