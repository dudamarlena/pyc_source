# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/package/dockerize.py
# Compiled at: 2020-04-08 00:25:06
# Size of source mod 2**32: 3514 bytes
import click, pkgutil, os, re

@click.option('--image-name', default='dockerized-app', help='The image name and optionally a tag in the ‘name:tag’ format.')
@click.option('--port', type=int, default=(-1), help='The port on which your application has been configured to run. (Your application will be exposed on the same port.)')
@click.option('--app-type', required=True, help='The type of app (FLASK, NODE_JS, SPRING_BOOT).')
@click.command()
def cli(image_name, port, app_type):
    """Main cli"""
    if port == -1:
        if app_type == 'FLASK':
            port = 5000
        else:
            port = 8080
    elif app_type == 'NODE_JS':
        handle_nodejs(image_name, port)
    else:
        if app_type == 'SPRING_BOOT':
            handle_java_spring_boot(image_name, port)
        else:
            if app_type == 'FLASK':
                handle_python_flask(image_name, port)


def handle_java_spring_boot(image_name, port):
    click.echo('Generating Dockerfile...')
    if not os.path.exists('target'):
        click.echo('No target/ present')
        exit(1)
    found_file = ''
    for filename in os.listdir('target/'):
        if re.search('.*\\.jar', filename):
            found_file = filename
            break

    if found_file == '':
        click.echo('No jar file present. Make sure your target/ contains a jar file')
        exit(1)
    text = pkgutil.get_data(__name__, 'templates/Java.Dockerfile').decode()
    open('Dockerfile', 'w').writelines([l for l in text])
    click.echo('Dockerfile generated')
    click.echo('Building Docker image...')
    os.system('docker build -t {} .'.format(image_name))
    click.echo('Built image {}'.format(image_name))
    click.echo('Running Docker image...')
    os.system('docker run -it -p {}:{} {}'.format(port, port, image_name))


def handle_python_flask(image_name, port):
    python_entrypoint_file = 'app.py'
    click.echo('Generating Dockerfile...')
    python_entrypoint_file = click.prompt('Enter python entrypoint file')
    os.environ['FLASK_ENTRYPOINT_FILE'] = python_entrypoint_file
    text = pkgutil.get_data(__name__, 'templates/Python-Flask.Dockerfile').decode()
    open('Dockerfile', 'w').writelines([l for l in text])
    click.echo('Dockerfile generated')
    click.echo('Building Docker image...')
    os.system('docker build -t {} --build-arg FLASK_ENTRYPOINT_FILE={} .'.format(image_name, python_entrypoint_file))
    click.echo('Built image {}'.format(image_name))
    click.echo('Running Docker image...')
    os.system('docker run -it -p {}:{} {}'.format(port, port, image_name))


def handle_nodejs(image_name, port):
    click.echo('Generating Dockerfile...')
    text = pkgutil.get_data(__name__, 'templates/NodeJS.Dockerfile').decode()
    open('Dockerfile', 'w').writelines([l for l in text])
    click.echo('Dockerfile generated')
    click.echo('Building Docker image...')
    os.system('docker build -t {} .'.format(image_name))
    click.echo('Built image {}'.format(image_name))
    click.echo('Running Docker image...')
    os.system('docker run -it -p {}:{} {}'.format(port, port, image_name))