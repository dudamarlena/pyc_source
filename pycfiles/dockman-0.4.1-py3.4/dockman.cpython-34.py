# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockman.py
# Compiled at: 2014-08-12 16:47:15
# Size of source mod 2**32: 1965 bytes
import json, argparse, docker
from flask import Flask, request, abort
app = Flask(__name__)
client = docker.Client(base_url='unix://var/run/docker.sock', version='1.13', timeout=60)

def safe_remove_container(container_name):
    client.stop(container_name)
    client.remove_container(container_name)


def container_exists(container_name, containers):
    listed_name = '/' + container_name
    return any([listed_name in c['Names'] for c in containers])


@app.route('/', methods=['POST'])
def docker_hook():
    d = None
    try:
        d = request.get_json(force=True)
    except Exception as e:
        app.logger.error('Error loading json', e)
        abort(400)

    if d:
        repo_name = d['repository']['repo_name']
        container = app.config.get('DOCKER_REPOS', {}).get(repo_name)
        if container:
            resp_stream = client.build(path=container['dockerfile_path'], tag=container['tag'])
            list(resp_stream)
            containers = client.containers(all=True)
            if container_exists(container['name'], containers):
                safe_remove_container(container['name'])
            client.create_container(container['tag'], name=container['name'])
            client.start(container['name'])
            return ('', 200)
        abort(403)


def load_repos(config_path):
    app.logger.info('Loading config %s' % config_path)
    with open(config_path) as (fp):
        return json.load(fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path')
    args = parser.parse_args()
    app.config['DOCKER_REPOS'] = load_repos(args.config_path)
    app.run()
else:
    app.config.from_envvar('DOCKMAN_CONFIG')
    app.config['DOCKER_REPOS'] = load_repos(app.config['REPOS_CONFIG'])