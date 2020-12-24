# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/package/dockerize.py
# Compiled at: 2020-03-21 21:05:05
# Size of source mod 2**32: 3194 bytes
import click, pkgutil, os, re

@click.option('--image-name', default='dockerized-app', help='Image name to use for build.')
@click.option('--port', type=int, default=(-1), help='The port to run the image on.')
@click.command()
def cli(image_name, port):
    """Main cli"""
    app_type = identify_app_type()
    click.echo(app_type + ' app detected')
    click.echo('Generating Dockerfile...')
    if app_type == 'JAVA_SPRING_BOOT':
        if not os.path.exists('target'):
            click.echo('here in 20')
            click.echo('No target/ present')
            exit(1)
            click.echo('here in 23')
        found_file = ''
        for filename in os.listdir('target/'):
            if re.search('.*\\.jar', filename):
                found_file = filename
                break

        if found_file == '':
            click.echo('here in 30')
            click.echo('No jar file present. Make sure your target/ contains a jar file')
            exit(1)
            click.echo('here in 33')
        text = pkgutil.get_data(__name__, 'templates/Java.Dockerfile').decode()
    open('Dockerfile', 'w').writelines([l for l in text])
    click.echo('Dockerfile generated')
    if port == -1:
        if app_type == 'JAVA_SPRING_BOOT':
            port = 8080
    click.echo('Building Docker image...')
    os.system('docker build -t {} .'.format(image_name))
    click.echo('Built image {}'.format(image_name))
    click.echo('Running Docker image...')
    os.system('docker run -p {}:{} {}'.format(port, port, image_name))


def identify_app_type():
    """Identify the project language to build Dockerfile"""
    return 'JAVA_SPRING_BOOT'