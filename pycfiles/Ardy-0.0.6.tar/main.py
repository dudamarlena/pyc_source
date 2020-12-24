# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prometeo/projects/ardy/ardy/core/cmd/main.py
# Compiled at: 2018-04-15 10:04:49
from __future__ import unicode_literals, print_function
import argparse, sys, traceback
from ardy.config import GlobalConfig
from ardy.core.build import Build
from ardy.core.deploy import Deploy
from ardy.utils.log import logger

class Command(object):
    config = None
    parser = None
    args = []

    def __init__(self, *args, **kwargs):
        arguments = kwargs.get(b'arguments', False)
        self.exit_at_finish = kwargs.get(b'exit_at_finish', True)
        if not arguments:
            arguments = sys.argv[1:]
        self.parser = self.init_config(arguments)
        commands = self.parser.add_subparsers(title=b'Commands', description=b'Available commands', dest=b'command_name')
        parser_deploy = commands.add_parser(b'deploy', help=b'Upload functions to AWS Lambda')
        parser_deploy.add_argument(b'lambdafunctions', default=b'_ALL_', nargs=b'*', type=str, help=b'Lambda(s) to deploy')
        parser_deploy.add_argument(b'-z', b'--zipfile', help=b'Path and filename of artefact to deploy')
        environments = self.config[b'deploy'].get(b'deploy_environments', [])
        if environments:
            parser_deploy.add_argument(b'environment', choices=environments, type=str, help=(b'Environment where deploy: {}').format(environments))
        parser_invoke = commands.add_parser(b'invoke', help=b'Invoke a functions from AWS Lambda')
        parser_invoke.add_argument(b'-l', b'--lambda-function', help=b'lambda')
        parser_build = commands.add_parser(b'build', help=b'Create an artefact and Upload to S3 if S3 is configured (See config)')
        parser_build.add_argument(b'-r', b'--requirements', help=b'Path and filename of the python project')
        self.args = self.parser.parse_args(arguments)
        try:
            result = self.parse_commandline()
            if result:
                self.exit_ok(b'OK')
        except Exception as e:
            logger.error(traceback.format_exc())

        self.exit_with_error(b'ERROR')

    @property
    def parser_base(self):
        parser = argparse.ArgumentParser(description=b'Ardy. AWS Lambda Toolkit')
        parser.add_argument(b'-f', b'--conffile', help=b'Name to the project config file')
        parser.add_argument(b'-p', b'--project', help=b'Project path')
        return parser

    def init_config(self, arguments):
        parser = self.parser_base
        parser.add_argument(b'args', nargs=argparse.REMAINDER)
        base_parser = parser.parse_args(arguments)
        params = {}
        if getattr(base_parser, b'project', False) and base_parser.project is not None:
            params[b'path'] = base_parser.project
        if getattr(base_parser, b'conffile', False) and base_parser.conffile is not None:
            params[b'filename'] = base_parser.conffile
        self.config = GlobalConfig(**params)
        return self.parser_base

    def parse_commandline(self):
        params = {}
        run_params = {}
        result = False
        if self.args.command_name == b'deploy':
            if self.args.lambdafunctions and self.args.lambdafunctions is not b'_ALL_':
                params[b'lambdas_to_deploy'] = self.args.lambdafunctions
            if getattr(self.args, b'environment', False):
                params[b'environment'] = self.args.environment
            if getattr(self.args, b'zipfile', False):
                run_params[b'path_to_zip_file'] = self.args.zipfile
            deploy = Deploy(config=self.config, **params)
            result = deploy.run(**run_params)
        elif self.args.command_name == b'invoke':
            pass
        elif self.args.command_name == b'build':
            if getattr(self.args, b'requirements', False):
                run_params[b'requirements'] = self.args.requirements
            build = Build(config=self.config)
            result = build.run(**params)
        else:
            self.parser.print_help()
        return result

    def exit_with_error(self, msg=b''):
        self.print_error(msg)
        if self.exit_at_finish:
            sys.exit(2)

    def exit_ok(self, msg=b''):
        self.print_ok(msg)
        if self.exit_at_finish:
            sys.exit(0)

    @staticmethod
    def print_ok(msg=b''):
        print(b'\x1b[92m\x1b[1m ' + msg + b' \x1b[0m\x1b[0m')

    @staticmethod
    def print_error(msg=b''):
        print(b'\x1b[91m\x1b[1m ' + msg + b' \x1b[0m\x1b[0m')


if __name__ == b'__main__':
    cmd = Command(arguments=sys.argv[1:])