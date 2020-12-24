# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/isacpetruzzi/Code/artsy/hokusai/hokusai/commands/development.py
# Compiled at: 2019-10-09 12:07:43
import os, signal
from hokusai import CWD
from hokusai.lib.command import command
from hokusai.lib.config import HOKUSAI_CONFIG_DIR, DEVELOPMENT_YML_FILE, config
from hokusai.lib.common import print_green, shout, EXIT_SIGNALS
from hokusai.lib.exceptions import HokusaiError
from hokusai.services.docker import Docker

@command()
def dev_start(build, detach, filename):
    if filename is None:
        docker_compose_yml = os.path.join(CWD, HOKUSAI_CONFIG_DIR, DEVELOPMENT_YML_FILE)
    else:
        docker_compose_yml = filename
    if not os.path.isfile(docker_compose_yml):
        raise HokusaiError('Yaml file %s does not exist.' % docker_compose_yml)

    def cleanup(*args):
        shout('docker-compose -f %s -p hokusai stop' % docker_compose_yml, print_output=True)

    for sig in EXIT_SIGNALS:
        signal.signal(sig, cleanup)

    opts = ''
    if build:
        Docker().build(filename)
    if detach:
        opts += ' -d'
    if not detach:
        print_green('Starting development environment... Press Ctrl+C to stop.')
    shout('docker-compose -f %s -p hokusai up%s' % (docker_compose_yml, opts), print_output=True)
    if detach:
        print_green('Run `hokousai dev stop` to shut down, or `hokusai dev logs --follow` to tail output.')
    return


@command()
def dev_stop(filename):
    if filename is None:
        docker_compose_yml = os.path.join(CWD, HOKUSAI_CONFIG_DIR, DEVELOPMENT_YML_FILE)
    else:
        docker_compose_yml = filename
    if not os.path.isfile(docker_compose_yml):
        raise HokusaiError('Yaml file %s does not exist.' % docker_compose_yml)
    shout('docker-compose -f %s -p hokusai stop' % docker_compose_yml, print_output=True)
    return


@command()
def dev_status(filename):
    if filename is None:
        docker_compose_yml = os.path.join(CWD, HOKUSAI_CONFIG_DIR, DEVELOPMENT_YML_FILE)
    else:
        docker_compose_yml = filename
    if not os.path.isfile(docker_compose_yml):
        raise HokusaiError('Yaml file %s does not exist.' % docker_compose_yml)
    shout('docker-compose -f %s -p hokusai ps' % docker_compose_yml, print_output=True)
    return


@command()
def dev_logs(follow, tail, filename):
    if filename is None:
        docker_compose_yml = os.path.join(CWD, HOKUSAI_CONFIG_DIR, DEVELOPMENT_YML_FILE)
    else:
        docker_compose_yml = filename
    if not os.path.isfile(docker_compose_yml):
        raise HokusaiError('Yaml file %s does not exist.' % docker_compose_yml)
    opts = ''
    if follow:
        opts += ' --follow'
    if tail:
        opts += ' --tail=%i' % tail
    shout('docker-compose -f %s -p hokusai logs%s' % (docker_compose_yml, opts), print_output=True)
    return


@command()
def dev_run(command, service_name, stop, filename):
    if filename is None:
        docker_compose_yml = os.path.join(CWD, HOKUSAI_CONFIG_DIR, DEVELOPMENT_YML_FILE)
    else:
        docker_compose_yml = filename
    if not os.path.isfile(docker_compose_yml):
        raise HokusaiError('Yaml file %s does not exist.' % docker_compose_yml)
    if service_name is None:
        service_name = config.project_name
    shout('docker-compose -f %s -p hokusai run %s %s' % (docker_compose_yml, service_name, command), print_output=True)
    if stop:
        shout('docker-compose -f %s -p hokusai stop' % docker_compose_yml, print_output=True)
    return


@command()
def dev_clean(filename):
    if filename is None:
        docker_compose_yml = os.path.join(CWD, HOKUSAI_CONFIG_DIR, DEVELOPMENT_YML_FILE)
    else:
        docker_compose_yml = filename
    if not os.path.isfile(docker_compose_yml):
        raise HokusaiError('Yaml file %s does not exist.' % docker_compose_yml)
    shout('docker-compose -f %s -p hokusai stop' % docker_compose_yml, print_output=True)
    shout('docker-compose -f %s -p hokusai rm --force' % docker_compose_yml, print_output=True)
    return