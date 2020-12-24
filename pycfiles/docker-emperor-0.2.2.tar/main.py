# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/main.py
# Compiled at: 2018-08-13 03:18:20
import os, sys, yaml, tempfile, json, collections, six, argparse, subprocess, imp
from pprint import pprint
from docker_emperor.commands import Command
from docker_emperor.nodes.project import Project
from docker_emperor.exceptions import DockerEmperorException
from docker_emperor.utils import setdefaultdict, combine, yamp_load
import docker_emperor.logger as logger

class DockerEmperor:
    version = __import__('docker_emperor').__version__

    def __init__(self, argsflat2=''):
        self.argsflat2 = argsflat2
        print argsflat2
        self.module_root = os.path.dirname(os.path.abspath(__file__))
        self.bin_root = os.path.join(self.module_root, 'bin')
        self.config_path = os.path.expanduser(os.path.join('~', '.docker-emperor'))
        try:
            self.config = json.load(open(self.config_path, 'rb'))
        except:
            self.config = {}

        self.docker_path = 'docker'
        self.logger = logger.Logger(self)
        self.current_mounting = None
        return

    @property
    def root_path(self):
        return os.getcwd()

    @property
    def projects(self):
        n = '__projects'
        if not hasattr(self, n):
            self.config['projects'] = setdefaultdict(self.config.setdefault('projects'))
            setattr(self, n, self.config['projects'])
        return getattr(self, n)

    @property
    def project(self):
        n = '__project'
        if not hasattr(self, n):
            setattr(self, n, Project(self))
        return getattr(self, n)

    @property
    def mounting(self):
        return self.project.mounting

    @property
    def compose(self):
        return self.project.compose

    def entrypoint(self, cmd=None, *args):
        try:
            args = list(args)
            if cmd:
                self.run_command(cmd, *args)
                self.save_config()
            else:
                logger.info(('docker-emperor version {}').format(self.version))
        except DockerEmperorException as e:
            logger.error(e)

    def run_command(self, name, *args, **kwargs):
        internal = kwargs.pop('internal', False)
        if args and args[(-1)][0] == '@':
            self.current_mounting = args[(-1)][1:]
            args = args[0:-1]
        if '--verbose' in args:
            Command.verbose = 1
        try:
            module_name = name.replace(':', '.')
            mod = __import__(('docker_emperor.commands.{}').format(module_name), globals(), locals(), ['run'], 0)
            return mod.run(self, *args, **kwargs)
        except ImportError as e:
            if internal:
                raise ImportError(e)
            elif not self.project.run_command(name, *args, **kwargs):
                logger.error('Unknown command %s' % name)
            return False

    def bash(self, *args, **kwargs):
        cmd = Command(*args, **kwargs)
        cmd.run()
        return cmd

    def save_config(self):
        if self.config:
            file = open(self.config_path, 'wb')
            file.write(json.dumps(self.config, indent=4))
            file.close()


def entrypoint():
    try:
        argsparser = argparse.ArgumentParser(description='Docker emperor orchestrator')
        argsparser.add_argument('args', nargs=argparse.REMAINDER, action='store')
        DockerEmperor().entrypoint(argsflat2=((' ').join(sys.argv[1:-1]) if len(sys.argv) >= 2 else ''), *argsparser.parse_args().args)
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt, exiting.')
        exit(0)


if __name__ == '__main__':
    entrypoint()